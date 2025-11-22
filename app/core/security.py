import time
from typing import Callable, Dict

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.config.settings import get_settings
from app.exceptions.http_errors import BadRequestError
from app.core.logging import get_logger


def configure_cors(app):
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        return response


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.settings = get_settings()
        self.bucket: Dict[str, Dict[str, float]] = {}
        self.logger = get_logger("atlas.ratelimit")

    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = request.client.host if request.client else "anonymous"
        now = time.time()
        window = 60  # seconds
        limit = self.settings.rate_limit_per_minute
        entry = self.bucket.get(client_ip, {"count": 0, "window_start": now})
        if now - entry["window_start"] > window:
            entry = {"count": 0, "window_start": now}
        entry["count"] += 1
        self.bucket[client_ip] = entry
        if entry["count"] > limit:
            self.logger.warning("rate limit exceeded", extra={"extra": {"client_ip": client_ip}})
            raise BadRequestError("Rate limit exceeded", {"client_ip": client_ip})
        return await call_next(request)


def sanitize_query(params: dict) -> dict:
    sanitized = {}
    for k, v in params.items():
        if isinstance(v, str):
            sanitized[k] = v.strip()
        else:
            sanitized[k] = v
    return sanitized
