"""Domain entity representing a capital city."""

from pydantic import BaseModel, ConfigDict, Field


class CapitalModel(BaseModel):
    """Capital domain model with location and population metadata."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "Tokyo",
                "country": "Japan",
                "population": 13929286,
                "lat": 35.6895,
                "lng": 139.6917,
            }
        },
    )

    name: str = Field(..., description="Capital name")
    country: str = Field(..., description="Country name this capital belongs to")
    population: int = Field(..., ge=0, description="Capital city population")
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lng: float = Field(..., ge=-180, le=180, description="Longitude")
