from dataclasses import dataclass
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass(frozen=True)
class Provider:
    name: str
    env_var: str
    base_url: str
    model: str

def select_provider() -> Provider:
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is missing. Add it to .env; see .env.example.")
    return Provider("Groq", "GROQ_API_KEY", "https://api.groq.com/openai/v1",
                    os.getenv("LLM_MODEL", "openai/gpt-oss-120b"))

def get_client_and_model() -> tuple[OpenAI, str, Provider]:
    provider = select_provider()
    client = OpenAI(api_key=os.getenv(provider.env_var), base_url=provider.base_url)
    return client, provider.model, provider
