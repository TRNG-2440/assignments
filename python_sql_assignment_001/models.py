"""Pydantic request and response models for the REST layer."""

import datetime
from typing import Optional

from pydantic import BaseModel


class GenreIn(BaseModel):
    name: str


class GenreOut(BaseModel):
    genre_id: int
    name: str


class BookIn(BaseModel):
    title: str
    author: str
    publication_year: Optional[int] = None
    genre_id: Optional[int] = None
    copy_count: int = 0


class BookOut(BaseModel):
    book_id: int
    title: str
    author: str
    publication_year: Optional[int] = None
    genre_id: Optional[int] = None
    copy_count: int


class MemberIn(BaseModel):
    full_name: str
    email: str
    join_date: datetime.date


class MemberOut(BaseModel):
    member_id: int
    full_name: str
    email: str
    join_date: datetime.date


class LoanIn(BaseModel):
    book_id: int
    member_id: int
    loan_date: datetime.date
    due_date: datetime.date


class LoanReturnIn(BaseModel):
    return_date: datetime.date


class LoanOut(BaseModel):
    loan_id: int
    book_id: int
    member_id: int
    loan_date: datetime.date
    due_date: datetime.date
    return_date: Optional[datetime.date] = None
