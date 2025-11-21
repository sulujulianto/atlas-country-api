from fastapi import FastAPI, HTTPException

from app.core import logging  # noqa: F401 - load logging configuration
from app.core.exceptions import global_exception_handler, http_exception_handler
from app.routes import capitals, statistics


def create_app() -> FastAPI:
    """
    Application factory for the Atlas Country API.
    This makes the app easier to test and extend in the future.
    """
    app = FastAPI(
        title="Atlas Country API",
        description=(
            "A modern REST API that provides country and capital information, "
            "including search, filtering, and basic region statistics."
        ),
        version="1.0.0",
    )

    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)

    app.include_router(capitals.router)
    app.include_router(statistics.router)

    @app.get("/health", tags=["Health"])
    def health_check():
        """
        Simple health check endpoint to verify that the API is running.
        """
        return {"status": "ok", "message": "Atlas Country API is running"}

    @app.get("/", include_in_schema=False)
    def root():
        """
        Root endpoint that redirects users to the API documentation.
        """
        return {
            "message": "Welcome to the Atlas Country API.",
            "docs_url": "/docs",
            "openapi_url": "/openapi.json",
        }

    return app


app = create_app()
