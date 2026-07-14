"""
FastAPI app entry point.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

import services
from routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    services.load_data()
    yield

app = FastAPI(
    title = "Transactions DataFrame API",
    description = "Serves pandas-computed transaction data from CSV to JSON",
    lifespan = lifespan
)

app.include_router(router)

@app.get("/health")
def health():
    return {
        "status": "Working!",
        "transactions": len(services.load_data())
    }

@app.get("/")
def root():
    return {"message": "Welcome!"}