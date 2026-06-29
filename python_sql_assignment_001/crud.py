"""FastAPI REST layer over the library DAO (stretch goal 1).

Run with:  uvicorn crud:app reload
Interactive docs at:  http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from psycopg2 import IntegrityError

from database import get_connection
from dao import GenreDAO, BookDAO, MemberDAO, LoanDAO
from views import StatsDAO
from models import (
    GenreIn, GenreOut,
    BookIn, BookOut,
    MemberIn, MemberOut,
    LoanIn, LoanReturnIn, LoanOut,
)

app = FastAPI(title="Library API")


@app.exception_handler(IntegrityError)
def integrity_error_handler(request: Request, exc: IntegrityError):
    # Raised for things like a duplicate genre name / member email, or
    # deleting a row that another table still references.
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Operation violates a database constraint."},
    )


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


# Genre endpoints 

@app.get("/genres", response_model=list[GenreOut])
def list_genres(conn=Depends(get_db)):
    return GenreDAO(conn).get_all()


@app.get("/genres/{genre_id}", response_model=GenreOut)
def get_genre(genre_id: int, conn=Depends(get_db)):
    row = GenreDAO(conn).get_by_id(genre_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Genre not found")
    return row


@app.post("/genres", response_model=GenreOut, status_code=status.HTTP_201_CREATED)
def create_genre(payload: GenreIn, conn=Depends(get_db)):
    return GenreDAO(conn).create(payload.name)


@app.put("/genres/{genre_id}", response_model=GenreOut)
def update_genre(genre_id: int, payload: GenreIn, conn=Depends(get_db)):
    row = GenreDAO(conn).update(genre_id, payload.name)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Genre not found")
    return row


@app.delete("/genres/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id: int, conn=Depends(get_db)):
    row = GenreDAO(conn).delete(genre_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Genre not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Book endpoints

@app.get("/books", response_model=list[BookOut])
def list_books(conn=Depends(get_db)):
    return BookDAO(conn).get_all()


@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, conn=Depends(get_db)):
    row = BookDAO(conn).get_by_id(book_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
    return row


@app.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookIn, conn=Depends(get_db)):
    return BookDAO(conn).create(
        payload.title, payload.author, payload.publication_year,
        payload.genre_id, payload.copy_count,
    )


@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookIn, conn=Depends(get_db)):
    row = BookDAO(conn).update(
        book_id, payload.title, payload.author, payload.publication_year,
        payload.genre_id, payload.copy_count,
    )
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
    return row


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, conn=Depends(get_db)):
    row = BookDAO(conn).delete(book_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#  Member endpoints 

@app.get("/members", response_model=list[MemberOut])
def list_members(conn=Depends(get_db)):
    return MemberDAO(conn).get_all()


@app.get("/members/{member_id}", response_model=MemberOut)
def get_member(member_id: int, conn=Depends(get_db)):
    row = MemberDAO(conn).get_by_id(member_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Member not found")
    return row


@app.post("/members", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(payload: MemberIn, conn=Depends(get_db)):
    return MemberDAO(conn).create(payload.full_name, payload.email, payload.join_date)


@app.put("/members/{member_id}", response_model=MemberOut)
def update_member(member_id: int, payload: MemberIn, conn=Depends(get_db)):
    row = MemberDAO(conn).update(
        member_id, payload.full_name, payload.email, payload.join_date
    )
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Member not found")
    return row


@app.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, conn=Depends(get_db)):
    row = MemberDAO(conn).delete(member_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Member not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#  Loan endpoints 

@app.get("/loans", response_model=list[LoanOut])
def list_loans(conn=Depends(get_db)):
    return LoanDAO(conn).get_all()


@app.get("/loans/active", response_model=list[LoanOut])
def list_active_loans(conn=Depends(get_db)):
    return LoanDAO(conn).get_active_loans()


@app.get("/loans/{loan_id}", response_model=LoanOut)
def get_loan(loan_id: int, conn=Depends(get_db)):
    row = LoanDAO(conn).get_by_id(loan_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Loan not found")
    return row


@app.post("/loans", response_model=LoanOut, status_code=status.HTTP_201_CREATED)
def create_loan(payload: LoanIn, conn=Depends(get_db)):
    return LoanDAO(conn).create(
        payload.book_id, payload.member_id, payload.loan_date, payload.due_date
    )


@app.patch("/loans/{loan_id}/return", response_model=LoanOut)
def return_loan(loan_id: int, payload: LoanReturnIn, conn=Depends(get_db)):
    row = LoanDAO(conn).return_book(loan_id, payload.return_date)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Loan not found")
    return row


@app.delete("/loans/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(loan_id: int, conn=Depends(get_db)):
    row = LoanDAO(conn).delete(loan_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Loan not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#  Statistics endpoints (stretch goal 2) 

@app.get("/stats/loanedgenres")
def stat_loaned_genres(conn=Depends(get_db)):
    return StatsDAO(conn).most_loaned_genres()


@app.get("/stats/activemembers")
def stat_active_members(conn=Depends(get_db)):
    return StatsDAO(conn).most_active_members()


@app.get("/stats/overdueloans")
def stat_overdue_loans(conn=Depends(get_db)):
    return StatsDAO(conn).overdue_loans()
