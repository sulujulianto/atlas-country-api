from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.exceptions import BadRequestError, NotFoundError, ValidationError


def _error_response(http_status: int, code: str, message: str, details: dict | None = None):
    return JSONResponse(
        status_code=http_status,
        content={
            "status": "error",
            "message": message,
            "code": code,
            "details": details or {},
        },
    )


async def not_found_handler(_: Request, exc: NotFoundError):
    return _error_response(exc.status_code, exc.code, exc.message, exc.details)


async def bad_request_handler(_: Request, exc: BadRequestError):
    return _error_response(exc.status_code, exc.code, exc.message, exc.details)


async def validation_error_handler(_: Request, exc: ValidationError):
    return _error_response(exc.status_code, exc.code, exc.message, exc.details)


async def request_validation_handler(_: Request, exc: RequestValidationError):
    return _error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "ERR_VALIDATION",
        "Invalid request parameters",
        {"errors": exc.errors()},
    )


async def unhandled_exception_handler(_: Request, exc: Exception):
    return _error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "ERR_INTERNAL", "Internal server error", {"error": str(exc)})
