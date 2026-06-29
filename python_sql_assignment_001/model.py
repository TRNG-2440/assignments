from dataclasses import dataclass
from datetime import date


@dataclass
class Genre:
    genre_id: int
    genre_name: str


@dataclass
class Member:
    member_id: int
    name: str
    email: str
    join_date: date


@dataclass
class Book:
    book_id: int
    title: str
    author_name: str
    publication_year: str
    genre_id: int
    total_copies: int
    available_copies: int


@dataclass
class Loan:
    loan_id: int
    book_id: int
    member_id: int
    loan_date: date
    due_date: date
    return_date: date
