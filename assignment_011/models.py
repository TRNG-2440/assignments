from pydantic import BaseModel, Field
from typing import Optional


class LogEntryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

class LogEntryResponse(BaseModel):
    id: int
    name: str

class LogEntryUpdate(BaseModel):
    name: Optional[str] = None
