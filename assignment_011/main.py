# Mark White
# 06/19/2026
# FastAPI Wellness Tracker

# This app will track daily wellness metrics including sleep, water intake, and exercise.
# It will allow users to create, read, update, and delete wellness entries.
# It will also provide a summary of the wellness data.

from fastapi import FastAPI
from routers.wellness import router as wellness_router

app = FastAPI(
    title="Wellness Tracker API",
    description="Track daily wellness metrics including sleep, water intake, and exercise.",
    version="1.0.0"
)

app.include_router(wellness_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Wellness Tracker API",
        "status": "Running"
    }