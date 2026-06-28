from pydantic import BaseModel
from typing import Optional
from datetime import date

class GenreCreate(BaseModel):
    name: str
    
class GenreResponse(BaseModel):
    genre_id: int
    name: str
    
class GenreUpdate(BaseModel):
    name: Optional[str] = None

class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: int
    genre_id: int
    copy_count: int

class BookResponse(BaseModel):
    book_id: int
    title: str
    author: str
    publication_year: int
    genre_id: int
    copy_count: int
    
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publication_year: Optional[int] = None
    genre_id: Optional[int] = None
    copy_count: Optional[int] = None

class MemberCreate(BaseModel):
    full_name: str
    email: str
    join_date: date
    
class MemberResponse(BaseModel):
    member_id: int
    full_name: str
    email: str
    join_date: date
    
class MemberUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    join_date: Optional[date] = None

class LoanCreate(BaseModel):
    book_id: int
    member_id: int
    loan_date: date
    due_date: date
    
class LoanResponse(BaseModel):
    loan_id: int
    book_id: int
    member_id: int
    loan_date: date
    due_date: date
    return_date: Optional[date] = None
    
class LoanUpdate(BaseModel):
    book_id: Optional[int] = None
    member_id: Optional[int] = None
    loan_date: Optional[date] = None
    due_date: Optional[date] = None
    return_date: Optional[date] = None