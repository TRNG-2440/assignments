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


def try_cast_to_float(prompt: str) -> Optional[float]:
    """
    Prompt the user for input and attempt to convert it to a float.

    Args:
        prompt: The message to display to the user.

    Returns:
        The float value if conversion is successful, None if a ValueError occurs.
    """
    input_str: str = input(prompt)
    try:
        return float(input_str)
    except ValueError as e:
        raise InvalidInputError(f"Error encountered while converting to int: {e}")
