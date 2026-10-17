"""Run the Groq demo from a source checkout."""

from pathlib import Path
import sys

# Make the src-layout package importable when running: python main.py
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from sanket_agentic import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
