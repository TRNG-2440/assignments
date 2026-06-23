"""
Basic API key authentication
"""

# libraries
import secrets
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from exceptions import InvalidAPIKeyException
from main import logger

# map of valid api keys to specific user
# would be stored in a database in a real app
VALID_API_KEY = "gogauchos"

# api key header for authentication
api_key_header = APIKeyHeader(name = "x-api-key", auto_error = False)

# verify a key
def verify_api_key(request: Request, api_key: str = Depends(api_key_header)):
    if not api_key or api_key != VALID_API_KEY:
        logger.warning(f"Failed API key attempt - path: {request.url.path}")
        raise InvalidAPIKeyException()
    logger.info(f"API key validated - path: {request.url.path}")
    return api_key