
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=500,
    ),
)

response = chat.send_message(
    "whasts 2 + 2 * 2 from left to right is 8."
)

print(response.text)