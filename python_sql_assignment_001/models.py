from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional
from datetime import date

class GenreResponse(BaseModel):
    genre_id: int
    genre_name: str = Field(min_length=1, max_length=32)

class GenreCreate(BaseModel):
    genre_name: str = Field(min_length=1, max_length=32)

class GenreUpdate(BaseModel):
    genre_name: str = Field(min_length=1, max_length=32)

class BookResponse(BaseModel):
    book_id: int
    genre_id: int = Field(ge=0)
    title: str = Field(min_length=1, max_length=64)     # varchar(64)
    author: str = Field(min_length=1, max_length=64)    # varchar(64)
    publication_year: int = Field(ge=0, le=32767)       # small int
    inventory: int = Field(ge=0, le=32767)              # small int

class BookCreate(BaseModel):
    genre_id: int = Field(ge=0)
    title: str = Field(min_length=1, max_length=64)     # varchar(64)
    author: str = Field(min_length=1, max_length=64)    # varchar(64)
    publication_year: int = Field(ge=0, le=32767)       # small int
    inventory: int = Field(ge=0, le=32767)              # small int

class BookUpdate(BaseModel):
    genre_id: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publication_year: Optional[int] = None
    inventory: Optional[int] = None

class MemberResponse(BaseModel):
    member_id: int
    member_name: str = Field(min_length=1, max_length=64)
    email: str = Field(min_length=1, max_length=64)
    date_joined: date

class MemberCreate(BaseModel):
    member_name: str = Field(min_length=1, max_length=64)
    email: str = Field(min_length=1, max_length=64)
    date_joined: date

class MemberUpdate(BaseModel):
    member_name: Optional[str] = None
    email: Optional[str] = None
    date_joined: Optional[date] = None

class LoanResponse(BaseModel):
    loan_id: int
    book_id: int
    member_id: int
    date_loaned: date
    date_due: date
    date_returned: date

class LoanCreate(BaseModel):
    book_id: int
    member_id: int
    date_loaned: date
    date_due: date
    date_returned: date

class LoanUpdate(BaseModel):
    book_id: Optional[int] = None
    member_id: Optional[int] = None
    date_loaned: Optional[date] = None
    date_due: Optional[date] = None
    date_returned: Optional[date] = None