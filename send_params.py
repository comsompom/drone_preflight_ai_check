#!/usr/bin/env python3
"""
Send an ArduPilot parameter file (.param) or mission/waypoints to the agent
with an optional intro message (e.g. drone type, takeoff method).
Usage:
  python send_params.py params.param
  python send_params.py params.param --intro "Plane, 18 kg, 3.2m wingspan, catapult, land takeoff"
  python send_params.py waypoints.txt --intro "Mission file for quad, manual then auto"
"""
import argparse
from pathlib import Path
from agent_client import send_message


def main() -> None:
    ap = argparse.ArgumentParser(description="Send param or mission file to ArduPilot Preflight agent.")
    ap.add_argument("file", type=Path, help="Path to .param or waypoints/mission file")
    ap.add_argument(
        "--intro",
        default="",
        help="Intro message: drone type, weight, takeoff method, etc.",
    )
    ap.add_argument("--no-retrieval", action="store_true", help="Disable retrieval info in response")
    args = ap.parse_args()

    path = args.file
    if not path.exists():
        print(f"File not found: {path}")
        exit(1)

    content = path.read_text(encoding="utf-8", errors="replace")
    intro = (args.intro.strip() + "\n\n") if args.intro.strip() else ""
    message = f"{intro}Here are my parameters / mission (from {path.name}):\n\n```\n{content}\n```"

    try:
        reply = send_message(
            message,
            include_retrieval_info=not args.no_retrieval,
            max_tokens=8192,
        )
        print("\n--- Agent reply ---\n")
        print(reply)
    except Exception as e:
        print("Error:", e)
        exit(1)


if __name__ == "__main__":
    main()
