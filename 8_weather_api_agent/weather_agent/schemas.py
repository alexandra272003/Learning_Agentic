lookup_weather_schema = {
    "type": "function",
    "function": {
        "name": "lookup_weather",
        "description": "Look up current weather for a place using Open-Meteo. Use for temperature, wind, humidity, or current conditions.",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string", "description": "City or place name, e.g. Varanasi, London."}},
            "required": ["location"],
            "additionalProperties": False,
        },
    },
}
TOOL_MENU = [lookup_weather_schema]

def tool_catalog() -> list[dict[str, str]]:
    return [{"name": x["function"]["name"], "description": x["function"]["description"]} for x in TOOL_MENU]
