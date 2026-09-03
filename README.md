# 🌤️ Weather & Renewable Energy ELT Pipeline

[![CI Pipeline](https://github.com/YakovlevEvgeny/weather-energy-etl/actions/workflows/ci.yml/badge.svg)](https://github.com/YakovlevEvgeny/weather-energy-etl/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![PostgreSQL 15](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![dbt](https://img.shields.io/badge/dbt-core-FF694B.svg)](https://www.getdbt.com/)
[![Docker](https://img.shields.io/badge/docker-compose-2496ED.svg)](https://www.docker.com/)

End-to-end automated ELT pipeline collecting hourly meteorological metrics and computing daily renewable solar & wind energy generation potentials.

---

## 🏛️ Architecture Overview

The pipeline implements an **ELT (Extract-Load-Transform)** pattern:

1. **Extract & Validate (Python + Pydantic v2):**
   * Ingestion from Open-Meteo REST API with resilient retries via `tenacity`.
   * Strict physical domain validation: relative humidity (0–100%), non-negative wind speeds and solar irradiance.
2. **Load & Idempotency (PostgreSQL 15):**
   * Loaded into raw schema (`raw.weather_hourly`).
   * Guaranteed idempotency using composite Primary Key `(timestamp, latitude, longitude)` with `ON CONFLICT DO UPDATE` (Upsert).
3. **Transform (dbt):**
   * **Staging Layer (`stg_weather_hourly`):** Coordinate mapping to city dimensions and hourly power physical calculations. Materialized as a `view`.
   * **Marts Layer (`fct_daily_weather_energy`):** Aggregation to daily resolution, computing mean temperatures and total energy metrics. Materialized as a `table`.
4. **Automation & Quality (CI/CD):**
   * Continuous integration pipeline on GitHub Actions: linting (`ruff`), unit tests (`pytest`), and end-to-end `dbt run` / `dbt test` execution against a containerized PostgreSQL instance.

```text
[ Open-Meteo API ]
        │
        ▼ (Extract: Python + Tenacity)
[ Raw JSON Data ]
        │
        ▼ (Validate: Pydantic v2)
[ Validated Records ]
        │
        ▼ (Load: Upsert / Idempotent)
[ PostgreSQL: raw.weather_hourly ]
        │
        ▼ (dbt run: Views)
[ Staging: stg_weather_hourly ]
        │
        ▼ (dbt run: Tables)
[ Marts: fct_daily_weather_energy ]
        │
        ▼ (dbt test)
[ Quality Checks: not_null, unique ]
