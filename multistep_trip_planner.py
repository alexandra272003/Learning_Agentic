"""
Multi-step prompting: 8-step travel planner using Groq.

Install:
    pip install openai python-dotenv

Create .env beside this script:
    GROQ_API_KEY=your_actual_groq_api_key
    GROQ_MODEL=openai/gpt-oss-20b

Run:
    python multistep_trip_planner.py

The script:
- Uses Groq's OpenAI-compatible Chat Completions API.
- Sets request timeouts and retries temporary failures.
- Keeps previous-step context concise to avoid oversized requests.
- Saves each successful step to multistep_trip_plan_output.md.
"""

import os
import time
from pathlib import Path
import time
from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
)
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to a .env file beside this script."
    )

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
OUTPUT_FILE = Path(__file__).with_name("multistep_trip_plan_output.md")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1",
    timeout=90.0,  # Maximum wait per request
    max_retries=0,  # Retries are handled below
)

SYSTEM_PROMPT = """
You are a practical, budget-conscious travel-planning assistant.
Be specific, organized, and consistent with the budget.
Do not claim to have checked live prices or availability.
Label prices as estimates and state important assumptions.
Prefer concise answers with useful tables or bullet points.
"""

USER_REQUEST = """
Plan a 3-day trip to new york with a total budget of $500 for one traveler.
The budget excludes international flights.

Include accommodation, local transport, daily activities and sightseeing,
food and drink, a day-by-day itinerary, a budget breakdown, and practical
tips. Keep the full on-the-ground budget at or below $500. State assumptions.
"""

STEPS = [
    ("Step 1: Assumptions", "List the key assumptions for a 3-day New York trip for one person with a $500 budget, excluding flights."),
    ("Step 2: Budget", "Allocate the $500 across accommodation, transport, food, activities, and emergency money; show totals."),
    ("Step 3: Accommodation", "Recommend a budget-friendly area and accommodation type for 2 nights with estimated cost."),
    ("Step 4: Transport", "Suggest affordable airport transfers and local transport with estimated costs."),
    ("Step 5: Activities", "Suggest affordable New York sightseeing activities for each of the 3 days with costs."),
    ("Step 6: Food", "Plan affordable breakfast, lunch, and dinner for 3 days with estimated costs."),
    ("Step 7: Itinerary", "Combine accommodation, transport, activities, and food into a simple morning-afternoon-evening itinerary."),
    ("Step 8: Final check", "Add all expenses, keep the total within $500, correct overspending, and list important booking checks."),
]


def call_groq(step_title: str, task: str, context: str) -> str:
    user_message = f"""
Original request:
{USER_REQUEST}

Previous steps:
{context if context else "None"}

Current step: {step_title}
Task: {task}

Answer in at most 5 short bullet points.
Be concise. Do not repeat the original request.
"""

    transient_errors = (
        APIConnectionError,
        APITimeoutError,
        RateLimitError,
        InternalServerError,
    )

    for attempt in range(1, 4):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=800,
                temperature=0.2,
            )

            choice = response.choices[0]
            result = choice.message.content

            if result and result.strip():
                return result.strip()

            # Empty response: retry instead of stopping immediately.
            print(
                f"Attempt {attempt}/3 returned empty content. "
                f"Finish reason: {choice.finish_reason}"
            )

        except transient_errors as exc:
            print(f"Attempt {attempt}/3 failed: {exc}")

        if attempt < 3:
            wait_seconds = attempt * 3
            print(f"Retrying in {wait_seconds} seconds...")
            time.sleep(wait_seconds)

    raise RuntimeError(
        f"{step_title} failed after 3 attempts. "
        "Check the model, API quota, and finish reason."
    )



def main() -> None:
    # Store output as we go so successful steps remain available if a later
    # request fails or the user stops the program.
    completed = []
    OUTPUT_FILE.write_text(
        "# 3-Day New York Trip — Multi-Step Prompting Results\n\n"
        f"**Model:** `{MODEL}`\n\n"
        f"**User request:** {USER_REQUEST.strip()}\n\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("MULTI-STEP TRAVEL PLANNER — GROQ")
    print(f"Model: {MODEL}")
    print(f"Output file: {OUTPUT_FILE}")
    print("=" * 72)
    print("\nUSER REQUEST\n" + USER_REQUEST.strip())

    for index, (step_title, task) in enumerate(STEPS, start=1):
        print(f"\n\n{'=' * 72}\n{step_title}\n{'=' * 72}")

        # Include only a compact summary of previous steps, rather than all
        # their full text. This keeps later requests smaller and faster.
        if completed:
            context = "\n\n".join(
                f"{title}\n{answer[:1000]}"
                for title, answer in completed[-3:]
            )
        else:
            context = ""

        try:
            answer = call_groq(step_title, task, context)
        except KeyboardInterrupt:
            print("\nStopped by user. Previously completed steps are saved.")
            print(f"Partial results: {OUTPUT_FILE}")
            return
        except Exception as exc:
            print(f"\nCould not complete {step_title}: {type(exc).__name__}: {exc}")
            print("The results from completed steps have been saved.")
            print(f"Partial results: {OUTPUT_FILE}")
            print(
                "\nCheck your connection, Groq model availability, rate limits, "
                "and API account status. You can rerun the script to start again."
            )
            return

        print(answer)
        completed.append((step_title, answer))

        with OUTPUT_FILE.open("a", encoding="utf-8") as file:
            file.write(f"\n\n## {step_title}\n\n{answer}\n")

        print(f"\n[Saved completed step {index}/8 to {OUTPUT_FILE.name}]")

    with OUTPUT_FILE.open("a", encoding="utf-8") as file:
        file.write(
            "\n\n---\n\n"
            "*Prices and availability are estimates. Verify details before booking.*\n"
        )

    print("\n\nAll 8 steps completed.")
    print(f"Full plan saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
