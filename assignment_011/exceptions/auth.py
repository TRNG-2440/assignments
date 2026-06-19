"""Custom exception types used across the authentication and user-management flows."""


class AuthenticationError(Exception):
    """Raised when a login attempt fails because the username or password is incorrect."""

    def __init__(self, username: str, detail: str = "Incorrect username or password"):
        """
        :param username: The username that failed to authenticate.
        :param detail: Human-readable explanation of the failure.
        """
        self.username = username
        self.detail = detail


class InvalidPasswordError(Exception):
    """Raised when a candidate password does not meet the configured strength requirements."""

    def __init__(self, detail: str = "Invalid password"):
        """
        :param detail: Human-readable explanation of which requirement was not met.
        """
        self.detail = detail


class FilePathNotSpecifiedError(Exception):
    """Raised when the JSON file path/key used for user storage has not been configured."""

    def __init__(self, detail: str):
        """
        :param detail: Human-readable explanation of the missing configuration.
        """
        self.detail = detail


class UserAlreadyExistsError(Exception):
    """Raised when attempting to register a username or email that is already in use."""

    def __init__(self, username: str, email: str, detail: str = "User already exists!"):
        """
        :param username: The username that already exists.
        :param email: The email that already exists.
        :param detail: Human-readable explanation of the failure.
        """
        self.detail = detail
        self.username = username
        self.email = email


class UserDoesNotExistError(Exception):
    """Raised when a lookup is performed for a username that has no matching record."""

    def __init__(self, username: str, detail: str = "User does not exist!"):
        """
        :param username: The username that could not be found.
        :param detail: Human-readable explanation of the failure.
        """
        self.detail = detail
        self.username = username
