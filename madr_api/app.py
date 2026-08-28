import asyncio
import sys

from fastapi import FastAPI

from madr_api.routers import auth, books, novelists, users

app = FastAPI()
app.include_router(novelists.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(auth.router)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@app.get("/")
def helloworld():
    return {"message": "hello world"}
