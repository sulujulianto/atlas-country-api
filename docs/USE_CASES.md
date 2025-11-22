# Use Cases

## Public Catalogue
- List countries with pagination and search; filter by region/subregion for a catalogue view.
- Show capitals with quick lookups.

## Analytics Dashboard
- Top 5 population charts (largest/smallest) via `/statistics/top-population/*`.
- Region and language distribution for map visualizations.

## Travel/Logistics
- Query by currency/language to plan routes or services.
- Filter by population/area ranges to segment markets.

## Monitoring
- Health endpoint `/health` for uptime checks.
- Structured logs + request IDs for tracing.
- Rate limiting to protect from abuse.

## Extensibility
- Swap repositories to use a database without touching services/routes.
- Add JWT auth by injecting dependency into routers.
- Extend schemas for new fields; services remain the orchestration layer.
