from fastapi import FastAPI, HTTPException, status, Query
from models import MovieCreate, MovieOut, MovieUpdate
from routers import movies

VERSION = "0.1.0"

app = FastAPI(
    title = "My CRUD Movie API",
    version = VERSION,
)

app.include_router(movies.router)

@app.get("/")
def read_root():
    return {"message": "Welcome, movie lovers!"}

@app.get("/health")
def get_health():
    return {"status": "ok", "version": VERSION}