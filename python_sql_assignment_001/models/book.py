from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: Annotated[str, Field(description="Title of the book")]
    author_name: Annotated[str, Field(description="Name of the author")]
    publication_year: Annotated[str, Field(description="Year of publication")]
    genre_id: Annotated[int, Field(description="Id of primary book genre")]
    total_copies: Annotated[int, Field(description="Total copies of the book in stock")]


class BookResponse(BaseModel):
    book_id: Annotated[int, Field(description="Id of the book")]
    title: Annotated[str, Field(description="Title of the book")]
    author_name: Annotated[str, Field(description="Name of the author")]
    publication_year: Annotated[str, Field(description="Year of publication")]
    genre_id: Annotated[int, Field(description="Id of primary book genre")]
    total_copies: Annotated[int, Field(description="Total copies of the book in stock")]
    available_copies: Annotated[int, Field(description="Current available copies")]


@dataclass
class Book:
    book_id: int
    title: str
    author_name: str
    publication_year: str
    genre_id: int
    total_copies: int
    available_copies: int
