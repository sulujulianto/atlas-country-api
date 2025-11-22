from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.logging import RequestLoggingMiddleware, configure_logging
from app.core.security import RateLimiterMiddleware, SecurityHeadersMiddleware, configure_cors
from app.config.settings import get_settings
from app.exceptions import BadRequestError, NotFoundError, ValidationError
from app.exceptions.handlers import (
    bad_request_handler,
    not_found_handler,
    request_validation_handler,
    unhandled_exception_handler,
    validation_error_handler,
)
from app.routes import api_router
from schemas import ResponseSchema


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        description=settings.description,
        version=settings.version,
        contact={"name": settings.contact_name, "email": settings.contact_email},
        license_info={"name": settings.license_name, "url": settings.license_url},
        openapi_tags=[
            {"name": "Countries", "description": "Country information, search, filtering, and metadata."},
            {"name": "Capitals", "description": "Capital city data with search and lookup."},
            {"name": "Statistics", "description": "Aggregated analytics over countries and capitals."},
        ],
    )

    configure_cors(app)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimiterMiddleware)

    app.include_router(api_router)

    @app.get(
        "/health",
        response_model=ResponseSchema,
        tags=["Health"],
        summary="Health Check",
        description="Quick health check endpoint.",
    )
    async def health() -> ResponseSchema:
        return ResponseSchema(status="success", data={"status": "ok"}, meta=None, error=None)

    # Exception handlers
    app.add_exception_handler(NotFoundError, not_found_handler)  # type: ignore[arg-type]
    app.add_exception_handler(BadRequestError, bad_request_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ValidationError, validation_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, request_validation_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)

    return app


app = create_app()
