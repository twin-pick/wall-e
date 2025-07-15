from fastapi import FastAPI
from services.wall_eV4 import scrap_watch_list as scrap_mark4
from services.wall_eV3 import scrap_watch_list as scrap_mark3
from services.wall_eV2 import scrap_watch_list as scrap_mark2
from services.wall_e import scrap_watch_list as scrap

app = FastAPI()

from concurrent.futures import ThreadPoolExecutor
import asyncio
executor = ThreadPoolExecutor(max_workers=2)


@app.get("/")
async def hello_world():
    return {"message": "Hello world"}


@app.get("/api/v1/{user}/watchlist")
async def scrap_user_mark1(user: str):
    print(user)
    list = scrap(user)
    return list


@app.get("/api/v1/{user}/watchlist/{genre}")
async def scrap_user_genre_mark1(user: str, genre: str):
    genre = genre.split(',')
    print(genre)
    list = scrap(user, genre)
    return list


@app.get("/api/v2/{user}/watchlist")
async def scrap_user_mark2(user: str):
    print(user)
    list = scrap_mark2(user)
    return list


@app.get("/api/v2/{user}/watchlist/{genre}")
async def scrap_user_genre_mark2(user: str, genre: str):
    genre = genre.split(',')
    print(genre)
    list = scrap_mark2(user, genre)
    return list


@app.get("/api/v3/{user}/watchlist")
async def scrap_user_mark3(user: str):
    print(user)
    list = await scrap_mark3(user)
    return list


@app.get("/api/v3/{user}/watchlist/{genre}")
async def scrap_user_genre_mark3(user: str, genre: str):
    genre = genre.split(',')
    print(genre)
    list = scrap_mark3(user, genre)
    return list

@app.get("/api/v4/{user}/watchlist")
async def scrap_user_v4(user: str):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        executor,
        lambda: scrap_mark4(user, [])  # ou passer des genres
    )
    return result  

@app.get("/api/v4/{user}/watchlist/{genre}")
async def scrap_user_v4(user: str):
    genre = genre.split(',')
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        executor,
        lambda: scrap_mark4(user, genre)  # ou passer des genres
    )
    return result 


@app.get("/api/health")
async def health():
    return
