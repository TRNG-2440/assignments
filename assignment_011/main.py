from fastapi import FastAPI
from routers import recipeRouter, mealPlanRouter

# Declare instance of FastAPI
app = FastAPI(title="Meal Planner API", version="1.0.0")

# Implement router of recipe api's
app.include_router(recipeRouter)

# Implement router of meal plan api's
app.include_router(mealPlanRouter)

# Route declarator
@app.get("/status")
def Status():
    return {"status": "ok"}

 