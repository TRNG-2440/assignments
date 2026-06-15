from datetime import datetime
from typing import Optional

from custom_exceptions import InvalidInputError


def try_cast_to_int(prompt: str) -> Optional[int]:
    """
    Prompt the user for input and attempt to convert it to an integer.

    Args:
        prompt: The message to display to the user.

    Returns:
        The integer value if conversion is successful, None if a ValueError occurs.
    """
    input_str: str = input(prompt)
    try:
        return int(input_str)
    except ValueError as e:
        raise InvalidInputError(f"Error encountered while converting to int: {e}")


def parse_start_datetime(date_str: str, time_str: str) -> datetime:
    """Combine a date string and a time string into a single `datetime`.

    Args:
        date_str: A date in "YYYY-MM-DD" format.
        time_str: A time in "HH:MM" format.

    Returns:
        A `datetime` combining the given date and time.

    Raises:
        ValueError: If either `date_str` or `time_str` is not in the
            expected format.
    """
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
