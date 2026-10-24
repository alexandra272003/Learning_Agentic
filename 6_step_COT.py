import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def solve_math(question):
    messages = [
        {
            "role": "system",
            "content": """
            You are a grade-school mathematics tutor.

            Solve the problem one step at a time.
            Return only ONE calculation or step per response.
            Do not solve the entire problem in one response.

            When the problem is fully solved, return:
            FINAL ANSWER: <answer>

            Example:
            Question: Sam has 10 apples, buys 5, and gives away 3.
            Step 1: 10 + 5 = 15
            Step 2: 15 - 3 = 12
            FINAL ANSWER: 12
            """
        },
        {"role": "user", "content": question}
    ]

    while True:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )

        answer = response.choices[0].message.content.strip()
        print("\nLLM:", answer)

        messages.append({"role": "assistant", "content": answer})

        if "FINAL ANSWER:" in answer.upper():
            break

        messages.append({
            "role": "user",
            "content": (
                "Give ONLY the next calculation or step using the "
                "previous result. Do not repeat earlier steps. "
                "If the problem is solved, return FINAL ANSWER."
            )
        })


solve_math(
    "A shopkeeper has 120 chocolates. He sells 1/3 of them in the "
    "morning. In the afternoon, he sells 25 more chocolates. "
    "He packs the remaining chocolates equally into 5 boxes. "
    "How many chocolates are in each box?"
)