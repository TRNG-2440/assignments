from fastapi import FastAPI
from routers import router


app = FastAPI(
    title = "Workout Log API",
    description = "A FastAPI project for tracking exercise sessions using JSON file persistence.",
    version = "1.0.0"
)


app.include_router(router)