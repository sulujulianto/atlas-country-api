# Project Architecture

## Layering (Atlas Country API)
```
config/        # settings, environment
core/          # logging, security middleware
exceptions/    # domain errors + handlers
models/        # domain entities (Country, Capital, Pagination, Search, Response)
repositories/  # data access (JSON loading, validation)
services/      # business logic (search, filter, sort, pagination, stats)
routes/        # HTTP controllers (FastAPI)
schemas/       # DTOs (request/response), if needed by HTTP layer
utils/         # helpers (json loader, filters, search, pagination)
data/          # JSON data source
tests/         # automated tests
```

## Responsibilities
- **config**: Centralized settings (env-driven).
- **models**: Core domain definitions, strict Pydantic models used internally.
- **repositories**: I/O and schema validation; no business logic. Reads JSON from `data/` and raises domain errors on invalid/missing data.
- **services**: Pure business logic; orchestrates search/filter/sort/pagination, stats; no HTTP concerns.
- **routes**: Thin FastAPI controllers; parse query/path params, call services, wrap into response envelope.
- **utils**: Reusable helpers (normalize text, filters, pagination meta, cached JSON loader).
- **exceptions**: Custom errors and global handlers with consistent error envelope.
- **core**: Cross-cutting concerns like logging (JSON, request IDs) and security middleware (CORS, headers, rate limiting).

## Data Flow (request to response)
1. **HTTP request** enters a FastAPI route (controller).
2. Route parses query/path params (pagination, filters, etc.) and sanitizes basic strings.
3. Route constructs domain models/DTOs (e.g., `SearchModel`, `PaginationModel`) and calls a **service**.
4. Service runs business logic, calling **repositories** to fetch domain entities from JSON.
5. Repository loads data via `utils/json_loader.py`, validates required keys; returns `CountryModel` / `CapitalModel` instances.
6. Service applies search/filter/sort/pagination helpers from **utils** and returns domain entities + pagination meta.
7. Route wraps results into a consistent **response envelope** and returns HTTP response.

## Error Handling
- Domain errors (`ERR_BAD_REQUEST`, `ERR_NOT_FOUND`, `ERR_VALIDATION`, `ERR_INTERNAL`) are defined in **exceptions** and surfaced via global handlers.
- Routes should not leak raw exceptions; services/repositories raise domain errors; handlers convert to `{status, message, code, details}`.

## Logging
- Implemented in **core/logging.py** as JSON logs with request IDs and duration metrics.
- Middleware injects `X-Request-ID` and logs method/path/status/duration.
- Log level/env configured in settings.

## Pagination & Search (high level)
- Pagination params: `page`, `size`; pagination meta computed via helper (`utils/pagination.py`) returning `{page, size, total_items, total_pages}`.
- Search/filter: case-insensitive partial match for text (`utils/search.py`), numeric ranges and list membership filters (`utils/filters.py`).
- Services orchestrate these helpers and ensure sorting fields are validated against domain model fields.
