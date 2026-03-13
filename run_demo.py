#!/usr/bin/env python3
"""
Run the hackathon demo: send the sample plane preflight message to the agent.
Use this to verify the agent and knowledge base are working.
"""
from agent_client import send_message

DEMO_MESSAGE = """I have a plane, 18 kg, 3.2m wingspan, catapult launch, land landing.
I'll upload my full parameter list next — please check them for safety and suggest any changes."""


def main() -> None:
    print("Sending demo message to ArduPilot Preflight agent...\n")
    print("Message:", DEMO_MESSAGE.strip(), "\n")
    try:
        reply = send_message(DEMO_MESSAGE, include_retrieval_info=True, max_tokens=4096)
        print("--- Agent reply ---\n")
        print(reply)
    except Exception as e:
        print("Error:", e)
        raise


if __name__ == "__main__":
    main()
