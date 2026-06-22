import json
import os

FILE_PATH = "data/mood.json"

def read_data():
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    
    if not os.path.exists(FILE_PATH):
        return []
    
    with open(FILE_PATH, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def write_data(data):

    try:
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except IOError:
        return False