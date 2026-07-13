from fastapi import APIRouter, HTTPException, status
from models import MovieCreate, MovieOut, MovieUpdate

router = APIRouter(
    prefix = "/movies",
    tags = ["movies"],
    responses = {404: {"description": "Movie not found"}}
)

DB: dict[int, dict] = {}
next_id = 1

def get_or_404(movie_id: int) -> dict:
    movie = DB.get(movie_id)
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {movie_id} not found"
            )
    return movie

@router.post("", response_model = MovieOut, status_code = status.HTTP_201_CREATED)
def create_movie(payload: MovieCreate):
    global next_id
    record = {"id": next_id, **payload.model_dump()}
    DB[next_id] = record
    next_id += 1
    return record

@router.get("/{movie_id}", response_model= MovieOut)
def get_movie(movie_id: int):
    item = DB.get(movie_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Movie {movie_id} not found")
    return item

@router.get("", response_model = list[MovieOut])
def get_movies(
    limit: int = 20, offset: int = 0
):
    movies = list(DB.values())
    return movies[offset: offset + limit]

@router.put("/{movie_id}", response_model = MovieOut)
def update_movie(movie_id: int, payload: MovieUpdate):
    get_or_404(movie_id)
    record = {"id": movie_id, **payload.model_dump()}
    DB[movie_id] = record
    return record

@router.delete("/{movie_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):
    if movie_id not in DB:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Movie {movie_id} not found")
    del DB[movie_id]
    return None