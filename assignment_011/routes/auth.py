from typing import Annotated

from fastapi import APIRouter, Depends, status

from models.users import UserResponse
from services.auth import verify_credentials, validate_and_create_user


router = APIRouter()


@router.post("/login")
def authenticate_login(
    user: Annotated[UserResponse, Depends(verify_credentials)],
) -> UserResponse:
    return user


@router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(
    user: Annotated[UserResponse, Depends(validate_and_create_user)],
) -> UserResponse:
    return user
