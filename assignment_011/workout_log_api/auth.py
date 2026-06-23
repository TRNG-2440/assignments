from fastapi import Depends, HTTPException, status 
from fastapi.security import APIKeyHeader

API_KEY = "workout-secret-key"

api_key_header = APIKeyHeader(name = 'X-APIKey')


def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Invalid or missing API key"
        )
    return api_key
