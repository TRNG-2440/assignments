from typing import Annotated

from fastapi import Depends

from db.database import DatabaseManager
from dao.genre_dao import GenreDAO
from dao.book_dao import BookDAO
from services.genre import GenreService


def get_genre_repo(db: Annotated[DatabaseManager, Depends()]) -> GenreDAO:
    return GenreDAO(db)


def get_book_repo(db: Annotated[DatabaseManager, Depends()]) -> BookDAO:
    return BookDAO(db)


def get_genre_service(
    genre_repo: Annotated[GenreDAO, Depends(get_genre_repo)],
    book_repo: Annotated[BookDAO, Depends(get_book_repo)],
) -> GenreService:
    return GenreService(genre_repo, book_repo)
