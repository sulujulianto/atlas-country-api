"""Utilities for safely loading and validating JSON datasets with caching."""

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, List, Optional

from app.exceptions import BadRequestError


def _validate_schema(data: Any, required_keys: Optional[List[str]] = None) -> None:
    """Validate data shape and required keys."""
    if required_keys is None:
        return
    if not isinstance(data, list):
        raise BadRequestError("Dataset must be a list of objects")
    for item in data:
        if not isinstance(item, dict):
            raise BadRequestError("Each dataset item must be an object")
        missing = [key for key in required_keys if key not in item]
        if missing:
            raise BadRequestError(f"Dataset item missing keys: {', '.join(missing)}")


def _load_file(path: Path) -> Any:
    """Load JSON file or raise BadRequestError if missing."""
    if not path.exists():
        raise BadRequestError(f"Data file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def cached_loader(path: Path, required_keys: Optional[List[str]] = None) -> Callable[[], Any]:
    """Return a cached loader callable to avoid re-reading files each call."""

    @lru_cache(maxsize=1)
    def _loader():
        data = _load_file(path)
        _validate_schema(data, required_keys)
        return data

    return _loader


def load_json_data(path: Path, required_keys: Optional[List[str]] = None) -> Any:
    """Load and validate JSON using a cached loader."""
    return cached_loader(path, required_keys)()
