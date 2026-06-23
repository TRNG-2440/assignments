"""
Models
"""
# dependencies
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# -- Pydantic Models --
# request model for movie (client input only; id/created_at are server-generated)
class MovieCreate(BaseModel):
    title: str = Field(min_length = 1, max_length = 100)
    status: str
    rating: Optional[float] = None
    genre: str

# response model for movie
class MovieResponse(BaseModel):
    id: str
    title: str
    status: str
    rating: float | None
    genre: str
    created_at: datetime

# partial update model - all fields optional
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    rating: Optional[float] = None
    genre: Optional[str] = None
