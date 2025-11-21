from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ErrorModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {"code": 404, "message": "Resource not found", "details": {"resource": "country"}}
        },
    )

    code: int = Field(...)
    message: str = Field(...)
    details: Optional[dict] = Field(None)


class ResponseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "status": "success",
                "data": {"name": "Japan"},
                "meta": {"page": 1, "size": 10, "total": 100},
                "error": None,
            }
        },
    )

    status: str = Field(...)
    data: Optional[Any] = Field(None)
    meta: Optional[dict] = Field(None)
    error: Optional[ErrorModel] = None
