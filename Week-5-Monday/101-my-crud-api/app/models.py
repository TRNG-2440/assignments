from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

year = date.today().year

class MovieCreate(BaseModel):
    title: str = Field(min_length = 1, max_length = 50)
    director: str = Field(min_length = 1, max_length = 50)
    year: int = Field(lt = year, gt = 1880)
    genre: str = Field(min_length = 1, max_length = 20)
    rating: int = Field(gt = -1, lt = 11)

class MovieOut(BaseModel):
    id: int
    title: str
    director: str
    year: int
    genre: str
    rating: int

class MovieUpdate(BaseModel):
    title: str = Field(min_length = 1, max_length = 50)
    director: str = Field(min_length = 1, max_length = 50)
    year: int = Field(lt = year, gt = 1880)
    genre: str
    rating: int =  Field(gt = -1, lt = 11)