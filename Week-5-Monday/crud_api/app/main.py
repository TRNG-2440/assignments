from fastapi import FastAPI
from .routers import entry

app = FastAPI(
    title="journal entry api",
    version="0.1.0"
)

app.include_router(entry.router)

@app.get("/")
def read_root():
    return {"message": "journal entry api. See /docs for the interactive docs."}