from datetime import datetime
import pytest
from pydantic import ValidationError
from src.extractors.schemas import WeatherApiResponse, WeatherHourlyRaw


def test_valid_weather_payload():
    data = {
        "latitude": 55.75,
        "longitude": 37.62,
        "timezone": "UTC",
        "hourly": {
            "time": [datetime(2026, 9, 2, 12, 0)],
            "temperature_2m": [21.5],
            "relative_humidity_2m": [65],
            "wind_speed_10m": [4.2],
            "direct_normal_irradiance": [350.0]
        }
    }
    model = WeatherApiResponse.model_validate(data)
    assert model.latitude == 55.75
    assert model.hourly.temperature_2m[0] == 21.5


def test_invalid_humidity_raises_error():
    data = {
        "latitude": 55.75,
        "longitude": 37.62,
        "timezone": "UTC",
        "hourly": {
            "time": [datetime(2026, 9, 2, 12, 0)],
            "temperature_2m": [21.5],
            "relative_humidity_2m": [120],  # Недопустимое значение > 100%
            "wind_speed_10m": [4.2],
            "direct_normal_irradiance": [350.0]
        }
    }
    with pytest.raises(ValidationError):
        WeatherApiResponse.model_validate(data)
