# Atlas Country API

![CI](https://img.shields.io/github/actions/workflow/status/edo/atlas-country-api/backend-ci.yml?label=CI&logo=github)
![Coverage](https://img.shields.io/badge/coverage-90%25-green)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Production-ready FastAPI backend delivering rich country and capital data with layered architecture, strict validation, structured logging, and CI/CD.

## Demo
![Demo](https://img.shields.io/badge/demo-GIF-placeholder-blue)

## Features
- Countries: list/search/filter by region/subregion/language/currency, sort, paginate, get by code.
- Capitals: list/search/sort/paginate, get by name.
- Statistics: totals, top populations, region & language distribution.
- Strict DTO schemas, unified responses, documented error codes (`ERR_*`).
- Security: CORS, security headers, basic rate limiting, request IDs, structured JSON logs.
- Docker & GitHub Actions CI (lint, mypy, bandit, tests, coverage).

## Architecture (high level)
```
routes (controllers) -> services (business logic) -> repositories (data access) -> data/json
             ^            |-> utils (search, filters, pagination)  
             |            |-> exceptions (errors + handlers)  
             |-> schemas (DTOs)      models (domain entities)  
core (logging, security)  config (settings)
```

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Docker
```bash
docker-compose up --build
# or
docker build -t atlas-api . && docker run -p 8000:8000 atlas-api
```

# Running with Docker
Build the image:
```bash
docker build -t atlas-api .
```

Run the container:
```bash
docker run -p 8000:8000 atlas-api
# or for local dev with hot-reload:
docker-compose up --build
```

Access the API:
- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Tests & Coverage
```bash
pytest --maxfail=1 --disable-warnings
coverage run -m pytest && coverage report
```
Artifacts: `coverage.xml`, `pytest-report.html`, `htmlcov/`.

## Endpoint Preview
- Countries: `/countries`, `/countries/{code}`, `/countries/search`, `/countries/region/{region}`, `/countries/subregion/{subregion}`, `/countries/language/{language}`, `/countries/currency/{currency}`
- Capitals: `/capitals`, `/capitals/{name}`
- Statistics: `/statistics/totals`, `/statistics/top-population/largest`, `/statistics/top-population/smallest`, `/statistics/regions`, `/statistics/languages`
- Health: `/health`
Detailed tables in `docs/ENDPOINTS.md`.

## Data Model Example
```json
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

## Folder Structure
```
app/
 ├── main.py
 ├── config/
 ├── core/
 ├── routes/
 ├── services/
 ├── repositories/
 ├── models/
 ├── utils/
 └── exceptions/
schemas/
data/
tests/
docs/
.github/workflows/
```

## CI/CD
- Workflow: `.github/workflows/backend-ci.yml`
  - ruff, mypy, bandit
  - pytest + coverage (fail <85%)
  - artifacts: coverage.xml, pytest report, htmlcov

## Contribution
See `docs/CONTRIBUTING.md`.

## Roadmap
- JWT auth option
- ETags/caching
- Pluggable DB repository
- Observability dashboards
