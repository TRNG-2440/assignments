"""
Endpoint definitions.
"""
# dependencies
import uuid
from datetime import datetime, timezone
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from storage import get_user_movies, save_user_movies
from models import MovieCreate, MovieResponse, MovieUpdate
from auth import verify_api_key

router = APIRouter(prefix = "/movies", tags = ["Movies"])

# shared error responses for authenticated routes
AUTH_RESPONSES: dict[int | str, dict[str, Any]] = {
    403: {"description": "Forbidden — missing or invalid API key"},
}
NOT_FOUND_RESPONSES: dict[int | str, dict[str, Any]] = {
    **AUTH_RESPONSES,
    404: {"description": "Not found — no movie with that ID in your watchlist"},
}

# CREATE (POST)
@router.post(
    "",
    response_model = MovieResponse,
    status_code = status.HTTP_201_CREATED,
    summary = "Add a movie to your watchlist",
    description = (
        "Creates a new movie in the authenticated user's watchlist. "
        "The server generates the unique `id` and `created_at` timestamp. "
        "Requires a valid `x-api-key` header."
    ),
    responses = {
        **AUTH_RESPONSES,
        422: {"description": "Validation error — request body did not match the expected schema"},
    },
)
def create_movie(movie: MovieCreate, username: str = Depends(verify_api_key)):
    movies = get_user_movies(username)
    new_movie = {
        "id": str(uuid.uuid4()),
        "title": movie.title,
        "status": movie.status,
        "rating": movie.rating,
        "genre": movie.genre,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    movies.append(new_movie)
    save_user_movies(username, movies)
    return new_movie

# READ ALL
@router.get(
    "",
    response_model = list[MovieResponse],
    summary = "List all movies in your watchlist",
    description = "Returns every movie belonging to the authenticated user. Requires a valid `x-api-key` header.",
    responses = AUTH_RESPONSES,
)
def list_movies(username: str = Depends(verify_api_key)):
    return get_user_movies(username)

# READ ONE
@router.get(
    "/{movie_id}",
    response_model = MovieResponse,
    summary = "Get a single movie by ID",
    description = "Returns one movie from the authenticated user's watchlist by its unique ID.",
    responses = NOT_FOUND_RESPONSES,
)
def get_movie(movie_id: str, username: str = Depends(verify_api_key)):
    movies = get_user_movies(username)
    for m in movies:
        if m["id"] == movie_id:
            return m
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Movie not found")

# UPDATE (partial)
@router.patch(
    "/{movie_id}",
    response_model = MovieResponse,
    summary = "Update fields on an existing movie",
    description = (
        "Partially updates a movie in the authenticated user's watchlist. "
        "Only the fields included in the request body are changed."
    ),
    responses = {
        **NOT_FOUND_RESPONSES,
        422: {"description": "Validation error — request body did not match the expected schema"},
    },
)
def update_movie(movie_id: str, update: MovieUpdate, username: str = Depends(verify_api_key)):
    movies = get_user_movies(username)
    for m in movies:
        if m["id"] == movie_id:
            # only overwrite fields the client actually sent
            m.update(update.model_dump(exclude_unset = True))
            save_user_movies(username, movies)
            return m
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Movie not found")

# DELETE
@router.delete(
    "/{movie_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    summary = "Remove a movie from your watchlist",
    description = "Deletes a movie from the authenticated user's watchlist by its unique ID.",
    responses = NOT_FOUND_RESPONSES,
)
def delete_movie(movie_id: str, username: str = Depends(verify_api_key)):
    movies = get_user_movies(username)
    new_movies = [m for m in movies if m["id"] != movie_id]
    if len(new_movies) == len(movies):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Movie not found")
    save_user_movies(username, new_movies)
