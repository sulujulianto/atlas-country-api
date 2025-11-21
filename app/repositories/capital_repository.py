from pathlib import Path
from typing import Callable, List

from app.models import CapitalModel
from app.utils import load_json_data


CAPITAL_REQUIRED_KEYS = ["name", "country", "population", "lat", "lng"]


class CapitalRepository:
    def __init__(self, data_path: Path):
        self.data_path = data_path

    def _load(self) -> List[CapitalModel]:
        raw = load_json_data(self.data_path, CAPITAL_REQUIRED_KEYS)
        return [CapitalModel(**item) for item in raw]

    def get_all_capitals(self) -> List[CapitalModel]:
        return self._load()

    def get_by_name(self, name: str) -> CapitalModel | None:
        name_lower = name.lower()
        for capital in self._load():
            if capital.name.lower() == name_lower:
                return capital
        return None

    def search(self, predicate: Callable[[CapitalModel], bool]) -> List[CapitalModel]:
        return [c for c in self._load() if predicate(c)]

    def sort(self, items: List[CapitalModel], field: str, descending: bool) -> List[CapitalModel]:
        return sorted(items, key=lambda c: getattr(c, field), reverse=descending)
