import logging
from src.extractors.weather_client import WeatherExtractor
from src.loaders.init_db import init_database
from src.loaders.weather_loader import WeatherLoader

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

CITIES = [
    {"name": "Moscow", "lat": 55.751, "lon": 37.618},
    {"name": "Berlin", "lat": 52.520, "lon": 13.405}
]

def run():
    init_database()
    extractor = WeatherExtractor()
    loader = WeatherLoader()

    total_rows = 0
    for city in CITIES:
        logging.info(f"Обработка города: {city['name']}")
        weather_data = extractor.fetch_weather_data(latitude=city["lat"], longitude=city["lon"])
        rows = loader.load(weather_data)
        total_rows += rows

    logging.info(f"Пайплайн завершен. Всего обработано строк: {total_rows}")

if __name__ == "__main__":
    run()
