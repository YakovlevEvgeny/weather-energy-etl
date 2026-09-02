# Weather & Renewable Energy ETL Pipeline

[![CI Pipeline](https://github.com/YakovlevEvgeny/weather-energy-etl/actions/workflows/ci.yml/badge.svg)](https://github.com/YakovlevEvgeny/weather-energy-etl/actions/workflows/ci.yml)

End-to-end production-grade ELT data pipeline for collecting, validating, and transforming meteorological data to estimate renewable energy potential (solar and wind).

---

## 🏗 Architecture Overview

```text
       [ Open-Meteo API ]
               │
               ▼  (HTTP + Tenacity Retry)
     [ Weather Extractor ]
               │
               ▼  (Pydantic v2 Schema Validation)
      [ Weather Loader ]
               │
               ▼  (Idempotent Upsert / ON CONFLICT)
     ┌────────────────────────────────────────────────────────┐
     │                PostgreSQL 15 Container                 │
     │                                                        │
     │   raw.weather_hourly                                   │
     │          │                                             │
     │          ▼  (dbt view)                                 │
     │   public_staging.stg_weather_hourly                    │
     │          │                                             │
     │          ▼  (dbt table aggregation)                    │
     │   public_marts.fct_daily_weather_energy                │
     └────────────────────────────────────────────────────────┘
