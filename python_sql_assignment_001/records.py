from datetime import date
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class GenreRecord:
    genre_id: int
    name: str


@dataclass
class BookRecord:
    book_id: int
    title: str
    author: str
    publication_year: date
    genre_id: int
    copy_count: int


@dataclass
class Member:
    member_id: int
    name: str
    email: str
    join_date: date


@dataclass
class Loan:
    loan_id: int
    book_id: int
    member_id: int
    loan_date: date
    due_date: date
    return_date: Optional[date]

