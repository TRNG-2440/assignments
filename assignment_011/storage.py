# JSON file read/write helpers
import json
from pathlib import Path
from typing import Any

# Declare file path where json files are stored
DATA_PATH = Path(__file__).parent / "Data"

# Declare file path of recipe file in JSON format
RECIPE_PATH = DATA_PATH / "recipes.json"

# Declare file path of JSON meal plan file in JSON format
MEAL_PLAN_PATH = DATA_PATH / "mealPlans.json"

# Extract data from a json file into data structure
def readFile(filePath: Path) -> list[dict[str, Any]]:
    
    # If file does not exist return empty list
    if not filePath.exists():
        return []
    
    # If file exists then convert from JSON to python readable format
    else:
        
        # Open file, then convert content from JSON to python readable format
        with filePath.open("r", encoding = "utf-8") as file:
            return json.load(file)
        
# output criteria from data structure into file using JSON format
def writeFile(filePath: Path, data: list[dict[str,Any]]) -> None:
      
      # Ensure parent folder (Data) exists.  If not, create new copy
      filePath.parent.mkdir(parents=True, exist_ok=True)

      # # Open file, then convert content from python readable format to JSON
      with filePath.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)




