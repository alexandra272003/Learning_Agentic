"""A small, stateless chatbot client for GroqCloud."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    Groq,
    RateLimitError,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL = "openai/gpt-oss-120b"


def stateless_groq_demo(prompt: str) -> str:
    """Send one prompt to Groq and return the assistant's response.

    Each call contains only the prompt passed to this function, so earlier
    messages are not remembered unless the caller includes them in the prompt.
    """
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string.")

    # Load the project's .env regardless of the terminal's current directory.
    load_dotenv(PROJECT_ROOT / ".env", override=False)

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY was not found. Add it to a .env file in the project root "
            "or set it as an environment variable."
        )

    model = os.getenv("GROQ_MODEL", DEFAULT_MODEL).strip()
    if not model:
        model = DEFAULT_MODEL

    client = Groq(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt.strip()}],
        )
    except AuthenticationError as exc:
        raise RuntimeError(
            "Groq rejected the API key. Check that GROQ_API_KEY is valid and active."
        ) from exc
    except RateLimitError as exc:
        raise RuntimeError(
            "Groq rate limit or quota reached. Check your Groq account limits and retry."
        ) from exc
    except APIConnectionError as exc:
        raise RuntimeError(
            "Could not connect to Groq. Check your internet connection and try again."
        ) from exc
    except APIStatusError as exc:
        raise RuntimeError(
            f"Groq returned HTTP {exc.status_code}. Check the model ID and API error details: {exc}"
        ) from exc

    answer = completion.choices[0].message.content
    return answer or "(The model returned an empty response.)"


def main() -> int:
    parser = argparse.ArgumentParser(description="Ask a question using the Groq API.")
    parser.add_argument(
        "prompt",
        nargs="?",
        default="Who was the UK prime minister before 2020?",
        help="The prompt to send to the model.",
    )
    args = parser.parse_args()

    print(f"Prompt: {args.prompt}\n")
    try:
        answer = stateless_groq_demo(args.prompt)
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("--- Groq Response ---")
    print(answer)
    return 0


__all__ = ["main", "stateless_groq_demo"]
