"""
ArduPilot Preflight Agent client.
Uses DigitalOcean Gradient AI agent endpoint (OpenAI-compatible API).
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

AGENT_URL = os.getenv("AGENT_URL", "").rstrip("/")
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "")


def get_client() -> OpenAI:
    """Build OpenAI client for the agent endpoint."""
    if not AGENT_URL or not AGENT_API_KEY:
        raise ValueError(
            "Set AGENT_URL and AGENT_API_KEY in .env (copy from .env.example)."
        )
    base_url = f"{AGENT_URL}/api/v1/"
    return OpenAI(base_url=base_url, api_key=AGENT_API_KEY)


def send_message(
    content: str,
    *,
    include_retrieval_info: bool = True,
    max_tokens: int = 4096,
) -> str:
    """
    Send a single user message to the agent and return the assistant reply.
    """
    client = get_client()
    response = client.chat.completions.create(
        model="agent",
        messages=[{"role": "user", "content": content}],
        max_tokens=max_tokens,
        extra_body={
            "include_retrieval_info": include_retrieval_info,
        },
    )
    reply = ""
    for choice in response.choices:
        if choice.message.content:
            reply += choice.message.content
    return reply.strip() or "(No response)"


if __name__ == "__main__":
    # Quick test
    try:
        r = send_message("Say OK if you can read this.")
        print(r)
    except Exception as e:
        print("Error:", e)
