import logging
from sqlalchemy import text
from src.utils.db import get_engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

INIT_SQL = """
CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.weather_hourly (
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    latitude NUMERIC(6, 3) NOT NULL,
    longitude NUMERIC(6, 3) NOT NULL,
    temperature_2m NUMERIC(5, 2),
    relative_humidity_2m INTEGER,
    wind_speed_10m NUMERIC(5, 2),
    direct_normal_irradiance NUMERIC(7, 2),
    extracted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_raw_weather PRIMARY KEY (timestamp, latitude, longitude)
);
"""

def init_database() -> None:
    engine = get_engine()
    with engine.begin() as conn:
        logger.info("Инициализация схемы raw и таблицы weather_hourly...")
        conn.execute(text(INIT_SQL))
        logger.info("Таблицы успешно созданы.")

if __name__ == "__main__":
    init_database()
