# Atlas Country API

Backend FastAPI sederhana untuk informasi negara dan ibu kota dengan pencarian, filter, statistik dasar, dan dokumentasi otomatis. Proyek ini disusun rapi agar mudah dipelajari, diuji, dan dipamerkan sebagai portofolio backend.

## Fitur
- `/health` untuk pengecekan cepat service.
- `/api/v1/countries` list negara dengan pagination, filter `region`, dan pencarian `search` pada nama/ibu kota.
- Detail negara: `/by-code/{code}` dan `/by-name/{name}`.
- Ringkasan wilayah: `/api/v1/countries/regions`.
- Negara acak: `/api/v1/countries/random`.
- Statistik: `/api/v1/statistics/population/largest`, `/api/v1/statistics/name-length/longest`, dan `/api/v1/statistics/regions/counts`.
- Swagger UI (`/docs`) dan ReDoc (`/redoc`).

## Konfigurasi API Key
Semua endpoint `/api/v1/...` meminta header `x-api-key`. Default kunci demo: `atlas-demo-key`. Ganti via environment `ATLAS_API_KEY` jika ingin nilai lain.
```
export ATLAS_API_KEY=isi-kunci-anda       # atau di .env (di-ignore git)
```
Gunakan header saat memanggil API:
```
x-api-key: atlas-demo-key   # atau nilai ATLAS_API_KEY yang Anda set
```

## Menjalankan Lokal
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Pengujian
```bash
pytest
```

## Struktur Proyek
```text
app/
├── core/                 # Logging & exception handlers
├── models/               # Pydantic schemas
├── routes/               # FastAPI routers
├── services/             # Akses & utilitas data negara
└── main.py               # FastAPI app factory & router registration
data/
└── capitals.json         # Dataset statis
tests/
└── test_endpoints.py     # Uji integrasi endpoint dengan httpx
requirements.txt
readme.md
```
