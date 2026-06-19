"""Authentication and registration service functions, wired up as FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from utils import hash_password, verify_password
from repository.users import UsersRepository
from models.users import UserCreate, UserDAO, UserResponse
from exceptions.auth import (
    AuthenticationError,
    UserAlreadyExistsError,
)

# HTTP Basic auth scheme used to extract username/password from the request.
security = HTTPBasic()


def verify_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    users_repo: Annotated[UsersRepository, Depends(UsersRepository)],
) -> UserResponse:
    """
    FastAPI dependency that authenticates a request via HTTP Basic auth.

    Looks up the user by username and verifies the supplied password
    against the stored bcrypt hash.

    :param credentials: Username/password extracted from the Authorization header.
    :param users_repo: Repository used to look up the user record.
    :return: The authenticated user's public-facing representation.
    :raises UserDoesNotExistError: If no user with that username exists.
    :raises AuthenticationError: If the password does not match.
    """
    user: UserDAO = users_repo.get_user(credentials.username)
    if not verify_password(credentials.password, user.password):
        raise AuthenticationError(username=credentials.username)
    return create_response(user)


def validate_and_create_user(
    user: UserCreate, users_repo: Annotated[UsersRepository, Depends(UsersRepository)]
) -> UserResponse:
    """
    Validates uniqueness, hashes the password, and persists a new user.

    :param user: The incoming registration payload.
    :param users_repo: Repository used to check uniqueness and store the user.
    :return: The newly created user's public-facing representation.
    :raises UserAlreadyExistsError: If the username or email is already taken.
    """
    if not users_repo.check_unique_user(username=user.username, email=user.email):
        raise UserAlreadyExistsError(username=user.username, email=user.email)
    hashed_pwd = hash_password(user.password)
    record: UserDAO = create_record(user, hashed_pwd)
    users_repo.create_user(record)
    return create_response(record)


def create_record(user: UserCreate, hashed_pwd: str) -> UserDAO:
    """
    Builds a storable UserDAO from a registration payload and its hashed password.

    Mutates `user.password` in place to the hashed value before converting.

    :param user: The validated registration payload (plaintext password).
    :param hashed_pwd: The bcrypt hash of the user's password.
    :return: A UserDAO ready to be persisted (with an auto-assigned id).
    """
    user.password = hashed_pwd
    return UserDAO.model_validate(user.model_dump())


def create_response(user: UserDAO) -> UserResponse:
    """
    Converts an internal UserDAO into the public-facing UserResponse shape,
    dropping sensitive fields such as the password hash.

    :param user: The internal user record.
    :return: A UserResponse safe to return from the API.
    """
    return UserResponse.model_validate(user.model_dump(), extra="ignore")
