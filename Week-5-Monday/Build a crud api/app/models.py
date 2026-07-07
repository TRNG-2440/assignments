from pydantic import BaseModel, Field


class MovieRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    director: str
    year: int = Field(gt=1888)
    in_theaters: bool = True


class MovieResponse(BaseModel):
    id: int
    title: str
    director: str
    year: int
    in_theaters: bool
