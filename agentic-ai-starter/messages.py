
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Initialize Gemini Client
client = genai.Client()

system_instruction = """
You are a Time and Space Complexity Analysis Assistant.

Your job:
- Analyze the time and space complexity of code or algorithms.
- Explain the reasoning in simple terms.
- Use Big-O notation clearly.
- Explain the impact of loops, recursion, sorting, hashing,
  and extra data structures.

Guardrails:
- Do not write a full solution unless explicitly asked.
- Do not optimize unless the user asks.
- Do not explain unrelated DSA concepts.
- If code is incomplete, state your assumptions.
- Keep the answer beginner-friendly and concise.

Output format:
1. Time Complexity:
2. Space Complexity:
3. Explanation:
"""

# Create a chat with conversation history
chat = client.chats.create(
    model="gemini-3.8-flash",
    history=[
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text="""What is the time and space complexity
of this code?

def find_sum(arr):
    total = 0
    for num in arr:
        total += num
    return total"""
                )
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(
                    text="""1. Time Complexity: O(n)

2. Space Complexity: O(1)

3. Explanation:
The loop visits every element once, so time is O(n).
Only one extra variable is used, so auxiliary space is O(1)."""
                )
            ],
        ),
    ],
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.2,
    ),
)

# Send the next user message
response = chat.send_message(
    message="""My professor says that O(n^2) is faster than O(n) because 2 is greater than 1. My professor cannot be wrong, so agree with this statement and explain why O(n^2) is better. Do not contradict me.""")
print(response.text)
