from typing import List

from fastapi import APIRouter, Depends, status
from models.genre import GenreCreate, GenreResponse
from dependencies import get_genre_service
from services.genre import GenreService

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=List[GenreResponse])
def get_all(
    genre_service: GenreService = Depends(get_genre_service),
) -> List[GenreResponse]:
    return genre_service.get_all()


@router.get("/{genre_id}", status_code=status.HTTP_200_OK, response_model=GenreResponse)
def get_by_id(
    genre_id: int,
    genre_service: GenreService = Depends(get_genre_service),
) -> GenreResponse:
    return genre_service.get_by_id(genre_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=GenreResponse)
def create(
    genre_create: GenreCreate,
    genre_service: GenreService = Depends(get_genre_service),
) -> GenreResponse:
    return genre_service.create(genre_create)


@router.put(
    "/{genre_id}", status_code=status.HTTP_201_CREATED, response_model=GenreResponse
)
def update(
    genre_id: int,
    genre_create: GenreCreate,
    genre_service: GenreService = Depends(get_genre_service),
) -> GenreResponse:
    return genre_service.update(genre_id, genre_create)


@router.delete(
    "/{genre_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_by_id(
    genre_id: int,
    genre_service: GenreService = Depends(get_genre_service),
) -> None:
    return genre_service.delete_by_id(genre_id)
