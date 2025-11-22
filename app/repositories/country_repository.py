"""Repository layer for countries: handles data loading and basic access."""

from pathlib import Path
from typing import Callable, List, Optional

from app.core.logging import get_logger
from app.exceptions import BadRequestError
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
    """Data access for countries backed by a JSON dataset."""

    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.logger = get_logger("atlas.repository.country")

    def _load(self) -> List[CountryModel]:
        """
        Load and validate country data from JSON.

        Raises:
            BadRequestError: if file missing or schema invalid.
        """
        try:
            raw = load_json_data(self.data_path, COUNTRY_REQUIRED_KEYS)
            return [CountryModel(**item) for item in raw]
        except BadRequestError:
            # propagate but ensure logged
            self.logger.error("Failed to load country data", exc_info=True)
            raise
        except Exception as exc:  # pydantic validation errors
            self.logger.error("Invalid country dataset", exc_info=True)
            raise BadRequestError("Invalid country dataset", {"error": str(exc)}) from exc

    def get_all_countries(self) -> List[CountryModel]:
        """Return all countries from the dataset."""
        return self._load()

    def get_country_by_code(self, code: str) -> Optional[CountryModel]:
        """Return a country by ISO code (case-insensitive), or None if not found."""
        code_lower = code.lower()
        for country in self._load():
            if country.country_code.lower() == code_lower:
                return country
        return None

    def get_by_region(self, region: str) -> List[CountryModel]:
        """Return countries matching a region (case-insensitive)."""
        region_lower = region.lower()
        return [c for c in self._load() if c.region.lower() == region_lower]

    def get_by_subregion(self, subregion: str) -> List[CountryModel]:
        """Return countries matching a subregion (case-insensitive)."""
        sub_lower = subregion.lower()
        return [c for c in self._load() if c.subregion.lower() == sub_lower]

    def search(self, predicate: Callable[[CountryModel], bool]) -> List[CountryModel]:
        """Return countries satisfying a predicate."""
        return [c for c in self._load() if predicate(c)]

    def sort(self, items: List[CountryModel], field: str, descending: bool) -> List[CountryModel]:
        """Sort a list of countries by a given field."""
        return sorted(items, key=lambda c: getattr(c, field), reverse=descending)

    def filter(self, predicate: Callable[[CountryModel], bool]) -> List[CountryModel]:
        """Filter countries by predicate."""
        return [c for c in self._load() if predicate(c)]
