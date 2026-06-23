from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from exceptions import (
    AuthenticationError,
    FilePathNotSpecifiedError,
    InvalidDateRangeError,
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserDoesNotExistError,
)
from logger import logger
from routes import users, budgets

app = FastAPI(title="Personal Finance Tracker API", version="1.0.0")

# Register routes
app.include_router(users, prefix="/users", tags=["Users"])
app.include_router(budgets, prefix="/budgets", tags=["Budgets"])


# Register exception handlers
@app.exception_handler(AuthenticationError)
async def auth_exception_handler(
    request: Request, exc: AuthenticationError
) -> JSONResponse:
    logger.warning(f"Failed login attempt for user: {exc.username}")

    # Return the 401 response to the client
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail},
        headers={"WWW-Authenticate": "Basic"},
    )


@app.exception_handler(InvalidPasswordError)
async def invalid_pwd_handler(
    request: Request, exc: InvalidPasswordError
) -> JSONResponse:

    # Return the 400 response to the client
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
        headers={"WWW-Authenticate": "Basic"},
    )


@app.exception_handler(FilePathNotSpecifiedError)
async def file_path_unspecified_handler(
    request: Request, exc: FilePathNotSpecifiedError
) -> JSONResponse:
    logger.error(exc.detail)
    # Return 500 response to the client
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
        headers={"WWW-Authenticate": "Basic"},
    )


@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(
    request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    logger.warning(
        f"User with username: {exc.username} or email: {exc.email} already exsists!"
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
        headers={"WWW-Authenticate": "Basic"},
    )


@app.exception_handler(UserDoesNotExistError)
async def user_doesnt_exists_handler(
    request: Request, exc: UserDoesNotExistError
) -> JSONResponse:
    logger.warning(f"User with username: {exc.username} does not exist!")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail},
        headers={"WWW-Authenticate": "Basic"},
    )


@app.exception_handler(InvalidDateRangeError)
async def invalid_date_range_handler(
    request: Request, exc: InvalidDateRangeError
) -> JSONResponse:
    logger.warning(f"Invalid date range {exc.start_date} - {exc.end_date} provided!")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
        headers={"WWW-Authenticate": "Basic"},
    )
