"""
Movie Watchlist API
"""
# depedencies
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import InvalidAPIKeyException
from routers import router as movies_router
from starlette import status

# application instance
app = FastAPI(
    title = "Movie Watchlist API",
    version = "1.0.0"
)

# register endpoint routers
app.include_router(movies_router)


# ========================================================================
# EXTRA - NOT REALLY NEEDED, but why not
# basic (synchronous) route to confirm app works
@app.get("/", tags = ["Public"], summary = "Welcome message",
         description = "Public welcome route. No authentication required.")
def read_root():
    return {"message": "Welcome to the Movie Watchlist API"}

# asynchronous status route
@app.get("/status", tags = ["Public"], summary = "Service status",
         description = "Public route reporting the running status and version. No authentication required.")
async def get_status():
    return {"status": "running", "version": "1.0.0"}
# ========================================================================

@app.exception_handler(InvalidAPIKeyException)
async def invalid_api_key_handler(request: Request, exc: InvalidAPIKeyException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": {
                "code": status.HTTP_403_FORBIDDEN,
                "type": "InvalidAPIKey",
                "message": exc.message
            }
        }
    )
