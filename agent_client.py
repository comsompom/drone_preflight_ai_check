"""
ArduPilot Preflight Agent client.
Uses DigitalOcean Gradient AI agent endpoint (OpenAI-compatible API).
"""
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load .env from project root (same folder as this file) so it works regardless of CWD
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path)

AGENT_URL = (os.getenv("AGENT_URL") or "").strip().rstrip("/")
AGENT_API_KEY = (os.getenv("AGENT_API_KEY") or "").strip()


def get_client() -> OpenAI:
    """Build OpenAI client for the agent endpoint."""
    missing = []
    if not AGENT_URL:
        missing.append("AGENT_URL")
    if not AGENT_API_KEY:
        missing.append("AGENT_API_KEY")
    if missing:
        raise ValueError(
            f"Set {', '.join(missing)} in .env (copy from .env.example). "
            f"Ensure .env is in the project root: {Path(__file__).resolve().parent}"
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
