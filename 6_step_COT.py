import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

model = os.getenv("LLM_MODEL", "openai/gpt-oss-120b")

print("Using model:", model)


def solve_math(question):
    messages = [
        {
            "role": "system",
            "content": """
You are a grade-school mathematics tutor.

Solve the problem one step at a time.
Return only ONE calculation or step per response.
Do not solve the entire problem in one response.

After each step, wait for the user message asking for the next step.

When the problem is fully solved, return:
FINAL ANSWER: <answer>
"""
        },
        {"role": "user", "content": question}
    ]

    max_steps = 10

    for step_number in range(max_steps):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            max_completion_tokens=500,
            extra_body={"include_reasoning": False}
        )

        answer = response.choices[0].message.content
        print(answer)

        if not answer:
            print("The model returned an empty response.")
            return

        print(f"\nLLM: {answer}")

        messages.append({
            "role": "assistant",
            "content": answer
        })

        if "FINAL ANSWER:" in answer.upper():
            return

        messages.append({
            "role": "user",
            "content": (
                "Give only the next calculation or step using "
                "the previous result. Do not repeat earlier steps. "
                "If the problem is solved, return FINAL ANSWER."
            )
        })

    print("\nStopped: maximum number of steps reached.")


if __name__ == "__main__":
    solve_math(
        "A shopkeeper has 120 chocolates. He sells 1/3 of them in the "
        "morning. In the afternoon, he sells 25 more chocolates. "
        "He packs the remaining chocolates equally into 5 boxes. "
        "How many chocolates are in each box?"
    )