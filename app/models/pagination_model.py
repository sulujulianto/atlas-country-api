from math import ceil
from pydantic import BaseModel, ConfigDict, Field


class PaginationRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"example": {"page": 1, "size": 10}},
    )

    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)


class PaginationMeta(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"example": {"page": 1, "size": 10, "total_items": 250, "total_pages": 25}},
    )

    page: int = Field(...)
    size: int = Field(...)
    total_items: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=0)

    @classmethod
    def from_counts(cls, page: int, size: int, total_items: int) -> "PaginationMeta":
        total_pages = ceil(total_items / size) if size else 0
        return cls(page=page, size=size, total_items=total_items, total_pages=total_pages)
