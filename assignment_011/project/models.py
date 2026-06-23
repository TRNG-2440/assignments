from pydantic import BaseModel

class UserCreate(BaseModel):
    user_id: int
    user_name: str

class UserProfile(BaseModel):
    api_key: str
    user_id: int
    user_name: str
    workout_count: int
    admin: bool

class WorkoutCreate(BaseModel):
    exercise_name: str
    sets: int
    reps: int
    weight: float

class Workout(BaseModel):
    workout_id: int
    user_id: int
    exercise_name: str
    sets: int
    reps: int
    weight: float