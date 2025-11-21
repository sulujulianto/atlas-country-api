import json
from functools import lru_cache
from pathlib import Path
from random import choice
from typing import Dict, List, Optional

from app.models import Country, RegionSummary

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "capitals.json"


class DataSourceError(RuntimeError):
    """Raised when the country dataset cannot be found or read."""


@lru_cache(maxsize=1)
def _load_dataset() -> List[Country]:
    if not DATA_PATH.exists():
        raise DataSourceError(f"Data file not found at {DATA_PATH}")

    with open(DATA_PATH, "r") as file:
        payload = json.load(file)

    data = payload.get("countries")
    if data is None:
        raise DataSourceError("Dataset is missing 'countries' key")

    return [Country(**item) for item in data]


def get_countries() -> List[Country]:
    # Return a shallow copy so callers cannot mutate the cached list.
    return list(_load_dataset())


def filter_countries(region: Optional[str] = None, search: Optional[str] = None) -> List[Country]:
    countries = get_countries()

    if region:
        region_lower = region.lower()
        countries = [
            country
            for country in countries
            if country.region and country.region.lower() == region_lower
        ]

    if search:
        term = search.lower()
        countries = [
            country
            for country in countries
            if term in country.name.lower() or term in country.capital.lower()
        ]

    return countries


def get_region_summaries(countries: List[Country]) -> List[RegionSummary]:
    region_counts: Dict[str, int] = {}
    for country in countries:
        if not country.region:
            continue

        region_name = country.region.strip()
        if not region_name:
            continue

        region_counts[region_name] = region_counts.get(region_name, 0) + 1

    return [
        RegionSummary(region=name, country_count=count)
        for name, count in sorted(region_counts.items())
    ]


def find_by_code(country_code: str) -> Optional[Country]:
    target = country_code.lower()
    for country in get_countries():
        if country.code.lower() == target:
            return country
    return None


def find_by_name(country_name: str) -> Optional[Country]:
    target = country_name.lower()
    for country in get_countries():
        if country.name.lower() == target:
            return country
    return None


def random_country() -> Optional[Country]:
    countries = get_countries()
    if not countries:
        return None
    return choice(countries)


def largest_population_country() -> Optional[Country]:
    return max(get_countries(), key=lambda country: country.population or 0, default=None)


def longest_name_country() -> Optional[Country]:
    return max(get_countries(), key=lambda country: len(country.name), default=None)
