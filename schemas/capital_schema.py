from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.models.capital_model import CapitalModel
from schemas.pagination_schema import PaginationMetaSchema


class CapitalResponseSchema(CapitalModel):
    model_config = CapitalModel.model_config


class CapitalListResponseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: List[CapitalResponseSchema] = Field(...)
    meta: PaginationMetaSchema = Field(...)
