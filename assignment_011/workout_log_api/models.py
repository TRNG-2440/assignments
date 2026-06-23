#Models implementation for the workout log api

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class WorkoutCreate(BaseModel):
    exercise_name: str 
    category: str
    sets: Optional[int] = Field(None, ge=0)
    reps: Optional[int] = Field(None, ge=0)
    weight: Optional[float]
    duration_minutes: Optional[float]  = Field(None, ge=0, example=45)
    notes: Optional[str] = Field(None, example="Felt strong today")


class WorkoutUpdate(BaseModel):
    exercise_name: Optional[str]
    category: Optional[str]
    sets: Optional[int] = Field(None, ge=0)
    reps: Optional[int] = Field(None, ge=0)
    weight: Optional[float]
    duration_minutes: Optional[float]  = Field(None, ge=0, example=45)
    notes: Optional[str]


class WorkoutResponse(WorkoutCreate):
    id: str
    created_at: datetime

