from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader



EXPECTED_API_KEY = "Wellness123"

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key == EXPECTED_API_KEY:
        return api_key
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")