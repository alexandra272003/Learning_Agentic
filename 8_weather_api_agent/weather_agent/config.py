import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = PROJECT_ROOT / "weather_agent" / "prompts"
GEOCODE_URL = os.getenv("GEOCODE_URL", "https://geocoding-api.open-meteo.com/v1/search")
FORECAST_URL = os.getenv("FORECAST_URL", "https://api.open-meteo.com/v1/forecast")
WEATHER_REQUEST_TIMEOUT = int(os.getenv("WEATHER_REQUEST_TIMEOUT", "12"))
MAX_TURNS = int(os.getenv("MAX_TURNS", "5"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
