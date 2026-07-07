from fastapi import APIRouter, HTTPException, status

from app.models import MovieRequest, MovieResponse

router = APIRouter(prefix="/movies", tags=["movies"])

DataBase: dict[int, dict] = {}
next_id = 1


@router.post("", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(payload: MovieRequest):
    global next_id
    record = {"id": next_id, **payload.model_dump()}
    DataBase[next_id] = record
    next_id += 1
    return record


@router.get("", response_model=list[MovieResponse])
def list_movies(in_theaters: bool | None = None, limit: int = 50):
    rows = list(DataBase.values())
    if in_theaters is not None:
        rows = [r for r in rows if r["in_theaters"] == in_theaters]
    return rows[:limit]


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int):
    item = DataBase.get(movie_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Movie {movie_id} not found")
    return item


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, payload: MovieRequest):
    if movie_id not in DataBase:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Movie {movie_id} not found")
    record = {"id": movie_id, **payload.model_dump()}
    DataBase[movie_id] = record
    return record


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):
    if movie_id not in DataBase:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Movie {movie_id} not found")
    del DataBase[movie_id]
    return None
