"""
Models
"""
# dependencies
from pydantic import BaseModel
from typing import Optional

# -- Pydantic Models --
# request model for movie
class MovieCreate(BaseModel):
    title: str
    status: str
    rating: float
    genre: str

# response model for movie
class MovieResponse(BaseModel):
    id: int
    title: str
    status: str
    rating: float
    genre: str

# partial update model - all fields optional
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    rating: Optional[float] = None
    genre: Optional[str] = None