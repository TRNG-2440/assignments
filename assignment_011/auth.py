 # Authentication logic

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

# Hard code user list for simplicity
USERS = {
  "Administrator": "Hello123",
  "Kdawg": "Berk02394"
}

# Input validation - verify user credentials
def VerifyUser(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    password = USERS.get(credentials.username, "")

   # Apply secret plug-ins to eliminate timing attacks
    correctPassword = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        password.encode("utf-8"),
    )

    if not correctPassword:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="\nError - Invalid password\n",
            headers={"WWW-Authenticate": "Basic"},
        )
        
    return credentials.username
        
