"""
Basic HTTP username:password authentication for Movie Watchlist API
"""

# libraries
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# security scheme
security = HTTPBasic()

# user store
USERS = {
    "Will": "gogauchos"
}

# credential comparison
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    stored_password = USERS.get(credentials.username, "")
    password_correct = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        stored_password.encode("utf-8")
    )

    if not password_correct:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid username or password",
            headers = {"WWW-Authenticate": "Basic"}
        )
    
    return credentials.username