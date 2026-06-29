from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from database import get_connection, initialize_db
from dao import GenreDAO, BookDAO, MemberDAO, LoanDAO

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = get_connection()
    initialize_db(conn)
    conn.close()
    yield

app = FastAPI(title="Library Management API", lifespan=lifespan)

def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

class GenreBase(BaseModel):
    name: str

class GenreOut(GenreBase):
    genre_id: int

class BookIn(BaseModel):
    title: str
    author: str
    publication_year: int
    genre_id: int
    copy_count: int

class BookOut(BookIn):
    book_id: int

class MemberIn(BaseModel):
    full_name: str
    email: str
    join_date: date

class MemberOut(MemberIn):
    member_id: int

class LoanIn(BaseModel):
    book_id: int
    member_id: int
    loan_date: date
    due_date: date

class LoanOut(LoanIn):
    loan_id: int
    return_date: Optional[date] = None

class ReturnUpdate(BaseModel):
    return_date: date

@app.post("/genres", response_model=GenreOut)
def create_genre(genre: GenreBase, conn=Depends(get_db)):
    return GenreDAO(conn).create(genre.name)

@app.get("/genres", response_model=List[GenreOut])
def get_genres(conn=Depends(get_db)):
    return GenreDAO(conn).get_all()

@app.get("/genres/{genre_id}", response_model=GenreOut)
def get_genre(genre_id: int, conn=Depends(get_db)):
    genre = GenreDAO(conn).get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@app.put("/genres/{genre_id}", response_model=GenreOut)
def update_genre(genre_id: int, genre: GenreBase, conn=Depends(get_db)):
    updated = GenreDAO(conn).update(genre_id, genre.name)
    if not updated:
        raise HTTPException(status_code=404, detail="Genre not found")
    return updated

@app.delete("/genres/{genre_id}")
def delete_genre(genre_id: int, conn=Depends(get_db)):
    GenreDAO(conn).delete(genre_id)
    return {"message": "Deleted successfully"}

@app.post("/books", response_model=BookOut)
def create_book(book: BookIn, conn=Depends(get_db)):
    return BookDAO(conn).create(book.title, book.author, book.publication_year, book.genre_id, book.copy_count)

@app.get("/books", response_model=List[BookOut])
def get_books(conn=Depends(get_db)):
    return BookDAO(conn).get_all()

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, conn=Depends(get_db)):
    book = BookDAO(conn).get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, book: BookIn, conn=Depends(get_db)):
    updated = BookDAO(conn).update(book_id, book.title, book.author, book.publication_year, book.genre_id, book.copy_count)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@app.delete("/books/{book_id}")
def delete_book(book_id: int, conn=Depends(get_db)):
    BookDAO(conn).delete(book_id)
    return {"message": "Deleted successfully"}

@app.post("/members", response_model=MemberOut)
def create_member(member: MemberIn, conn=Depends(get_db)):
    return MemberDAO(conn).create(member.full_name, member.email, member.join_date)

@app.get("/members", response_model=List[MemberOut])
def get_members(conn=Depends(get_db)):
    return MemberDAO(conn).get_all()

@app.get("/members/{member_id}", response_model=MemberOut)
def get_member(member_id: int, conn=Depends(get_db)):
    member = MemberDAO(conn).get_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@app.put("/members/{member_id}", response_model=MemberOut)
def update_member(member_id: int, member: MemberIn, conn=Depends(get_db)):
    updated = MemberDAO(conn).update(member_id, member.full_name, member.email, member.join_date)
    if not updated:
        raise HTTPException(status_code=404, detail="Member not found")
    return updated

@app.delete("/members/{member_id}")
def delete_member(member_id: int, conn=Depends(get_db)):
    MemberDAO(conn).delete(member_id)
    return {"message": "Deleted successfully"}

@app.post("/loans", response_model=LoanOut)
def create_loan(loan: LoanIn, conn=Depends(get_db)):
    return LoanDAO(conn).create(loan.book_id, loan.member_id, loan.loan_date, loan.due_date)

@app.get("/loans/active", response_model=List[LoanOut])
def get_active_loans(conn=Depends(get_db)):
    return LoanDAO(conn).get_active_loans()

@app.get("/loans", response_model=List[LoanOut])
def get_loans(conn=Depends(get_db)):
    return LoanDAO(conn).get_all()

@app.get("/loans/{loan_id}", response_model=LoanOut)
def get_loan(loan_id: int, conn=Depends(get_db)):
    loan = LoanDAO(conn).get_by_id(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@app.patch("/loans/{loan_id}/return", response_model=LoanOut)
def return_loan(loan_id: int, return_data: ReturnUpdate, conn=Depends(get_db)):
    updated = LoanDAO(conn).return_book(loan_id, return_data.return_date)
    if not updated:
        raise HTTPException(status_code=404, detail="Loan not found")
    return updated

@app.delete("/loans/{loan_id}")
def delete_loan(loan_id: int, conn=Depends(get_db)):
    LoanDAO(conn).delete(loan_id)
    return {"message": "Deleted successfully"}