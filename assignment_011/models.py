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
  name: str
  quantity: float
  unit: str
  amount: str

# Meal instructions
class Instructions(BaseModel):
  name: str
  instructions: str

# ------- Recipe Models ------- 

# Produce recipe
class CreateRecipe(BaseModel):
  name: str
  created_at: datetime
  ingredients: list[Ingredient]
  instructions: Optional[str] = None
  servings: int

# Update each recipe
class UpdateRecipe(BaseModel):
  name: Optional[str] = None
  ingredients: Optional[list[Ingredient]] = None
  instructions: Optional[str] = None
  servings: Optional[int] = None

# Response of each recipe
class RecipeResponse(BaseModel):
  recipe_id: str
  name: str
  created_at: datetime
  day: DAY
  meal: MEAL
  ingredients: list[Ingredient]
  instructions: Optional[str] = None
  servings: int
  
# ------- Meal Plan Models ------- 

# Produce meal plan
class CreateMealPlan(BaseModel):
  name: str
  meal_id: str
  recipe_id: str
  created_at: datetime
  day: DAY
  meal: MEAL

# Update meal plan
class UpdateMealPlan(BaseModel):
  name: str
  meal_id: Optional[str]
  created_at: datetime
  day: Optional[DAY]
  meal: Optional[MEAL]

# Response of each meal plan
class MealPlanResponse(BaseModel):
  name: str
  meal_id: str
  recipe_id: Optional[str]
  created_at: datetime
  day: DAY
  meal: MEAL

# ------- List Models ------- 

# List of all meals combined
class ShoppingList(BaseModel):
  total_meals: int
  meals: list[CreateMealPlan]
  ingredients: list[Ingredient]


