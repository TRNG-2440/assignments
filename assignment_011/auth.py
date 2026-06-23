"""
Basic API key authentication
"""

# libraries
import secrets
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader
from exceptions import InvalidAPIKeyException
from logging_config import logger

# map of valid api keys to specific user
# would be stored in a database in a real app
VALID_API_KEY = {
    "gogauchos": "william",
    "secondkey": "bob"
}

# api key header for authentication
api_key_header = APIKeyHeader(name = "x-api-key", auto_error = False)

# verify a key
def verify_api_key(request: Request, api_key: str = Depends(api_key_header)):
    if not api_key or api_key not in VALID_API_KEY:
        logger.warning(f"Failed API key attempt - path: {request.url.path}")
        raise InvalidAPIKeyException()
    username = VALID_API_KEY[api_key]
    logger.info(f"API key validated - path: {request.url.path}")
    return username