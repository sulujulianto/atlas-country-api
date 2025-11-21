from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.exceptions import BadRequestError, NotFoundError, ValidationError


def _error_response(code: int, message: str, details: dict | None = None):
    return JSONResponse(
        status_code=code,
        content={
            "status": "error",
            "code": code,
            "message": message,
            "details": details or None,
        },
    )


async def not_found_handler(_: Request, exc: NotFoundError):
    return _error_response(status.HTTP_404_NOT_FOUND, exc.message, exc.details)


async def bad_request_handler(_: Request, exc: BadRequestError):
    return _error_response(status.HTTP_400_BAD_REQUEST, exc.message, exc.details)


async def validation_error_handler(_: Request, exc: ValidationError):
    return _error_response(status.HTTP_422_UNPROCESSABLE_ENTITY, exc.message, exc.details)


async def request_validation_handler(_: Request, exc: RequestValidationError):
    return _error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Invalid request parameters",
        {"errors": exc.errors()},
    )


async def unhandled_exception_handler(_: Request, exc: Exception):
    return _error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error", {"error": str(exc)})
