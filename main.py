from fastapi import FastAPI
from models import User
from util import get


api = FastAPI()

@api.get("/fastapi/user/{user_id}/{user_name}")
def get_user(user_id: int, user_name: str):
	return User(id=user_id, username=user_name)

@get(api)
def get_user_ideal(_=f"/mine/user/{(user_id:=int())=}/{(user_name:=str())=}"):
	return User(id=user_id, username=user_name)

@get(api)
def get_user_default_name(_=f"/mine/user/{(user_id:=int())=}"):
	return User(id=user_id, username="default username")

