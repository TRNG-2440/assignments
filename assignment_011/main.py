"""
Movie Watchlist API
"""
# depedencies
from logging_config import logger
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from exceptions import InvalidAPIKeyException
from auth import verify_api_key
from starlette import status

# application instance
app = FastAPI(
    title = "Movie Watchlist API",
    version = "1.0.0"
)


# ========================================================================
# EXTRA - NOT REALLY NEEDED, but why not
# basic (synchronous) route to confirm app works
@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Watchlist API"}

# asynchronous status route 
@app.get("/status")
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

# authentication route
@app.post("/auth", tags = ["Auth"])
def authenticate(request: Request, response: JSONResponse = None, api_key: str = Depends(verify_api_key)):  # pyright: ignore[reportArgumentType]
    logger.info("Authentication successful — session cookie issued")

    resp = JSONResponse(
        content = {"message": "Authenticated successful, session cookie set."},
        status_code = status.HTTP_200_OK
    )
    resp.set_cookie(
        key="session",
        value="authenticated",
        httponly=True,
        max_age=3600,
        samesite="lax"
    )
    return resp

# cookie validation helper
def require_session(request: Request):
    # Reads the session cookie set by POST /auth.
    # Any route that depends on this will be blocked if the
    # cookie is absent — the client must authenticate first.
    session = request.cookies.get("session")
    if not session or session != "authenticated":
        logger.warning(f"Request without valid session cookie — path: {request.url.path}")
        raise InvalidAPIKeyException()