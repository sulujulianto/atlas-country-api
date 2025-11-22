"""Domain entity representing a country with geography, demographics, and attributes."""

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CountryModel(BaseModel):
    """Country domain model used across repositories and services."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "Indonesia",
                "official_name": "Republic of Indonesia",
                "country_code": "ID",
                "capital": "Jakarta",
                "region": "Asia",
                "subregion": "South-Eastern Asia",
                "population": 273523621,
                "area": 1904569.0,
                "latitude": -6.2,
                "longitude": 106.8,
                "borders": ["MYS", "TLS", "PNG"],
                "languages": ["Indonesian"],
                "currencies": ["IDR"],
            }
        },
    )

    name: str = Field(..., description="Common name of the country")
    official_name: str = Field(..., description="Official long-form name")
    country_code: str = Field(..., min_length=2, max_length=3, description="ISO country code (alpha-2/alpha-3)")
    capital: str = Field(..., description="Capital city name")
    region: str = Field(..., description="Geographic region (e.g., Asia, Europe)")
    subregion: str = Field(..., description="More specific subregion")
    population: int = Field(..., ge=0, description="Total population")
    area: float = Field(..., ge=0, description="Total land area in square kilometers")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude of capital or centroid")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude of capital or centroid")
    borders: List[str] = Field(default_factory=list, description="List of bordering country codes")
    languages: List[str] = Field(default_factory=list, description="Official or major languages")
    currencies: List[str] = Field(default_factory=list, description="Currencies used")
