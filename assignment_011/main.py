"""
Movie Watchlist API
"""
# depedencies
from fastapi import FastAPI, Depends
from auth import get_current_user

# application instance
app = FastAPI(
    title = "Movie Watchlist API",
    description = "Track movies you've watched, give ratings for moveis, and more!",
    version = "1.0.0"
)

# basic (synchronous) route to confirm app works
@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Watchlist API"}

# asynchronous status route 
@app.get("/status")
async def get_status():
    return {"status": "running", "version": "1.0.0"}

@app.get("/me")
def read_me(user: str = Depends(get_current_user)):
    return {"authenticated_as": user}