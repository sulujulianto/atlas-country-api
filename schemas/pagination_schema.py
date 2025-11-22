from math import ceil

from pydantic import BaseModel, ConfigDict, Field


class PaginationRequestSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"example": {"page": 1, "size": 10}},
    )

    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    size: int = Field(10, ge=1, le=100, description="Page size")


class PaginationMetaSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"example": {"page": 1, "size": 10, "total_items": 250, "total_pages": 25}},
    )

    page: int = Field(..., description="Current page")
    size: int = Field(..., description="Page size")
    total_items: int = Field(..., ge=0, description="Total number of items")
    total_pages: int = Field(..., ge=0, description="Total number of pages")

    @classmethod
    def from_counts(cls, page: int, size: int, total_items: int) -> "PaginationMetaSchema":
        total_pages = ceil(total_items / size) if size else 0
        return cls(page=page, size=size, total_items=total_items, total_pages=total_pages)
