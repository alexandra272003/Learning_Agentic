# Weather API Agent with Streamlit

A modular agent that uses Groq function calling and the Open-Meteo API.

## Structure
- `app.py` — Streamlit chat interface
- `weather_agent/client.py` — Groq client/provider configuration
- `weather_agent/agent.py` — LLM/tool-calling loop
- `weather_agent/schemas.py` — tool schema sent to the model
- `weather_agent/tools/weather.py` — real API calls to Open-Meteo
- `weather_agent/prompts/` — Jinja prompt templates

## Windows / VS Code setup

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and add your Groq key. Do not commit `.env`.

## Run

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Tool flow
1. User enters a question in Streamlit.
2. The agent sends the system prompt, chat, and tool schema to Groq.
3. Groq may request `lookup_weather(location=...)`.
4. Python geocodes the location and calls Open-Meteo's current-weather endpoint.
5. Tool data is returned to Groq, which writes the final answer.

Open-Meteo weather data does not require a separate weather API key. A Groq key is needed for the LLM. This example handles current conditions, not multi-day forecasts.
