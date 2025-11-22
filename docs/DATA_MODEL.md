# Data Model

## Domain Entities (`app/models`)
- `CountryModel`: strict entity with geography, population, languages, currencies, borders.
- `CapitalModel`: strict entity with coordinates and population.

## DTO Schemas (`schemas`)
- `PaginationRequestSchema` / `PaginationMetaSchema`
- `SearchQuerySchema`
- `ResponseSchema` / `ErrorSchema`
- `CountryResponseSchema`, `CountryListResponseSchema`
- `CapitalResponseSchema`, `CapitalListResponseSchema`

### CountryModel Fields
| Field | Type | Rules | Example |
| --- | --- | --- | --- |
| name | str | required | "Indonesia" |
| official_name | str | required | "Republic of Indonesia" |
| country_code | str | len 2-3 | "ID" |
| capital | str | required | "Jakarta" |
| region | str | required | "Asia" |
| subregion | str | required | "South-Eastern Asia" |
| population | int | >=0 | 273523621 |
| area | float | >=0 | 1904569.0 |
| latitude | float | -90..90 | -6.2 |
| longitude | float | -180..180 | 106.8 |
| borders | list[str] | optional | ["MYS","TLS","PNG"] |
| languages | list[str] | optional | ["Indonesian"] |
| currencies | list[str] | optional | ["IDR"] |

### CapitalModel Fields
| Field | Type | Rules | Example |
| --- | --- | --- | --- |
| name | str | required | "Tokyo" |
| country | str | required | "Japan" |
| population | int | >=0 | 13929286 |
| lat | float | -90..90 | 35.6895 |
| lng | float | -180..180 | 139.6917 |

### Pagination
Request: `page>=1`, `size` 1–100.  
Meta response: `{page, size, total_items, total_pages}` (ceil rule).

### Search / Filter Rules
- Text: case-insensitive, partial match.
- Region/Subregion: exact match case-insensitive.
- Numeric ranges: inclusive (`min_population`, `max_population`, `min_area`, `max_area`).
- List membership: languages, currencies exact match (case-insensitive).
- Sorting: any model field; order `asc|desc`; invalid triggers `ERR_BAD_REQUEST`.

### Error Codes
Documented in `docs/ENDPOINTS.md`; envelope:
```json
{
  "status": "error",
  "message": "Rate limit exceeded",
  "code": "ERR_BAD_REQUEST",
  "details": {"client_ip":"127.0.0.1"}
}
```

### Analytics Data
- Derived from `data/countries.json` and `data/capitals.json`.
- Statistics: totals, top populations, region and language distribution.***
