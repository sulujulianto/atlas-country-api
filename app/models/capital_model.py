from pydantic import BaseModel, ConfigDict, Field


class CapitalModel(BaseModel):
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

    name: str = Field(...)
    country: str = Field(...)
    population: int = Field(..., ge=0)
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
