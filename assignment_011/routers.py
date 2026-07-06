# Endpoint definitions
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from auth import VerifyUser
from models import CreateRecipe, RecipeResponse, UpdateRecipe, CreateMealPlan, MealPlanResponse, UpdateMealPlan
from storage import RECIPE_PATH, MEAL_PLAN_PATH, readFile, writeFile

# Declare router object
recipeRouter = APIRouter(tags=["Recipes"])

mealPlanRouter = APIRouter(tags=["MealPlan"])

# -----------------------------------------------------------------------------
# POST route decerator - Create new recipe
@recipeRouter.post("/recipes", 
  response_model = RecipeResponse,
  status_code = status.HTTP_201_CREATED,
  summary = "Create new recipe",
  description = "Add new recipe",
  responses =
  {
    401: {"description": "Unauthorized — invalid credentials"},
    422: {"description": "Validation error — request body did not match schema"},
  },
)

# Controller function - Create recipe
def Create_Recipe(
    
    # Object derived from model
    recipe: CreateRecipe,
    
    # User name obtained through verification process in auth.py
    username: str = Depends(VerifyUser),
):
    # Read JSON text from file
    recipeFile = readFile(RECIPE_PATH)

    # Declare recipe dictionary
    recipeDict = {
      "recipe_id": str(uuid.uuid4()),
      "name": recipe.name,
      "created_at": datetime.now().isoformat(),
      "ingredients": [i.model_dump() for i in recipe.ingredients],
      "instructions": recipe.instructions,
    }

    # Insert recipe dictionary to file object
    recipeFile.append(recipeDict)

    # Output recipe dictionary to recipes.json
    writeFile(RECIPE_PATH, recipeFile)
    
    return recipeDict

# -----------------------------------------------------------------------------
# GET route decerator - Read all recipes
@recipeRouter.get("/recipes", 
                  
  # Declare list through RecipeResponse model               
  response_model = list[RecipeResponse],

  # Verify status code
  status_code = status.HTTP_200_OK,

  # Declare summary
  summary = "Retreive all recipes",

  # Declare description
  description = "Retreive all recipes current on file",

  # Declare response status codes
  responses=
  {
      
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipes not found"},
  },
    )

# Controller function - retreive all recipes
def Get_All_Recipes(
    
    # User name obtained through verification process in auth.py
    username: str = Depends(VerifyUser),
):
    # Return file object of recipes.json
    return readFile(RECIPE_PATH)

# -----------------------------------------------------------------------------
# GET route decorator - Read specific receipe by recipe_id
@recipeRouter.get("/recipes/{recipe_id}",
                  
    response_model = RecipeResponse,

    status_code = status.HTTP_200_OK,

    summary="Retrieve one recipe",

    description="Retreive a single recipe after user inputs their recipe_id.",

    responses={
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipe not found"},
    },
)

# Retreive a specific recipe through recipe_id
def Get_Single_Recipe(
    
    recipe_id: str,

    username: str = Depends(VerifyUser),
):
    
    recipeFile = readFile(RECIPE_PATH)

    # Search for recipe in file
    for recipe in recipeFile:
        if recipe["recipe_id"] == recipe_id:
            return recipe

    # Throw excepption if recipe is not found
    raise HTTPException(
        
        status_code=status.HTTP_404_NOT_FOUND,

        detail=f"Recipe with id {recipe_id} not found",
    )

# -----------------------------------------------------------------------------
# PUT route decorator - modify single receipe by recipe_id
@recipeRouter.put("/recipes/{recipe_id}",
                  
    response_model = RecipeResponse,

    summary="Update recipe",

    description="Modify a single recipe through recipe_id.",

    responses={
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipe not found"},
    },
)

# Retreive a specific recipe through recipe_id
def Update_Recipe(
    
    recipe_id: str,

    updates: UpdateRecipe,

    username: str = Depends(VerifyUser),
):
    
    # Declare file object through recipes.json
    recipeFile = readFile(RECIPE_PATH)

    # Search for recipe in file
    for recipe in recipeFile:
        if recipe["recipe_id"] == recipe_id:

          # Updated data inputted by user
          updateData = updates.model_dump(exclude_unset=True)

          # Recplace pre-existing content with updated data
          for key, value in updateData.items():
            recipe[key] = value

          # Output content to recipes.json
          writeFile(RECIPE_PATH, recipeFile)

          return recipe

    # Throw excepption if recipe is not found
    raise HTTPException(
        
        status_code=status.HTTP_404_NOT_FOUND,

        detail=f"Recipe with id {recipe_id} not found",
    )

# -----------------------------------------------------------------------------
# DELETE route decorator - remove record by id
@recipeRouter.delete(
    "/recipes/{recipe_id}",
    
    summary="Delete recipe",

    description="Delete a single recipe through recipe_id.",

    responses={
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipe not found"},
    },
  )
def Delete_Recipe(

    recipe_id: str,

    username: str = Depends(VerifyUser),
    
):
     # Declare file object through recipes.json
    recipeFile = readFile(RECIPE_PATH)

    # Declare boolean value to determine if entry has been found
    isFound = False
    
     # Search for recipe in file
    for i, recipe in enumerate(recipeFile):
        if recipe["recipe_id"] == recipe_id:
            
            # Delete entry
            recipeFile.pop(i)

            isFound = True

            break
    
    if(isFound):
        writeFile(RECIPE_PATH,recipeFile)

        return {"message": f"Recipe {recipe_id} has been successfully deleted."}


    # Throw excepption if recipe is not found
    raise HTTPException(
        
        status_code=status.HTTP_404_NOT_FOUND,

        detail=f"Recipe with id {recipe_id} not found",
    )
# -----------------------------------------------------------------------------
# POST route decerator - Create new mealplan
@mealPlanRouter.post("/mealPlan", 
                     
  response_model = MealPlanResponse,

  status_code = status.HTTP_201_CREATED,

  summary = "Create new meal plan",

  description = "Add new meal plan",

  responses =
  {
    401: {"description": "Unauthorized — invalid credentials"},
    422: {"description": "Validation error — request body did not match schema"},
  },
)

# Controller function - Create recipe
def Create_Meal_Plan(
    
    # Object derived from model
    meal_plan: CreateMealPlan,
    
    # User name obtained through verification process in auth.py
    username: str = Depends(VerifyUser),
):
    # Read JSON text from file
    mealPlanFile = readFile(MEAL_PLAN_PATH)

    # Open file for recipe path
    recipeFile = readFile(RECIPE_PATH)

    # Recipe list
    recipe = None

    # Traverse through recipe to find name of meal
    for r in recipeFile:
      if r["recipe_id"] == meal_plan.recipe_id:
        recipe = r
        break

    if recipe is None:
      raise HTTPException(status_code=404, detail="Recipe not found")

    # Declare recipe dictionary
    mealPlanDict = {
      "name": meal_plan.name,
      "recipe": recipe,
      "meal_id": str(uuid.uuid4()),
      "recipe_id": meal_plan.recipe_id,
      "created_at": datetime.now().isoformat(),
      "day": meal_plan.day.value,
      "meal": meal_plan.meal.value,
    }

    # Insert recipe dictionary to file object
    mealPlanFile.append(mealPlanDict)

    # Output recipe dictionary to recipes.json
    writeFile(MEAL_PLAN_PATH, mealPlanFile)

    return mealPlanDict
# -----------------------------------------------------------------------------
# GET route decerator - Read all meal plans
@mealPlanRouter.get("/mealPlan", 
             
  response_model = list[MealPlanResponse],

  status_code = status.HTTP_200_OK,

  summary = "Retreive all meal plan",

  description = "Retreive all meal plans on current file",

  responses =
  {
    401: {"description": "Unauthorized — invalid credentials"},
    422: {"description": "Validation error — request body did not match schema"},
  },
)

# Controller function - Create recipe
def Get_All_Meal_Plans(
    
    # User name obtained through verification process in auth.py
    username: str = Depends(VerifyUser),
):

    return readFile(MEAL_PLAN_PATH)
# -----------------------------------------------------------------------------
# GET route decerator - Read specific meal plan by meal_id
@mealPlanRouter.get("/mealPlan/{meal_id}", 
            
  response_model = MealPlanResponse,

  status_code = status.HTTP_200_OK,

  summary = "Retreive all one meal plan",

  description = "Retreive a single meal plan after user inputs their meal plan id.",

  responses =
  {
    401: {"description": "Unauthorized — invalid credentials"},

    422: {"description": "Validation error — request body did not match schema"},
  },
)

# Controller function - Create recipe
def Get_Single_Meal_Plan(
    
    # Declare meal_id
    meal_id: str,
    
    # User name obtained through verification process in auth.py
    username: str = Depends(VerifyUser),
):

    # Declare file object
    mealFile = readFile(MEAL_PLAN_PATH)

    # Search for recipe in file
    for meal in mealFile:
        if meal["meal_id"] == meal_id:
            return meal

    # Throw excepption if recipe is not found
    raise HTTPException(
        
        status_code=status.HTTP_404_NOT_FOUND,

        detail=f"Meal plan id {meal_id} not found",)

# -----------------------------------------------------------------------------
# PUT route decorator - modify single receipe by recipe_id
@mealPlanRouter.put("/mealPlan/{meal_id}",
                  
    response_model = MealPlanResponse,

    summary="Update meal plan",

    description="Modify a single meal plan through meal_id.",

    responses={
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipe not found"},
    },
)

# Update a specific meal plan through meal_id
def Update_Meal_Plan(
    
    meal_id: str,

    updates: UpdateMealPlan,

    username: str = Depends(VerifyUser),
):
    
    # Declare file object through recipes.json
    mealFile = readFile(MEAL_PLAN_PATH)

    # Search for recipe in file
    for meal in mealFile:
        if meal["meal_id"] == meal_id:

          # Updated data inputted by user
          updateData = updates.model_dump(exclude_unset=True)

          # Recplace pre-existing content with updated data
          for key, value in updateData.items():
            meal[key] = value

          # Output content to recipes.json
          writeFile(MEAL_PLAN_PATH, mealFile)

          return meal

    # Throw excepption if recipe is not found
    raise HTTPException(
        
        status_code=status.HTTP_404_NOT_FOUND,

        detail=f"Meal Plan with id {meal_id} not found",
    )

# -----------------------------------------------------------------------------
# DELETE route decorator - remove record by id
@mealPlanRouter.delete(
    "/mealPlan/{meal_id}",
    
    summary = "Delete meal plan",

    description = "Delete a single meal plan through meal_id.",

    responses={
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipe not found"},
    },
  )

def Delete_Meal_Plan(
    
    meal_id: str,

    username: str = Depends(VerifyUser),
    
):
     # Declare file object through mealPlans.json
    mealFile = readFile(MEAL_PLAN_PATH)

    # Declare boolean value to determine if entry has been found
    isFound = False
    
     # Search for recipe in file
    for i, meal in enumerate(mealFile):
        if meal["meal_id"] == meal_id:
            
            # Delete entry
            mealFile.pop(i)

            isFound = True

            break
    
    if(isFound):
        writeFile(MEAL_PLAN_PATH,mealFile)

        return {"message": f"Meal plan {meal_id} has been successfully deleted.\n"}


    # Throw excepption if recipe is not found
    raise HTTPException(
        
        status_code=status.HTTP_404_NOT_FOUND,

        detail=f"Meal plan id {meal_id} not found",
    )