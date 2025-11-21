# Atlas Country API

Production-grade REST API built with FastAPI delivering rich country and capital data, with layered architecture, validation, pagination, sorting, filtering, and comprehensive tests.

## Overview
- Layered design: routes → services → repositories → utils, with strict typing and schema validation.
- Rich data domain: countries (region, subregion, borders, languages, currencies, geo, population, area) and capitals.
- Professional OpenAPI docs with contact, license, tags, and examples.
- Robust error handling and consistent response envelope.

## Features
- Countries: list, search, region/subregion/language/currency filters, sorting, pagination, get by code.
- Capitals: list with search/sort/pagination, get by name.
- Validation: strict Pydantic models, query validation, and custom errors (400/404/422).
- Error responses are structured with `status`, `code`, `message`, and `details`.
- Data loaded from JSON with schema checks and caching.

## Tech Stack
- FastAPI + Uvicorn
- Pydantic v2 for strict models
- pytest for automated tests
- JSON data source (no DB dependency)

## Data Model Examples
```json
// CountryModel
{
  "name": "Indonesia",
  "official_name": "Republic of Indonesia",
  "country_code": "ID",
  "capital": "Jakarta",
  "region": "Asia",
  "subregion": "South-Eastern Asia",
  "population": 273523621,
  "area": 1904569.0,
  "latitude": -6.2,
  "longitude": 106.8,
  "borders": ["MYS", "TLS", "PNG"],
  "languages": ["Indonesian"],
  "currencies": ["IDR"]
}
```

## Endpoints (high level)
- Countries:
  - `GET /countries` (pagination, sort, filters, search)
  - `GET /countries/{code}`
  - `GET /countries/search`
  - `GET /countries/region/{region}`
  - `GET /countries/subregion/{subregion}`
  - `GET /countries/language/{language}`
  - `GET /countries/currency/{currency}`
- Capitals:
  - `GET /capitals`
  - `GET /capitals/{name}`
- Health:
  - `GET /health`

## Example Usage
List European countries, sorted by population descending:
```bash
curl "http://127.0.0.1:8000/countries?region=Europe&sort_by=population&order=desc&page=1&size=10"
```

Search by name with population filter:
```bash
curl "http://127.0.0.1:8000/countries/search?name=an&min_population=50000000"
```

Get capital by name:
```bash
curl "http://127.0.0.1:8000/capitals/Tokyo"
```

## Run Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Testing
```bash
pytest
```

## Folder Structure
```
app/
 ├── main.py
 ├── config/
 ├── routes/
 ├── services/
 ├── repositories/
 ├── models/
 ├── utils/
 └── exceptions/
data/
tests/
```

## Contribution Guide
- Use feature branches and open PRs with clear descriptions.
- Keep coverage by adding/maintaining tests for new code paths.
- Follow PEP8 and run `pytest` before submitting.

## Roadmap
- Add authentication/authorization layer.
- Add caching headers and ETags.
- Plug-in external datasets or database backend.
- Add CI pipeline (lint + tests). 
