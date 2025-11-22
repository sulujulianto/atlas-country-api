import json
from pathlib import Path

import pytest

from app.exceptions import BadRequestError
from app.repositories import CountryRepository


def test_repository_missing_file(tmp_path: Path):
    missing = tmp_path / "missing.json"
    repo = CountryRepository(missing)
    with pytest.raises(BadRequestError):
        repo.get_all_countries()


def test_repository_invalid_schema(tmp_path: Path):
    invalid_file = tmp_path / "countries.json"
    invalid_file.write_text(json.dumps([{"name": "X"}]))
    repo = CountryRepository(invalid_file)
    with pytest.raises(BadRequestError):
        repo.get_all_countries()
