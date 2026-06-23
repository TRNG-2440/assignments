from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jsonDataStore import JsonRepository
from models import UserProfile, Workout, UserCreate, WorkoutCreate
from typing import Optional

repository = JsonRepository()


# AUTH

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserProfile:
    api_key = credentials.credentials
    users = repository.get_users()
    for user in users:
        if user.api_key == api_key:
            return user
    raise HTTPException(status_code=401, detail="Invalid API key")

# USERS

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.get("/")
def get_users(current_user: UserProfile = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return repository.get_users()

@user_router.get("/{user_id}")
def get_user(user_id: int, current_user: UserProfile = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return repository.get_user(user_id)

@user_router.post("/")
def create_user(user: UserCreate):
    new_user = UserProfile(
        user_id=user.user_id,
        user_name=user.user_name,
        admin=False, # This defaults to false. To become admin, edit json directly
        workout_count=0,
        api_key=""  # overwritten in repo
    )
    try:
        return repository.create_user(new_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.put("/")
def update_user(user: UserProfile, current_user: UserProfile = Depends(get_current_user)):
    # AuthZ: must be self or admin
    if not current_user.admin and current_user.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    success = repository.update_user(user)
    return {"success": success}


@user_router.delete("/{user_id}")
def delete_user(user_id: int, current_user: UserProfile = Depends(get_current_user)):
    # AuthZ: must be self or admin
    if not current_user.admin and current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    success = repository.delete_user(user_id)
    return {"success": success}

# WORKOUTS

workout_router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)

@workout_router.get("/")
def get_workouts(current_user: UserProfile = Depends(get_current_user)):
    all_workouts = repository.get_workouts()
    return [w for w in all_workouts if w.user_id == current_user.user_id]

@workout_router.post("/")
def create_workout(
    workout: WorkoutCreate, current_user: UserProfile = Depends(get_current_user)):
    new_workout = Workout(
        workout_id=0,  # overwritten in repository
        user_id=current_user.user_id,
        exercise_name=workout.exercise_name,
        sets=workout.sets,
        reps=workout.reps,
        weight=workout.weight
    )
    return repository.create_workout(new_workout)

@workout_router.put("/")
def update_workout(workout: Workout, current_user: UserProfile = Depends(get_current_user)):
    existing = repository.get_workout(workout.workout_id)
    if not existing:
        return {"success": False}
    if not current_user.admin and existing.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    repository.update_workout(workout)
    return {"success": True}

@workout_router.delete("/{workout_id}")
def delete_workout(workout_id: int, current_user: UserProfile = Depends(get_current_user)):
    workout = repository.get_workout(workout_id)
    if not workout:
        return {"success": False}
    if not current_user.admin and workout.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    repository.delete_workout(workout_id)
    return {"success": True}