from functools import lru_cache
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

    model_config = dict(extra="forbid")


@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()
