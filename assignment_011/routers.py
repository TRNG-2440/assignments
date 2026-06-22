# Endpoint definitions
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from auth import VerifyUser
from models import CreateRecipe, RecipeResopnse, UpdateRecipe, CreateMealPlan, MealPlanResponse, UpdateMealPlan
from storage import RECIPE_PATH, MEAL_PLAN_PATH, readFile, writeFile

# Declare router object
recipeRouter = APIRouter(tags=["Recipes"])

mealPlanRouter = APIRouter(tags=["MealPlan"])

# -----------------------------------------------------------------------------
# POST route decerator - Create new recipe
@recipeRouter.post("/recipes", 
  response_model = RecipeResopnse,
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
      "created_at": recipe.created_at.isoformat(),
      "ingredients": [i.model_dump() for i in recipe.ingredients],
      "instructions": recipe.instructions,
      "servings": recipe.servings,
    }

    # Insert recipe dictionary to file object
    recipeFile.append(recipeDict)

    # Output recipe dictionary to recipes.json
    writeFile(RECIPE_PATH, recipeFile)
    return recipeDict

# -----------------------------------------------------------------------------
# GET route decerator - Read all recipes
@recipeRouter.get("/recipes", 
                  
  # Declare list through RecipeResopnse model               
  response_model = list[RecipeResopnse],

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
                  
    # Declare response_model object
    response_model = RecipeResopnse,

    # Verify status code
    status_code = status.HTTP_200_OK,

    # Declare summary 
    summary="Retrieve one recipe",

     # Declare description
    description="Retreive a single recipe after user inputs their recipe_id.",

     # Declare response for status code
    responses={
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipe not found"},
    },
)

# Retreive a specific recipe through recipe_id
def Get_Single_Recipe(
    
    # Declare recipe_id
    recipe_id: str,

    # Declare username
    username: str = Depends(VerifyUser),
):
    
    # Declare file object
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
                  
    # Declare response_model object
    response_model = RecipeResopnse,

    # Declare summary 
    summary="Update recipe",

     # Declare description
    description="Modify a single recipe through recipe_id.",

     # Declare response for status code
    responses={
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipe not found"},
    },
)

# Retreive a specific recipe through recipe_id
def Update_Recipe(
    
    # Declare response_id
    recipe_id: str,

    updates: UpdateRecipe,

    # Declare username
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
    
    # Declare summary 
    summary="Delete recipe",

     # Declare description
    description="Delete a single recipe through recipe_id.",

     # Declare response for status code
    responses={
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipe not found"},
    },
  )
def Delete_Recipe(
    
     # Declare response_id
    recipe_id: str,

    # Declare username
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

        return {"\nMessage": f"Recipe {recipe_id} has been successfully deleted.\n"}


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

    # Declare recipe dictionary
    mealPlanDict = {
      "meal_id": meal_plan.meal_id,
      "created_at": meal_plan.created_at.isoformat(),
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

  # Declare list through RecipeResopnse model                 
  response_model = list[MealPlanResponse],

  # Verify status code
  status_code = status.HTTP_200_OK,

  # Declare summary
  summary = "Retreive all meal plan",

  # Declare description
  description = "Retreive all meal plans on current file",

  # Declare repsonse status codes
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

  # Declare list through RecipeResopnse model                 
  response_model = MealPlanResponse,

  # Verify status code
  status_code = status.HTTP_200_OK,

  # Declare summary
  summary = "Retreive all one meal plan",

  # Declare description
  description = "Retreive a single meal plan after user inputs their meal plan id.",

  # Declare repsonse status codes
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
                  
    # Declare response_model object
    response_model = MealPlanResponse,

    # Declare summary 
    summary="Update meal plan",

     # Declare description
    description="Modify a single meal plan through meal_id.",

     # Declare response for status code
    responses={
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipe not found"},
    },
)

# Update a specific meal plan through meal_id
def Update_Meal_Plan(
    
    # Declare response_id
    meal_id: str,

    updates: UpdateMealPlan,

    # Declare username
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
    
    # Declare summary 
    summary = "Delete meal plan",

     # Declare description
    description = "Delete a single meal plan through meal_id.",

     # Declare response for status code
    responses={
        401: {"description": "Unauthorized — invalid credentials"},

        404: {"description": "Recipe not found"},
    },
  )

def Delete_Meal_Plan(
    
     # Declare response_id
    meal_id: str,

    # Declare username
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