# FastAPI app entry point, router registration
from fastapi import FastAPI
from pathlib import Path


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}



