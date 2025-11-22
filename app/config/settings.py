import os
from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    app_name: str = Field("Atlas Country API", description="Application name")
    version: str = Field("2.0.0", description="API version")
    description: str = Field(
        "A production-grade REST API providing rich country and capital data with search, filtering, and statistics.",
        description="OpenAPI description",
    )
    contact_name: str = Field("Atlas Backend Team", description="Contact name")
    contact_email: str = Field("backend@atlas.example", description="Contact email")
    license_name: str = Field("MIT", description="License name")
    license_url: str = Field("https://opensource.org/licenses/MIT", description="License URL")
    environment: str = Field("dev", description="Environment name: dev/staging/prod")
    log_level: str = Field("INFO", description="Log level")
    cors_origins: List[str] = Field(default_factory=lambda: ["*"], description="Allowed CORS origins")
    rate_limit_per_minute: int = Field(60, ge=1, description="Simple in-memory rate limit per minute per client")

    model_config = dict(extra="forbid")

    @classmethod
    def from_env(cls) -> "AppSettings":
        origins_env = os.getenv("ATLAS_CORS_ORIGINS")
        if origins_env:
            cors_origins = [o.strip() for o in origins_env.split(",") if o.strip()]
        else:
            cors_origins = cls.model_fields["cors_origins"].default_factory() if cls.model_fields["cors_origins"].default_factory else ["*"]

        return cls(
            app_name=os.getenv("ATLAS_APP_NAME", cls.model_fields["app_name"].default),
            version=os.getenv("ATLAS_VERSION", cls.model_fields["version"].default),
            description=os.getenv("ATLAS_DESCRIPTION", cls.model_fields["description"].default),
            contact_name=os.getenv("ATLAS_CONTACT_NAME", cls.model_fields["contact_name"].default),
            contact_email=os.getenv("ATLAS_CONTACT_EMAIL", cls.model_fields["contact_email"].default),
            license_name=os.getenv("ATLAS_LICENSE_NAME", cls.model_fields["license_name"].default),
            license_url=os.getenv("ATLAS_LICENSE_URL", cls.model_fields["license_url"].default),
            environment=os.getenv("ATLAS_ENV", cls.model_fields["environment"].default),
            log_level=os.getenv("ATLAS_LOG_LEVEL", cls.model_fields["log_level"].default),
            cors_origins=cors_origins,
            rate_limit_per_minute=int(os.getenv("ATLAS_RATE_LIMIT_PER_MINUTE", cls.model_fields["rate_limit_per_minute"].default)),
        )


@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings.from_env()
