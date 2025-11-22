from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ErrorSchema(BaseModel):
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

    status: str = Field("error", description="Response status")
    message: str = Field(..., description="Human-readable error message")
    code: str = Field(..., description="Application-specific error code")
    details: Optional[dict] = Field(default=None, description="Additional error details")


class ResponseSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "status": "success",
                "data": {"name": "Japan"},
                "meta": {"page": 1, "size": 10, "total_items": 200, "total_pages": 20},
                "error": None,
            }
        },
    )

    status: str = Field(..., description="Response status")
    data: Optional[Any] = Field(default=None, description="Payload")
    meta: Optional[dict] = Field(default=None, description="Metadata such as pagination")
    error: Optional[ErrorSchema] = Field(default=None, description="Error object if status=error")
