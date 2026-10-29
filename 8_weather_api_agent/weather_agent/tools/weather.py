import requests
from weather_agent.config import GEOCODE_URL, FORECAST_URL, WEATHER_REQUEST_TIMEOUT

WEATHER_CODES = {
    0:"Clear sky", 1:"Mainly clear", 2:"Partly cloudy", 3:"Overcast",
    45:"Fog", 48:"Depositing rime fog", 51:"Light drizzle", 53:"Moderate drizzle",
    55:"Dense drizzle", 56:"Light freezing drizzle", 57:"Dense freezing drizzle",
    61:"Slight rain", 63:"Moderate rain", 65:"Heavy rain", 66:"Light freezing rain",
    67:"Heavy freezing rain", 71:"Slight snow", 73:"Moderate snow", 75:"Heavy snow",
    77:"Snow grains", 80:"Slight rain showers", 81:"Moderate rain showers",
    82:"Violent rain showers", 85:"Slight snow showers", 86:"Heavy snow showers",
    95:"Thunderstorm", 96:"Thunderstorm with slight hail", 99:"Thunderstorm with heavy hail"
}

def lookup_weather(location: str) -> dict:
    """Fetch current conditions using Open-Meteo geocoding and forecast endpoints."""
    location = location.strip()
    if not location:
        return {"error": "Location cannot be empty."}
    try:
        r = requests.get(GEOCODE_URL, params={
            "name": location, "count": 1, "language": "en", "format": "json"
        }, timeout=WEATHER_REQUEST_TIMEOUT)
        r.raise_for_status()
        results = r.json().get("results") or []
        if not results:
            return {"error": f"Could not find location '{location}'."}
        place = results[0]
        r = requests.get(FORECAST_URL, params={
            "latitude": place["latitude"], "longitude": place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m",
            "timezone": "auto"
        }, timeout=WEATHER_REQUEST_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        current = data.get("current")
        if not current:
            return {"error": "Open-Meteo returned no current conditions."}
        code = current.get("weather_code")
        return {
            "location": place.get("name", location), "region": place.get("admin1"),
            "country": place.get("country"), "local_time": current.get("time"),
            "temperature_c": current.get("temperature_2m"),
            "feels_like_c": current.get("apparent_temperature"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "condition": WEATHER_CODES.get(code, f"Weather code {code}"),
            "cloud_cover_percent": current.get("cloud_cover"),
            "precipitation_mm": current.get("precipitation"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "wind_direction_degrees": current.get("wind_direction_10m"),
            "timezone": data.get("timezone"), "source": "Open-Meteo"
        }
    except requests.RequestException as exc:
        return {"error": f"Weather API request failed: {exc}"}
    except (KeyError, TypeError, ValueError) as exc:
        return {"error": f"Could not parse weather response: {exc}"}

TOOL_FUNCTIONS = {"lookup_weather": lookup_weather}
