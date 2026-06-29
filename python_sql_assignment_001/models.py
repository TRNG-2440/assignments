from dataclasses import dataclass
from datetime import date
from typing import Optional

# 
@dataclass
class Genre:
    genre_id: int
    name: str


@dataclass
class Book:
    book_id: int
    title: str
    author: str
    publication_year: int
    genre_id: int
    copy_count: int


@dataclass
class Member:
    member_id: int
    full_name: str
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