import json
from json import JSONDecodeError

FILE_PATH = "data/garden_db.json"

def read_data():
    data = []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except JSONDecodeError:
        return data
    except FileNotFoundError as e:
        print(f"no file found at {FILE_PATH}")

    return data
#   - check if the file exists at the given path
#   - if it does not exist, return an empty list
#   - if it does, open it and load the contents as JSON
#   - return the loaded data

def write_data(json_data):
    try:
        with open(FILE_PATH, "x", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
    except FileExistsError:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
                
#   - open the file at the given path in write mode
#   - serialise 'data' as JSON and write it to the file