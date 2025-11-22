import logging
import time
import uuid
from contextvars import ContextVar
from typing import Callable, Union

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.config.settings import get_settings

_request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


class RequestIdFilter(logging.Filter):
    """Inject request_id from context into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id_ctx.get()
        return True


def configure_logging() -> None:
    """Configure root logger with readable format and request ID filter."""
    settings = get_settings()
    logger = logging.getLogger()
    logger.setLevel(settings.log_level.upper())

    handler = logging.StreamHandler()
    handler.addFilter(RequestIdFilter())
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | request_id=%(request_id)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.handlers = [handler]


def get_logger(name: str = "atlas") -> logging.Logger:
    """Return configured logger with request ID filter."""
    logger = logging.getLogger(name)
    logger.addFilter(RequestIdFilter())
    return logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = get_logger("atlas.request")

    async def dispatch(self, request: Request, call_next: Callable):
        request_id = str(uuid.uuid4())
        _request_id_ctx.set(request_id)
        start = time.perf_counter()
        response: Response | None = None
        try:
            response = await call_next(request)
            return response
        except Exception as exc:  # log stack trace for unhandled exceptions
            self.logger.exception(
                "Unhandled exception during request",
                extra={"extra": {"method": request.method, "path": str(request.url.path)}},
            )
            raise exc
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            status_code: Union[int, str] = response.status_code if response is not None else "n/a"
            self.logger.info(
                "HTTP request",
                extra={
                    "extra": {
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": status_code,
                        "duration_ms": round(duration_ms, 2),
                    }
                },
            )
            if response is not None:
                response.headers["X-Request-ID"] = request_id
