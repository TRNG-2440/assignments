from pydantic import BaseModel, Field
from typing import Optional
from activity import Activity

class LogEntryCreate(BaseModel):
    activity: Activity
    description: str = Field(min_length=2, max_length=255)
    location: str = Field(min_length=1, max_length= 64)

class LogEntryResponse(BaseModel):
    id: str
    created_at: str
    activity: Activity
    description: str
    location: str

class LogEntryUpdate(BaseModel):
    activity: Optional[Activity] = None
    description: Optional[str] = None
    location: Optional[str] = None
