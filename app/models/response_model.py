"""Domain response envelope models used internally."""

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ErrorDetailModel(BaseModel):
    """Represents an application error."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "status": "error",
                "message": "Invalid sort field: foo",
                "code": "ERR_BAD_REQUEST",
                "details": {"field": "sort_by"},
            }
        },
    )

    status: str = Field("error", description="Response status.")
    message: str = Field(..., description="Human-readable error message.")
    code: str = Field(..., description="Application-specific error code.")
    details: Optional[dict] = Field(default=None, description="Additional context.")


class ResponseModel(BaseModel):
    """Canonical response envelope for services/controllers."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "status": "success",
                "data": {"name": "Japan"},
                "meta": {"page": 1, "size": 10, "total_items": 100, "total_pages": 10},
                "error": None,
            }
        },
    )

    status: str = Field(..., description="success or error.")
    data: Optional[Any] = Field(default=None, description="Payload data.")
    meta: Optional[dict] = Field(default=None, description="Metadata such as pagination.")
    error: Optional[ErrorDetailModel] = Field(default=None, description="Error payload when status=error.")
