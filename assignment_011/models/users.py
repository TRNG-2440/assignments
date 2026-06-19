"""Pydantic models for user creation, storage, and API responses."""

from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field, field_validator
from exceptions.auth import InvalidPasswordError

MINIMUM_PASSWORD_LENGTH = 8


class UserCreate(BaseModel):
    """Incoming payload for registering a new user (e.g. from a signup request)."""

    username: str = Field(min_length=2, max_length=30)
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def check_password_requirements(cls, password: str) -> str:
        """
        Validates that `password` meets minimum strength requirements.

        Requires at least MINIMUM_PASSWORD_LENGTH characters, with at least
        one uppercase letter, one lowercase letter, one digit, and one
        special (non-alphanumeric) character.

        :param password: The plaintext candidate password.
        :return: The same password, unchanged, if it passes all checks.
        :raises InvalidPasswordError: If any requirement is not met.
        """
        has_upper_char = any(char.isupper() for char in password)
        has_lower_char = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special_char = any(not char.isalnum() for char in password)
        if len(password) < MINIMUM_PASSWORD_LENGTH:
            raise InvalidPasswordError(
                detail="Password must be at least 8 characters long."
            )
        if not has_upper_char:
            raise InvalidPasswordError(
                detail="Password must contain at least one uppercase letter."
            )
        if not has_lower_char:
            raise InvalidPasswordError(
                detail="Password must contain at least one lowercase letter."
            )
        if not has_digit:
            raise InvalidPasswordError(
                detail="Password must contain at least one digit."
            )
        if not has_special_char:
            raise InvalidPasswordError(
                detail="Password must contain at least one special character"
            )
        return password


class UserDAO(BaseModel):
    """Internal data-access representation of a user, including the hashed password.

    This is the shape persisted to/read from storage; `password` is expected
    to already be hashed by the time this model is constructed for storage.
    """

    id: str = Field(default_factory=lambda: uuid4().hex)
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Public-facing representation of a user, safe to return from the API (no password)."""

    id: str
    username: str
    email: EmailStr
