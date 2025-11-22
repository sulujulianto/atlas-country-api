"""Domain pagination models for reuse in services and repositories."""

from math import ceil
from pydantic import BaseModel, ConfigDict, Field


class PaginationModel(BaseModel):
    """Pagination parameters for requests."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"example": {"page": 1, "size": 10}},
    )

    page: int = Field(1, ge=1, description="Page number (1-indexed).")
    size: int = Field(10, ge=1, le=100, description="Page size.")


class PaginationMetaModel(BaseModel):
    """Pagination metadata returned alongside list responses."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {"page": 1, "size": 10, "total_items": 250, "total_pages": 25}
        },
    )

    page: int = Field(..., description="Current page number.")
    size: int = Field(..., description="Page size.")
    total_items: int = Field(..., ge=0, description="Total matched items.")
    total_pages: int = Field(..., ge=0, description="Computed total pages.")

    @classmethod
    def from_counts(cls, page: int, size: int, total_items: int) -> "PaginationMetaModel":
        total_pages = ceil(total_items / size) if size else 0
        return cls(page=page, size=size, total_items=total_items, total_pages=total_pages)
