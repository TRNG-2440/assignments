from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from models.book import BookCreate, BookResponse
from dependencies import get_book_service
from services import BookService


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=List[BookResponse])
def get_all(
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> List[BookResponse]:
    return book_service.get_all()


@router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=BookResponse)
def get_by_id(
    book_id: int,
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> BookResponse:
    return book_service.get_by_id(book_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create(
    book: BookCreate,
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> BookResponse:
    return book_service.create(book)


@router.put("/{book_id}", status_code=status.HTTP_200_OK, response_model=BookResponse)
def update(
    book_id: int,
    book: BookCreate,
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> BookResponse:
    return book_service.update(book_id, book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(
    book_id: int,
    book_service: Annotated[BookService, Depends(get_book_service)],
) -> None:
    return book_service.delete_by_id(book_id)
