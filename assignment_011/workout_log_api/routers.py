from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from datetime import datetime
import uuid

from models import WorkoutCreate, WorkoutUpdate, WorkoutResponse
from storage import read_data, write_data
from auth import verify_api_key


router = APIRouter()


WORKOUTS_FILE = "data/workouts.json"


@router.get(
    "/health", 
    summary = "Health Check",
    description = "Public endpoint to check that the API is running."
)

def health_check():
    return {"status": "API is running"}


@router.post(
    "/workouts",
    response_model = WorkoutResponse,
    status_code = status.HTTP_201_CREATED,
    summary = "Create a new workout",
    description = "Adds a new workout entry to the log. Requires API key authentication",
    responses = {
        403: {"desciption": "Invalid or missing API key"},
        422: {"description": "Validation error"}
    }
)

def create_workout(
    workout: WorkoutCreate,
    api_key : str = Depends(verify_api_key)
):
    workouts = read_data(WORKOUTS_FILE)

    new_workout = workout.model_dump()
    new_workout["id"] = str(uuid.uuid4())
    new_workout["created_at"] = datetime.now().isoformat()

    workouts.append(new_workout)
    write_data(WORKOUTS_FILE, workouts)

    return new_workout

#Adding a READ ALL endpoint

@router.get(
    "/workouts",
    response_model = list[WorkoutResponse],
    summary = "Get all workout",
    description = "Returns all workout entries. Can optionally filter by category or by exericise name.",
    responses ={
        403: {"description": "Invalid or missing APY key"}
    }
)

def get_workouts(
    category: Optional[str] = None,
    exercise_name: Optional[str] = Query(None),
    api_key: str = Depends(verify_api_key)
):
    workouts =read_data(WORKOUTS_FILE)

    if category:
        workouts = [
            workout for workout in workouts
            if workout["category"].lower() == category.lower()
        ]
    
    if exercise_name:
        workouts = [
            workout for workout in workouts
            if exercise_name.lower() in workout["exericise_name"].lower()
        ]
    return workouts


#Adding READ ONE endpoint

@router.get(
    "/workouts/{workout_id}",
    response_model = WorkoutResponse,
    summary = "Get one workout",
    description = "Returns a single workout by its ID",
    responses = {
        403: {"description": "Invalid or missing API key"},
        404: {"description": "Workout not found"}
    }
)

def get_workout(
    workout_id: str,
    api_key: str = Depends(verify_api_key)
):
    workouts = read_data(WORKOUTS_FILE)

    for workout in workouts:
        if workout["id"] == workout_id:
            return workout
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Workout not found"
    )

#UPDATE endpoint

@router.patch(
    "/workouts/{workout_id}",
    response_model= WorkoutResponse,
    summary = "Update a workout",
    description = "Updates one or more fields for existing workout entry",
    responses = {
        403: {"description": "Invalid or missing API key" },
        404: {"description": "Workout not found" },
        422: {"description": "Validation error" },
    }
)

def update_workout(
    workout_id: str,
    updated_workout: WorkoutUpdate,
    api_key: str = Depends(verify_api_key)
):
    workouts = read_data(WORKOUTS_FILE)
    
    for index, workout in enumerate(workouts):
        if workout["id"] == workout_id:
            update_data = updated_workout.model_dump(exclude_unset= True)
        
            workouts[index].update(update_data)
            write_data(WORKOUTS_FILE, workouts)

            return workouts[index]
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Workout not found"
    )

#DELETE endpoint

@router.delete(
    "/workouts/{workout_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Delete a workout",
    description = "Deletes a workout entry from the log by ID",
    responses = {
        403: {"description": "Invalid or missing API key"},
        404: {"description": "Workout not found"}
    }
)

def delete_workout(
    workout_id: str,
    api_key: str = Depends(verify_api_key)
):
    workouts = read_data(WORKOUTS_FILE)

    for workout in workouts:
        if workout["id"] == workout_id:
            workouts.remove(workout)
            write_data(WORKOUTS_FILE, workouts)
            return
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Workout not found"
    )

#SUMMARY Endpoint
@router.get(
    "/workouts/summary/stats",
    summary = "Get workout summary",
    description = "Returns summary statistics about the workout log.",
    responses = {
        403: {"description": "Invalid or missing API key"}
    }
)

def get_summary(api_key: str = Depends(verify_api_key)):

    workouts = read_data(WORKOUTS_FILE)

    total_workouts = len(workouts)
    total_sets = sum(workout["sets"] for workout in workouts)
    total_reps = sum(workout["sets"] * workout["reps"] for workout in workouts)

    weight_workouts = [
        workout for workout in workouts
        if workout.get("weight") is not None
    ]

    avg_weight = None

    if weight_workouts:
        avg_weight = sum(
            workout["weight"] for workout in weight_workouts
        )/len(weight_workouts)

    return {
        "total_workouts": total_workouts,
        "total_reps": total_reps,
        "total_sets": total_sets,
        "avg_weight": avg_weight
    }