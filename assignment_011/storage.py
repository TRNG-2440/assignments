import json
import os



def read_data(file_path):
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, "r", encoding="utf-8") as file:
       try:
            return json.load(file)
       except json.JSONDecodeError:
            return []
        
def write_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)