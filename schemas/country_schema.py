from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.models.country_model import CountryModel
from schemas.pagination_schema import PaginationMetaSchema


class CountryResponseSchema(CountryModel):
    model_config = CountryModel.model_config


class CountryListResponseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: List[CountryResponseSchema] = Field(...)
    meta: PaginationMetaSchema = Field(...)
