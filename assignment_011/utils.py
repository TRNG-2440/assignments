"""General-purpose helpers for JSON-backed storage and password hashing."""

import json
from pathlib import Path
from typing import Any, List, Union

import bcrypt

from enum import Enum

from logger import logger


class Currency(Enum):
    symbol: str  # currency symbol
    # Members definition: CODE = (CODE, SYMBOL)
    USD = ("USD", "$")
    EUR = ("EUR", "€")
    GBP = ("GBP", "£")
    JPY = ("JPY", "¥")
    CHF = ("CHF", "CHF")
    AUD = ("AUD", "A$")
    CAD = ("CAD", "C$")
    CNY = ("CNY", "¥")
    INR = ("INR", "₹")
    MXN = ("MXN", "$")
    BRL = ("BRL", "R$")
    KRW = ("KRW", "₩")
    SGD = ("SGD", "S$")
    HKD = ("HKD", "HK$")
    NOK = ("NOK", "kr")
    SEK = ("SEK", "kr")
    DKK = ("DKK", "kr")
    NZD = ("NZD", "NZ$")
    ZAR = ("ZAR", "R")
    RUB = ("RUB", "₽")
    TRY = ("TRY", "₺")
    PLN = ("PLN", "zł")
    THB = ("THB", "฿")
    IDR = ("IDR", "Rp")
    MYR = ("MYR", "RM")
    PHP = ("PHP", "₱")
    CZK = ("CZK", "Kč")
    ILS = ("ILS", "₪")
    AED = ("AED", "د.إ")
    SAR = ("SAR", "﷼")

    def __new__(cls, code: str, symbol: str):
        obj = object.__new__(cls)
        obj._value_ = code  # Sets .value to the string code
        obj.symbol = symbol  # Sets .symbol to currency symbol
        return obj


def read_json_file(file_path: Union[str, Path], key: str) -> Any:
    """
    Safely reads and parses data from a JSON file.

    Expects the top-level JSON object to contain `key`, whose value is a
    list of JSON-encoded strings (each re-parsed individually via
    `json.loads`).

    :param file_path: Path to the JSON file (str or Path object).
    :param key: The top-level key whose list value should be read and decoded.
    :return: Parsed Python data structure (usually a list of dicts), or None
        if the file is empty/falsy.
    :raises FileNotFoundError: If the file does not exist.
    :raises json.JSONDecodeError: If the file or an individual record is not valid JSON.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if data:
                # Pull out the list stored under `key`.
                data = data.get(key)
                # Each entry is itself a JSON string, so decode it individually.
                return [json.loads(item) for item in data]

    except FileNotFoundError:
        logger.error(f"Error: The file at {file_path} was not found.")
        raise
    except json.JSONDecodeError as e:
        logger.error(
            f"Error: Failed to decode JSON. Invalid syntax on line {e.lineno}, col {e.colno}."
        )
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise


def append_record_to_json(
    file_path: Union[str, Path], key: str, new_record: Any
) -> None:
    """
    Appends a record to an array inside a JSON file containing a specific key.
    Creates a new file if it does not exist.

    :param file_path: Path to the target JSON file.
    :param key: The dictionary key where the array is stored.
    :param new_record: The data item to append to the array.
    :raises json.JSONDecodeError: If the existing file contains invalid JSON.
    :raises TypeError: If the value currently stored under `key` is not a list.
    """
    path = Path(file_path)
    data = {}

    # Read existing data if the file exists
    if path.exists() and path.stat().st_size > 0:
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error: Existing file contains invalid JSON ({e}).")
            raise

    # Ensure the key exists and points to a list
    if key not in data:
        data[key] = []
    elif not isinstance(data[key], list):
        raise TypeError(
            f"The value for key '{key}' is a {type(data[key])}, not a list."
        )

    # Append the new record to the list
    data[key].append(new_record)

    # Write back to the file
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def append_records_to_json(
    file_path: Union[str, Path], key: str, new_records: List[Any]
) -> None:
    """
    Appends multiple records to an array inside a JSON file containing a specific key.
    Creates a new file if it does not exist.

    :param file_path: Path to the target JSON file.
    :param key: The dictionary key where the array is stored.
    :param new_records: A list of data items to append to the array.
    :raises json.JSONDecodeError: If the existing file contains invalid JSON.
    :raises TypeError: If the value currently stored under `key` is not a list.
    """
    path = Path(file_path)
    data = {}

    # Read existing data if the file exists
    if path.exists() and path.stat().st_size > 0:
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            logger.error(f"Error: Existing file contains invalid JSON ({e}).")
            raise

    # Ensure the key exists and points to a list
    if key not in data:
        data[key] = []
    elif not isinstance(data[key], list):
        raise TypeError(
            f"The value for key '{key}' is a {type(data[key])}, not a list."
        )

    # Extend the list with the multiple new records
    data[key].extend(new_records)

    # Write back to the file
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def write_all_records_to_json(
    file_path: Union[str, Path], key: str, records: List[Any]
) -> None:
    path = Path(file_path)
    data = {}
    data[key] = records
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def hash_password(password: str) -> str:
    """Hashes a plaintext password using a randomly generated salt."""
    # Convert plaintext string to bytes
    pwd_bytes = password.encode("utf-8")

    # Generate a salt (bcrypt embeds the salt in the resulting hash)
    salt = bcrypt.gensalt()

    # Hash the password
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)

    return hashed_bytes.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a stored bcrypt hash string."""
    # Convert inputs back to bytes
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_bytes)
