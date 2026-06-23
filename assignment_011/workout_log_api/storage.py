
import json
import os


def read_data(filepath):
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, "r") as file:
        return json.load(file)
    

def write_data(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w") as file:
        json.dump(data, file, indent = 4, default = str)
