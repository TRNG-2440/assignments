"""Repository layer for reading and writing user records to a JSON-backed store."""

import os

from dotenv import load_dotenv

from models.users import UserDAO
from exceptions.auth import FilePathNotSpecifiedError, UserDoesNotExistError
from utils import append_record_to_json, read_json_file

load_dotenv()


class UsersRepository:
    """Data-access layer for user records, backed by a flat JSON file.

    The file path and the key under which the user list is stored are read
    from the USERS_DATA and USERS_DATA_KEY environment variables.
    """

    def __init__(self):
        """Load storage configuration from environment variables."""
        self._file_path = os.getenv("USERS_DATA")
        self._key = os.getenv("USERS_DATA_KEY")

    def check_unique_user(self, username: str, email: str) -> bool:
        """
        Checks whether a username and email are both available (not already taken).

        :param username: Candidate username to check.
        :param email: Candidate email to check.
        :return: True if neither the username nor the email is already in use.
        :raises FilePathNotSpecifiedError: If storage location is not configured.
        """
        if self._file_path and self._key:
            all_users: list[dict] = read_json_file(self._file_path, self._key)
            has_username = any(
                user for user in all_users if user.get("username") == username
            )
            has_email = any(user for user in all_users if user.get("email") == email)
            return not (has_email or has_username)
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for USERS_DATA not specified!"
            )

    def create_user(self, user: UserDAO) -> None:
        """
        Persists a new user record to the JSON store.

        :param user: The fully-populated user (with hashed password) to store.
        :raises FilePathNotSpecifiedError: If storage location is not configured.
        """
        if self._file_path and self._key:
            append_record_to_json(self._file_path, self._key, user.model_dump_json())
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for USERS_DATA or key not specified!"
            )

    def get_user(self, username: str) -> UserDAO:
        """
        Looks up a single user by username.

        :param username: The username to search for.
        :return: The matching user record.
        :raises FilePathNotSpecifiedError: If storage location is not configured.
        :raises UserDoesNotExistError: If no user with that username exists.
        """
        if self._file_path and self._key:
            all_users: list[dict] = read_json_file(self._file_path, self._key)
            filtered_users: list[dict] = [
                user for user in all_users if user.get("username") == username
            ]
            if filtered_users:
                return UserDAO.model_validate(filtered_users[0])
            else:
                raise UserDoesNotExistError(username=username)
        else:
            raise FilePathNotSpecifiedError(
                detail="File path for USERS_DATA not specified!"
            )
