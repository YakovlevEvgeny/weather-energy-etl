from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator


class WeatherHourlyRaw(BaseModel):
    """Схема валидации почасовых замеров погоды от Open-Meteo API."""
    time: List[datetime]
    temperature_2m: List[float] = Field(..., description="Температура воздуха на высоте 2м (°C)")
    relative_humidity_2m: List[int] = Field(..., description="Относительная влажность (%)")
    wind_speed_10m: List[float] = Field(..., description="Скорость ветра на высоте 10м (м/с)")
    direct_normal_irradiance: List[float] = Field(..., description="Прямая солнечная радиация (W/m²)")

    @field_validator("relative_humidity_2m")
    @classmethod
    def validate_humidity(cls, values: List[int]) -> List[int]:
        for val in values:
            if not (0 <= val <= 100):
                raise ValueError(f"Влажность выходит за пределы [0, 100]: {val}")
        return values


class WeatherApiResponse(BaseModel):
    """Корневой объект ответа Open-Meteo."""
    latitude: float
    longitude: float
    timezone: str
    hourly: WeatherHourlyRaw
