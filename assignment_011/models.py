from pydantic import BaseModel, Field
from datetime import date, datetime


class WellnessCreate(BaseModel):
    date: date
    sleep_hours: float = Field(ge=0, le=24)
    water_intake: int = Field(ge=0, le=1000)
    exercise_time: int = Field(ge=0, le=1000)
    notes: str = Field(max_length=1000)


class WellnessUpdate(BaseModel):
    date: date
    sleep_hours: float = Field(ge=0, le=24)
    water_intake: int = Field(ge=0, le=1000)
    exercise_time: int = Field(ge=0, le=1000)
    notes: str = Field(max_length=1000)

class WellnessResponse(BaseModel):
    id: str
    created_at: datetime
    date: date
    sleep_hours: float
    water_intake: int
    exercise_time: int
    notes: str


class WellnessSummary(BaseModel):
    total_entries: int
    best_sleep: float
    worst_sleep: float
    average_sleep: float
    average_water_intake: float
    average_exercise: float