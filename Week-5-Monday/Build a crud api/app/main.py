from fastapi import FastAPI

from app.routers import movies

app = FastAPI(title="My CRUD API", version="0.1.0")


@app.get("/")
def read_root():
    return {"status": "ok"}


app.include_router(movies.router)
