from fastapi import FastAPI

app = FastAPI(title="My CRUD API", version="0.1.0")

@app.get("/")
def read_root():
    return {"status": "ok"}