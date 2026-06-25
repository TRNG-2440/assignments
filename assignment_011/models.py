# Define schema criteria

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

# --------------- Enums ---------------

# Enum - day of week 
class DAY(str, Enum):
  MONDAY = "Monday"
  TUESDAY = "Tuesday"
  WEDNESDAY = "Wednesday"
  THURSDAY = "Thursday"
  FRIDAY = "Friday"
  SATURDAY = "Saturday"
  SUNDAY = "Sunday"

# Enum - type of meal
class MEAL(str, Enum):
  BREAKFAST = "Breakfast"
  LUNCH = "Lunch"
  DINNER = "Dinner"
  DESSERT = "Dessert"

# ------- Ingredient Models ------- 

# Ingredient used in each meal
class Ingredient(BaseModel):
  ingredient_name: str
  measurement: Optional[str]
  notes: Optional[str]

# Meal instructions
class Instructions(BaseModel):
  name: str
  instructions: str

# ------- Recipe Models ------- 

# Produce recipe
class CreateRecipe(BaseModel):
  name: str
  ingredients: list[Ingredient]
  instructions: Optional[str] = None

# Update each recipe
class UpdateRecipe(BaseModel):
  name: Optional[str] = None
  ingredients: Optional[list[Ingredient]] = None
  instructions: Optional[str] = None

# Response of each recipe
class RecipeResponse(BaseModel):
  recipe_id: str
  name: str
  ingredients: list[Ingredient]
  instructions: Optional[str] = None

# ------- Meal Plan Models ------- 

# Produce meal plan
class CreateMealPlan(BaseModel):
  name: str
  recipe_id: str
  day: DAY
  meal: MEAL

# Update meal plan
class UpdateMealPlan(BaseModel):
  name: str
  day: Optional[DAY]
  meal: Optional[MEAL]

# Response of each meal plan
class MealPlanResponse(BaseModel):
  name: str
  recipe_id: Optional[str]
  day: DAY
  meal: MEAL

  


