from typing import List, Optional

from pydantic import BaseModel


class Country(BaseModel):
    code: str
    name: str
    capital: str
    region: Optional[str] = None
    population: Optional[int] = None


class CountryListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[Country]


class RegionSummary(BaseModel):
    region: str
    country_count: int


class ErrorResponse(BaseModel):
    detail: str
