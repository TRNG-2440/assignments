"""
Connected to data directory to save data for API
"""
# dependencies 
import json
from pathlib import Path

# path to data file
DATA_FILE = Path(__file__).parent / "data" / "movie_watchlist.json"

# read data from movie_watchlist.json
def read_data(filepath: str) -> dict:
    # file potentially might not exist, return empty dict
    if not DATA_FILE.exists():
        return {}
    
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return {}

# write data into movie_watchlist.json
def write_data(filepath: str, data):
    # Ensure the data/ directory exists before writing
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent = 2)