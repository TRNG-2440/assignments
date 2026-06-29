from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from exceptions import (
    BooksWithGenreExistsError,
    GenreExistsError,
    GenreNotFoundError,
    MemberExistsError,
    MemberHasLoansError,
    MemberNotFoundError,
)
from routes import genres, members
from logger import logger

app = FastAPI(title="Library API", version="1.0.0")

app.include_router(genres, prefix="/genres", tags=["Genres"])
app.include_router(members, prefix="/members", tags=["Members"])


@app.exception_handler(GenreNotFoundError)
async def genre_not_found_handler(
    request: Request, exc: GenreNotFoundError
) -> JSONResponse:
    logger.warning(f"No record found for genre_id: {exc.genre_id}!")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )


@app.exception_handler(MemberNotFoundError)
async def member_not_found_handler(
    request: Request, exc: MemberNotFoundError
) -> JSONResponse:
    logger.warning(f"No record found for member_id: {exc.member_id}!")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )


@app.exception_handler(GenreExistsError)
async def genre_exists_handler(request: Request, exc: GenreExistsError) -> JSONResponse:
    logger.warning(f"Genre: {exc.genre_name} already exists!")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
    )


@app.exception_handler(MemberExistsError)
async def member_exists_handler(
    request: Request, exc: MemberExistsError
) -> JSONResponse:
    logger.warning(f"Member with email: {exc.member_email} already exists!")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
    )


@app.exception_handler(BooksWithGenreExistsError)
async def books_with_genre_exist_handler(
    request: Request, exc: BooksWithGenreExistsError
) -> JSONResponse:
    logger.warning(f"Books with genre_id: {exc.genre_id} exist!")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
    )


@app.exception_handler(MemberHasLoansError)
async def member_has_loans_handler(
    request: Request, exc: MemberHasLoansError
) -> JSONResponse:
    logger.warning(f"Member id: {exc.member_id} has borrowed books!")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
    )
