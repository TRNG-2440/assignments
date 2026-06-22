import json
from json import JSONDecodeError

FILE_PATH = "data/garden_db.json"

def read_data():
    """
        reads data using json.load() and returns list 
        - JSONDecodeError returns empty list
        - FileNotFoundError outpus no file found and returns empty list 
    """
    data = []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except JSONDecodeError:
        return data
    except FileNotFoundError as e:
        print(f"no file found at {FILE_PATH}")

    return data

def write_data(json_data):
    """
        writes data to file location using json.dump()
    """
    try:
        with open(FILE_PATH, "x", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
    except FileExistsError:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
            