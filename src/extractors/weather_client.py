import logging
from typing import Any, Dict
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from src.extractors.schemas import WeatherApiResponse

# Базовая настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


class WeatherExtractor:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry_error_callback=lambda retry_state: logger.error(
            f"Все 3 попытки исчерпаны. Ошибка: {retry_state.outcome.exception()}"
        ),
        reraise=True
    )
    def fetch_weather_data(self, latitude: float, longitude: float) -> WeatherApiResponse:
        """
        Выгружает почасовые метеоданные по заданным координатам.
        Автоматически повторяет запрос до 3 раз при сбоях сети.
        """
        params: Dict[str, Any] = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m",
                "direct_normal_irradiance"
            ],
            "timezone": "UTC"
        }

        logger.info(f"Запрос метеоданных для координат: lat={latitude}, lon={longitude}")
        response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
        response.raise_for_status()

        # Валидация через Pydantic v2
        validated_data = WeatherApiResponse.model_validate(response.json())
        logger.info(f"Данные успешно получены и валидированы. Записей: {len(validated_data.hourly.time)}")
        return validated_data
