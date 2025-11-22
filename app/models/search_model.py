"""Domain search model capturing filters and sorting preferences."""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class SearchModel(BaseModel):
    """Search and filter criteria for country/capital lookups."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "indo",
                "region": "Asia",
                "subregion": "South-Eastern Asia",
                "min_population": 1000000,
                "max_population": 500000000,
                "min_area": 1000.0,
                "max_area": 2000000.0,
                "language": "Indonesian",
                "currency": "IDR",
                "sort_by": "population",
                "order": "desc",
            }
        },
    )

    name: Optional[str] = Field(None, description="Partial, case-insensitive match on name/official_name/capital.")
    region: Optional[str] = Field(None, description="Region filter.")
    subregion: Optional[str] = Field(None, description="Subregion filter.")
    min_population: Optional[int] = Field(None, ge=0, description="Minimum population.")
    max_population: Optional[int] = Field(None, ge=0, description="Maximum population.")
    min_area: Optional[float] = Field(None, ge=0, description="Minimum area.")
    max_area: Optional[float] = Field(None, ge=0, description="Maximum area.")
    language: Optional[str] = Field(None, description="Language filter.")
    currency: Optional[str] = Field(None, description="Currency filter.")
    sort_by: Optional[str] = Field(None, description="Field to sort by.")
    order: Literal["asc", "desc"] = Field("asc", description="Sort order.")
