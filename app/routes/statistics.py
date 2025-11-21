from fastapi import APIRouter, Depends, HTTPException

from app.core.security import verify_api_key
from app.models import Country
from app.services import country_service
from app.services.country_service import DataSourceError

router = APIRouter(
    prefix="/api/v1/statistics",
    tags=["Statistics"],
    dependencies=[Depends(verify_api_key)],
)


@router.get("/population/largest", response_model=Country)
def largest_population():
    try:
        country = country_service.largest_population_country()
    except DataSourceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if not country:
        raise HTTPException(status_code=404, detail="No countries available")

    return country


@router.get("/regions/counts")
def region_counts():
    try:
        countries = country_service.get_countries()
    except DataSourceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    summaries = country_service.get_region_summaries(countries)
    return {summary.region: summary.country_count for summary in summaries}


@router.get("/name-length/longest", response_model=Country)
def longest_name():
    try:
        country = country_service.longest_name_country()
    except DataSourceError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if not country:
        raise HTTPException(status_code=404, detail="No countries available")

    return country
