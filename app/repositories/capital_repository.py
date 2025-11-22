"""Repository layer for capitals: handles data loading and basic access."""

from pathlib import Path
from typing import Callable, List, Optional

from app.core.logging import get_logger
from app.exceptions import BadRequestError
from app.models import CapitalModel
from app.utils import load_json_data


CAPITAL_REQUIRED_KEYS = ["name", "country", "population", "lat", "lng"]


class CapitalRepository:
    """Data access for capitals backed by a JSON dataset."""

    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.logger = get_logger("atlas.repository.capital")

    def _load(self) -> List[CapitalModel]:
        """
        Load and validate capital data from JSON.

        Raises:
            BadRequestError: if file missing or schema invalid.
        """
        try:
            raw = load_json_data(self.data_path, CAPITAL_REQUIRED_KEYS)
            return [CapitalModel(**item) for item in raw]
        except BadRequestError:
            self.logger.error("Failed to load capital data", exc_info=True)
            raise
        except Exception as exc:
            self.logger.error("Invalid capital dataset", exc_info=True)
            raise BadRequestError("Invalid capital dataset", {"error": str(exc)}) from exc

    def get_all_capitals(self) -> List[CapitalModel]:
        """Return all capitals from the dataset."""
        return self._load()

    def get_by_name(self, name: str) -> Optional[CapitalModel]:
        """Return a capital by name (case-insensitive), or None if not found."""
        name_lower = name.lower()
        for capital in self._load():
            if capital.name.lower() == name_lower:
                return capital
        return None

    def search(self, predicate: Callable[[CapitalModel], bool]) -> List[CapitalModel]:
        """Return capitals satisfying a predicate."""
        return [c for c in self._load() if predicate(c)]

    def sort(self, items: List[CapitalModel], field: str, descending: bool) -> List[CapitalModel]:
        """Sort a list of capitals by a given field."""
        return sorted(items, key=lambda c: getattr(c, field), reverse=descending)
