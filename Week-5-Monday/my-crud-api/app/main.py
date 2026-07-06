# dependencies
from fastapi import FastAPI

app = FastAPI(title = "My Movies CRUD API", version = "1.0.0")

@app.get("/")
def read_root():
    return {"status": "ok"}