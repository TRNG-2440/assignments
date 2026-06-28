from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional
from dao import GenreDAO, BookDAO, MemberDAO, LoanDAO

app = FastAPI()
genre_dao = GenreDAO()
book_dao = BookDAO()
member_dao = MemberDAO()
loan_dao = LoanDAO()

# ================================================
# Pydantic Models
# ================================================

# ====== Genre ======
class CreateGenreRequest(BaseModel):
    genre_name: str

class UpdateGenreRequest(BaseModel):
    genre_name: str

class PatchGenreRequest(BaseModel):
    genre_name: str

class GenreResponse(BaseModel):
    genre_id: int
    genre_name: str

