from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CountryModel(BaseModel):
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

    name: str = Field(...)
    official_name: str = Field(...)
    country_code: str = Field(..., min_length=2, max_length=3)
    capital: str = Field(...)
    region: str = Field(...)
    subregion: str = Field(...)
    population: int = Field(..., ge=0)
    area: float = Field(..., ge=0)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    borders: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    currencies: List[str] = Field(default_factory=list)
