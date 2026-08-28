from fastapi import FastAPI

from madr_api.routers import books, novelists, users, auth

app = FastAPI()
app.include_router(novelists.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def helloworld():
    return {"message": "hello world"}
