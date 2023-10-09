import asyncio
from typing import Any
import aiohttp
from aiohttp import ClientSession
from models import User

def handle_200(url: str, data: Any):
	try:
		user: User = User.from_dict(data)
		print(f"{url} -> {user}")
	except Exception as e:
		print(f"Error deserializing from {url} -> {data}", e)

async def fetch_url(session: ClientSession, url: str):
	async with session.get(url) as response:
		data = await response.json()
		if response.status == 200: handle_200(url, data)
		else: print(f"Error getting response from {url}")

async def main():
	urls: list[str] = []
	for i in range(100):
		urls.append(f"http://localhost:8000/fastapi/user/{i}/billy")
	for i in range(100):
		urls.append(f"http://localhost:8000/mine/user/{i}/billy")
	for i in range(100):
		urls.append(f"http://localhost:8000/mine/user/{i}")

	async with aiohttp.ClientSession() as session:
		tasks = [fetch_url(session, url) for url in urls]
		await asyncio.gather(*tasks)

if __name__ == '__main__':
	asyncio.run(main())
