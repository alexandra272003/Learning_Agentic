# Gemini Agentic AI Starter

A minimal Python agent using Google's Gemini API with two tools:
- `calculate`: arithmetic operations
- `get_current_date`: current local date/time from your computer

## Setup (VS Code / Windows)

1. Install Python 3.10+.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env`, then add your API key from
   https://aistudio.google.com/apikey

6. Run:

   ```bash
   python main.py
   ```

Type `exit` to quit.

## Notes

- Keep `.env` private and never commit your API key.
- The model is set to `gemini-2.5-flash`. If your account cannot access it,
  select a model currently available to your API key.
- Tool calls are handled automatically by the Google Gen AI SDK.
