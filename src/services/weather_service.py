import requests, json
from src.config import Config
from src.utils.string_utils import format_date

GEOCODING_API = 'https://geocoding-api.open-meteo.com/v1/search'
WEATHER_API = 'https://api.open-meteo.com/v1/forecast'
FORECAST_DAYS = 7


def load_descriptions():
    with open(Config.DESCRIPTIONS_FILE, 'r', encoding='utf8') as file:
        return json.load(file)

WEATHER_DESCRIPTIONS = load_descriptions()


def get_coordinates(city):
    try:
        response = requests.get(GEOCODING_API, params={'name': city}, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = data.get('results')
        if not results:
            return None, None

        return results[0]['latitude'], results[0]['longitude']
    except requests.RequestException:
        return None, None


def fetch_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code"],
        "forecast_days": FORECAST_DAYS,
        "timezone": "auto"
    }

    try:
        response = requests.get(WEATHER_API, params=params, timeout=10)
        response.raise_for_status()
        daily = response.json().get('daily', {})

        dates = daily.get('time', [])
        t_mins = daily.get('temperature_2m_min', [])
        t_maxs = daily.get('temperature_2m_max', [])
        codes = daily.get('weather_code', [])

        weather = []
        for date, t_min, t_max, code in zip(dates, t_mins, t_maxs, codes):
            description_data = WEATHER_DESCRIPTIONS.get(str(code), {})
            condition = description_data.get('day', {}).get('description', f"Unknown ({code})")

            weather.append({
                'date': format_date(date),
                'min': t_min,
                'max': t_max,
                'condition': condition
            })

        return weather
    except requests.RequestException:
        return []