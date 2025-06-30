from fastapi import FastAPI
from services.wall_eV2 import scrap_watch_list as scrap_v2
from services.wall_e import scrap_watch_list as scrap

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message": "Hello world"}

@app.get("/api/v1/{user}/watchlist")
async def scrap_user(user: str):
    print(user)
    list = scrap(user)
    return list

@app.get("/api/v2/{user}/watchlist")
async def scrap_user(user: str):
    print(user)
    list = scrap_v2(user)
    return list
