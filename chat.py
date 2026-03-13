#!/usr/bin/env python3
"""
Send a single message to the ArduPilot Preflight agent and print the reply.
Usage:
  python chat.py "Your message here"
  python chat.py   (then type message when prompted, or paste multi-line and Ctrl+Z then Enter on Windows)
"""
import sys
from agent_client import send_message


def main() -> None:
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        print("Enter your message (end with Ctrl+Z then Enter on Windows, Ctrl+D on Unix):")
        text = sys.stdin.read().strip()
    if not text:
        print("No message provided.")
        sys.exit(1)
    try:
        reply = send_message(text)
        print("\n--- Agent reply ---\n")
        print(reply)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
