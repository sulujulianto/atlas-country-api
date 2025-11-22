# Atlas Country API — Overview

Production-grade FastAPI backend providing rich data for countries and capitals with search, filtering, pagination, statistics, and consistent error handling.

## Highlights
- Layered architecture (routes → services → repositories → utils) with DTO schemas.
- Strict validation via Pydantic v2 schemas & domain models.
- JSON logging, request IDs, rate limiting, security headers, and CORS.
- Comprehensive tests (countries, capitals, statistics, errors, repos).
- Docker + GitHub Actions CI (lint, type-check, security scan, tests, coverage).

## Versioning Strategy
- Semantic versioning (`MAJOR.MINOR.PATCH`), reflected in `app/config/settings.py`.
- API path versioning reserved; current base at `/` with tags per resource.
- Release notes tracked in `docs/CHANGELOG.md`.

## Pagination & Sorting
- Query params: `page` (>=1), `size` (1–100), `sort_by`, `order=asc|desc`.
- Response includes `meta`: `{page, size, total_items, total_pages}`.

## Searching & Filtering
- Countries: `name`, `region`, `subregion`, `language`, `currency`, `min_population`, `max_population`, `min_area`, `max_area`.
- Capitals: `name` partial search; optional sort.
- Case-insensitive partial matches for text fields.

## Error Handling
Unified envelope:
```json
{
  "status": "error",
  "message": "Invalid sort field: foo",
  "code": "ERR_BAD_REQUEST",
  "details": {"field": "sort_by"}
}
```
Documented error codes in `docs/ENDPOINTS.md` and `docs/DATA_MODEL.md`.

## Security & Observability
- CORS configurable, security headers, basic rate limiting, input sanitization.
- JSON structured logging with request IDs and duration metrics.

## Performance
- Static JSON source cached per process.
- Lightweight filtering/sorting in services to keep repositories pure I/O.

## Runbook (short)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Tests & coverage:
```bash
pytest --maxfail=1 --disable-warnings
```
