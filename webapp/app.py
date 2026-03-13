"""
ArduPilot Preflight Inspector — Flask web UI.
Military-style interface for interacting with the AI agent.
Run from project root: python webapp/app.py
"""
import os
import sys
from pathlib import Path

# Project root (parent of webapp/) — for .env and agent_client import
ROOT = Path(__file__).resolve().parent.parent
WEBAPP_DIR = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from flask import Flask, render_template, request, jsonify


def get_agent_reply(content: str) -> str:
    from agent_client import send_message
    return send_message(content, include_retrieval_info=False, max_tokens=8192)


# Explicit paths so templates/static are found when run from project root or from webapp/
app = Flask(
    __name__,
    template_folder=str(WEBAPP_DIR / "templates"),
    static_folder=str(WEBAPP_DIR / "static"),
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Message is required"}), 400
    try:
        reply = get_agent_reply(message)
        return jsonify({"reply": reply})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "0") == "1")
