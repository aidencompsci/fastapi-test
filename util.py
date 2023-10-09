from types import FunctionType

from fastapi import FastAPI
from typing import Callable

def _parse_var_from_path(path):
	vardec: str = path.rsplit("=", 1)[0]
	vardecsplit = vardec.split(":=", 1)
	var = vardecsplit[0].replace("(", "").replace(")", "")
	vartype = vardecsplit[1].replace("(", "").replace(")", "")
	return var, vartype

def _get_func_vars(vars: list[tuple[str, str]]):
	return ", ".join([f"{var}: {vartype}" for var,vartype in vars])

def _get_func_setters(vars: list[tuple[str, str]]):
	return "; ".join([f"func.__globals__['{var}'] = {var}" for var, vartype in vars])

def get(app: FastAPI):
	def get_inner(func: FunctionType | Callable):
		if not isinstance(func.__defaults__[0], str): raise Exception("path must be fstring")
		fullpath = ""
		vars: list[tuple[str, str]] = []
		for p in func.__defaults__[0].split("/"):
			if not p: continue
			if p.count("=") == 2:
				var,vartype = _parse_var_from_path(p)
				vars.append((var, vartype))
				p = "{" + var + "}"
			fullpath += f"/{p}"

		func_vars = _get_func_vars(vars)
		func_setters = _get_func_setters(vars)

		funcdev = f"""@app.get("{fullpath}")
def __create_get__({func_vars}): {func_setters}; return func()"""
		exec(funcdev, {"app": app, "func": func})

		def get_wrapper(*args, **kwargs):
			return func(*args, **kwargs)
		return get_wrapper
	return get_inner