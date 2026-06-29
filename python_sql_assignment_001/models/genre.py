from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, Field


class GenreCreate(BaseModel):
    genre_name: Annotated[str, Field(description="Name of the genre")]


class GenreResponse(BaseModel):
    genre_id: Annotated[int, Field(description="Id of the genre")]
    genre_name: Annotated[str, Field(description="Name of the genre")]


@dataclass
class Genre:
    genre_name: str
    genre_id: int = -1
