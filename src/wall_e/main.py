from fastapi import FastAPI
from services.wall_eV2 import scrap_watch_list

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message": "Hello world"}

@app.get("/api/v1/{user}/watchlist")
async def scrap_user(user: str):
    print(user)
    list = scrap_watch_list(user)
    return list
