from typing import Annotated

from fastapi import Depends

from db.database import DatabaseManager
from dao.genre_dao import GenreDAO
from dao.book_dao import BookDAO
from dao.member_dao import MemberDAO
from dao.loan_dao import LoanDAO
from services.loan import LoanService
from services import GenreService, MemberService, BookService


def get_genre_repo(db: Annotated[DatabaseManager, Depends()]) -> GenreDAO:
    return GenreDAO(db)


def get_member_repo(db: Annotated[DatabaseManager, Depends()]) -> MemberDAO:
    return MemberDAO(db)


def get_book_repo(db: Annotated[DatabaseManager, Depends()]) -> BookDAO:
    return BookDAO(db)


def get_loan_repo(
    db: Annotated[DatabaseManager, Depends()],
    book_repo: Annotated[BookDAO, Depends(get_book_repo)],
) -> LoanDAO:
    return LoanDAO(db, book_repo)


def get_genre_service(
    genre_repo: Annotated[GenreDAO, Depends(get_genre_repo)],
    book_repo: Annotated[BookDAO, Depends(get_book_repo)],
) -> GenreService:
    return GenreService(genre_repo, book_repo)


def get_member_service(
    member_repo: Annotated[MemberDAO, Depends(get_member_repo)],
    loan_repo: Annotated[LoanDAO, Depends(get_loan_repo)],
) -> MemberService:
    return MemberService(member_repo, loan_repo)


def get_book_service(
    book_repo: Annotated[BookDAO, Depends(get_book_repo)],
    genre_repo: Annotated[GenreDAO, Depends(get_genre_repo)],
    loan_repo: Annotated[LoanDAO, Depends(get_loan_repo)],
) -> BookService:
    return BookService(book_repo, genre_repo, loan_repo)


def get_loan_service(
    loan_repo: Annotated[LoanDAO, Depends(get_loan_repo)],
    book_repo: Annotated[BookDAO, Depends(get_book_repo)],
) -> LoanService:
    return LoanService(loan_repo, book_repo)
