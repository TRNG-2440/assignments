"""
Connected to data directory to save data for API
"""
# dependencies 
import json
from pathlib import Path

# path to data file
DATA_FILE = Path(__file__).parent / "data" / "movie_watchlist.json"

def read_data(filepath: Path = DATA_FILE) -> dict:
    # if file missing, fall back to empty file
    if not filepath.exists():
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def write_data(data: dict, filepath: Path = DATA_FILE) -> None:
    with open(filepath, "w") as f:
        json.dump(data, f, indent = 4)

def get_user_movies(username: str) -> list:
    data = read_data()
    return data.get(username, [])

def save_user_movies(username: str, movies: list) -> None:
    data = read_data()
    data[username] = movies
    write_data(data)