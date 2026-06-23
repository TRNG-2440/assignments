"""
Models
"""
# dependencies
from pydantic import BaseModel, Field
from typing import Optional

# -- Pydantic Models --
# request model for movie
class MovieCreate(BaseModel):
    title: str = Field(min_length = 1, max_length = 100)
    status: str
    rating: float | None
    genre: str

# response model for movie
class MovieResponse(BaseModel):
    id: str
    title: str
    status: str
    rating: float | None
    genre: str

# partial update model - all fields optional
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    rating: Optional[float] = None
    genre: Optional[str] = None