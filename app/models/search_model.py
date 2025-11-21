from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class SearchQueryModel(BaseModel):
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

    name: Optional[str] = Field(None)
    region: Optional[str] = Field(None)
    subregion: Optional[str] = Field(None)
    min_population: Optional[int] = Field(None, ge=0)
    max_population: Optional[int] = Field(None, ge=0)
    min_area: Optional[float] = Field(None, ge=0)
    max_area: Optional[float] = Field(None, ge=0)
    language: Optional[str] = Field(None)
    currency: Optional[str] = Field(None)
    sort_by: Optional[str] = Field(None, description="Field name to sort by")
    order: Literal["asc", "desc"] = Field("asc")
