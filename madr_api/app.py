from fastapi import FastAPI

from madr_api.routers import books, novelists

app = FastAPI()
app.include_router(novelists.router)
app.include_router(books.router)


@app.get("/")
def helloworld():
    return {"message": "hello world"}
