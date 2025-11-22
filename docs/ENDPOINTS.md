# Atlas Country API – Endpoints

FastAPI service providing country and capital data with search, filtering, sorting, pagination, and basic statistics. All responses use a consistent envelope:

```json
{
  "status": "success",
  "data": {...},      // payload
  "meta": {...},      // pagination metadata (when applicable)
  "error": null       // or error object when status="error"
}
```

Error envelope:
```json
{
  "status": "error",
  "message": "Invalid sort field: foo",
  "code": "ERR_BAD_REQUEST",
  "details": {"field": "sort_by"}
}
```

Common query parameters
- Pagination: `page` (>=1), `size` (1–100).
- Sorting: `sort_by`, `order=asc|desc`.
- Search/filter (countries): `name`, `region`, `subregion`, `min_population`, `max_population`, `min_area`, `max_area`, `language`, `currency`.
- Search/filter (capitals): `name`, `sort_by`, `order`.

## Countries

| Method | Path | Description |
| --- | --- | --- |
| GET | `/countries` | List countries with search/filter/sort/pagination |
| GET | `/countries/{code}` | Get country by ISO code |
| GET | `/countries/search` | Advanced search (same params as list) |
| GET | `/countries/region/{region}` | Filter by region |
| GET | `/countries/subregion/{subregion}` | Filter by subregion |
| GET | `/countries/language/{language}` | Filter by language |
| GET | `/countries/currency/{currency}` | Filter by currency |

**Parameters (for list/search):**
- `page`, `size`
- `name`, `region`, `subregion`
- `min_population`, `max_population`, `min_area`, `max_area`
- `language`, `currency`
- `sort_by` (any CountryModel field), `order=asc|desc`

**Example request**
```bash
curl "http://127.0.0.1:8000/countries?region=Europe&sort_by=population&order=desc&page=1&size=5"
```

**Example response**
```json
{
  "status": "success",
  "data": [
    {"name":"France","official_name":"French Republic","country_code":"FR","capital":"Paris","region":"Europe","subregion":"Western Europe","population":67413000,"area":551695.0,"latitude":48.8566,"longitude":2.3522,"borders":["BEL","DEU","CHE","ITA","ESP","LUX"],"languages":["French"],"currencies":["EUR"]},
    {"name":"Germany","official_name":"Federal Republic of Germany","country_code":"DE","capital":"Berlin","region":"Europe","subregion":"Western Europe","population":83240525,"area":357022.0,"latitude":52.52,"longitude":13.405,"borders":["POL","CZE","AUS","CHE","FRA","LUX","BEL","NLD","DNK"],"languages":["German"],"currencies":["EUR"]}
  ],
  "meta": {"page":1,"size":5,"total_items":2,"total_pages":1},
  "error": null
}
```

**Errors**
- 400 `ERR_BAD_REQUEST`: invalid sort field, rate limit exceeded, bad input.
- 404 `ERR_NOT_FOUND`: country not found.
- 422 `ERR_VALIDATION`: invalid query/body.
- 500 `ERR_INTERNAL`: unexpected server error.

## Capitals

| Method | Path | Description |
| --- | --- | --- |
| GET | `/capitals` | List capitals with search/sort/pagination |
| GET | `/capitals/{name}` | Get capital by name |

**Parameters (list):**
- `page`, `size`
- `name`
- `sort_by` (e.g., population), `order=asc|desc`

**Example request**
```bash
curl "http://127.0.0.1:8000/capitals?name=to&sort_by=population&order=desc&page=1&size=3"
```

**Example response**
```json
{
  "status":"success",
  "data":[
    {"name":"Tokyo","country":"Japan","population":13929286,"lat":35.6895,"lng":139.6917},
    {"name":"Jakarta","country":"Indonesia","population":10770487,"lat":-6.2088,"lng":106.8456}
  ],
  "meta":{"page":1,"size":3,"total_items":2,"total_pages":1},
  "error":null
}
```

**Errors**
- 400 `ERR_BAD_REQUEST`: invalid sort field.
- 404 `ERR_NOT_FOUND`: capital not found.
- 422 `ERR_VALIDATION`: invalid query/body.
- 500 `ERR_INTERNAL`: unexpected server error.

## Statistics

| Method | Path | Description |
| --- | --- | --- |
| GET | `/statistics/totals` | Total countries and capitals |
| GET | `/statistics/top-population/largest` | Top N largest populations (param `limit`) |
| GET | `/statistics/top-population/smallest` | Top N smallest populations (param `limit`) |
| GET | `/statistics/regions` | Region distribution |
| GET | `/statistics/languages` | Language distribution |

**Example request**
```bash
curl "http://127.0.0.1:8000/statistics/top-population/largest?limit=3"
```

**Errors**
- 400 `ERR_BAD_REQUEST`: invalid limit (if service-level validation fails).
- 422 `ERR_VALIDATION`: limit outside allowed bounds.
- 500 `ERR_INTERNAL`: unexpected server error.

## Health

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | Health check |

**Response**
```json
{"status":"success","data":{"status":"ok"},"meta":null,"error":null}
```
