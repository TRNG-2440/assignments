from fastapi import FastAPI
from routers import user_router, workout_router

app = FastAPI()

app.include_router(user_router)
app.include_router(workout_router)