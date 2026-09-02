import logging
from datetime import datetime
from sqlalchemy import text
from src.extractors.schemas import WeatherApiResponse
from src.utils.db import get_engine

logger = logging.getLogger(__name__)

UPSERT_QUERY = """
INSERT INTO raw.weather_hourly (
    timestamp, latitude, longitude, 
    temperature_2m, relative_humidity_2m, 
    wind_speed_10m, direct_normal_irradiance, extracted_at
) VALUES (
    :timestamp, :latitude, :longitude, 
    :temperature_2m, :relative_humidity_2m, 
    :wind_speed_10m, :direct_normal_irradiance, :extracted_at
)
ON CONFLICT (timestamp, latitude, longitude) 
DO UPDATE SET
    temperature_2m = EXCLUDED.temperature_2m,
    relative_humidity_2m = EXCLUDED.relative_humidity_2m,
    wind_speed_10m = EXCLUDED.wind_speed_10m,
    direct_normal_irradiance = EXCLUDED.direct_normal_irradiance,
    extracted_at = EXCLUDED.extracted_at;
"""

class WeatherLoader:
    def __init__(self):
        self.engine = get_engine()

    def load(self, data: WeatherApiResponse) -> int:
        """Загружает валидированные записи в PostgreSQL с защитой от дублирования."""
        records = []
        now = datetime.utcnow()
        hourly = data.hourly

        for i in range(len(hourly.time)):
            records.append({
                "timestamp": hourly.time[i],
                "latitude": round(data.latitude, 3),
                "longitude": round(data.longitude, 3),
                "temperature_2m": hourly.temperature_2m[i],
                "relative_humidity_2m": hourly.relative_humidity_2m[i],
                "wind_speed_10m": hourly.wind_speed_10m[i],
                "direct_normal_irradiance": hourly.direct_normal_irradiance[i],
                "extracted_at": now
            })

        with self.engine.begin() as conn:
            conn.execute(text(UPSERT_QUERY), records)

        logger.info(f"Успешно сохранено/обновлено {len(records)} записей в raw.weather_hourly")
        return len(records)
