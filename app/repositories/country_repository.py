from pathlib import Path
from typing import Callable, List

from app.models import CountryModel
from app.utils import load_json_data


COUNTRY_REQUIRED_KEYS = [
    "name",
    "official_name",
    "country_code",
    "capital",
    "region",
    "subregion",
    "population",
    "area",
    "latitude",
    "longitude",
    "borders",
    "languages",
    "currencies",
]


class CountryRepository:
    def __init__(self, data_path: Path):
        self.data_path = data_path

    def _load(self) -> List[CountryModel]:
        raw = load_json_data(self.data_path, COUNTRY_REQUIRED_KEYS)
        return [CountryModel(**item) for item in raw]

    def get_all_countries(self) -> List[CountryModel]:
        return self._load()

    def get_country_by_code(self, code: str) -> CountryModel | None:
        code_lower = code.lower()
        for country in self._load():
            if country.country_code.lower() == code_lower:
                return country
        return None

    def get_by_region(self, region: str) -> List[CountryModel]:
        region_lower = region.lower()
        return [c for c in self._load() if c.region.lower() == region_lower]

    def get_by_subregion(self, subregion: str) -> List[CountryModel]:
        sub_lower = subregion.lower()
        return [c for c in self._load() if c.subregion.lower() == sub_lower]

    def search(self, predicate: Callable[[CountryModel], bool]) -> List[CountryModel]:
        return [c for c in self._load() if predicate(c)]

    def sort(self, items: List[CountryModel], field: str, descending: bool) -> List[CountryModel]:
        return sorted(items, key=lambda c: getattr(c, field), reverse=descending)

    def filter(self, predicate: Callable[[CountryModel], bool]) -> List[CountryModel]:
        return [c for c in self._load() if predicate(c)]
