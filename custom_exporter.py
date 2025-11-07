from prometheus_client import start_http_server, Gauge
import random, time

# === Custom metrics (с меткой city) ===
temperature = Gauge('weather_temperature_celsius', 'Current temperature in Celsius', ['city'])
humidity = Gauge('weather_humidity_percent', 'Current humidity percentage', ['city'])
wind_speed = Gauge('weather_wind_speed_mps', 'Wind speed in meters per second', ['city'])
pressure = Gauge('weather_pressure_hpa', 'Atmospheric pressure in hPa', ['city'])
rainfall = Gauge('weather_rainfall_mm', 'Rainfall in millimeters', ['city'])
uv_index = Gauge('weather_uv_index', 'UV index level', ['city'])
air_quality = Gauge('weather_air_quality_index', 'Air quality index (AQI)', ['city'])
visibility = Gauge('weather_visibility_km', 'Visibility in kilometers', ['city'])
feels_like = Gauge('weather_feels_like_celsius', 'Feels-like temperature in Celsius', ['city'])
condition_score = Gauge('weather_condition_score', 'Overall weather comfort score', ['city'])

# === Cписок городов ===
cities = ["Astana", "Almaty", "Aktau"]

# === Start HTTP server ===
if __name__ == "__main__":
    start_http_server(8000)
    print("✅ Custom Weather Exporter running on http://localhost:8000/metrics")

    while True:
        for city in cities:
            temperature.labels(city=city).set(round(random.uniform(-10, 35), 2))
            humidity.labels(city=city).set(round(random.uniform(20, 100), 2))
            wind_speed.labels(city=city).set(round(random.uniform(0, 15), 2))
            pressure.labels(city=city).set(round(random.uniform(990, 1040), 2))
            rainfall.labels(city=city).set(round(random.uniform(0, 10), 2))
            uv_index.labels(city=city).set(round(random.uniform(0, 12), 2))
            air_quality.labels(city=city).set(round(random.uniform(10, 150), 2))
            visibility.labels(city=city).set(round(random.uniform(1, 10), 2))
            feels_like.labels(city=city).set(round(random.uniform(-10, 35), 2))
            condition_score.labels(city=city).set(round(random.uniform(0, 100), 2))

        time.sleep(20)
