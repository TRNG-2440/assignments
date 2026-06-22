from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

USER_API_KEY = "secret-key-dont-steal-me-bro"

api_key_header = APIKeyHeader(name="X-Api-Key", auto_error=True)

def check_key_header(api_key: str = Depends(api_key_header)):
    if api_key != USER_API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Key Provided")
    return api_key