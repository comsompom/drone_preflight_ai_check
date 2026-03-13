"""
Unit tests for Flask web app: routes and /api/chat logic.
"""
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add project root for webapp import
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def client():
    """Flask test client with get_agent_reply mocked to avoid real API calls."""
    with patch("webapp.app.get_agent_reply") as mock_reply:
        mock_reply.return_value = "Mocked agent reply."
        from webapp.app import app
        app.config["TESTING"] = True
        with app.test_client() as c:
            yield c


def test_index_returns_200(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"ArduPilot" in r.data or b"Preflight" in r.data


def test_api_chat_requires_message(client):
    r = client.post(
        "/api/chat",
        json={},
        content_type="application/json",
    )
    assert r.status_code == 400
    data = r.get_json()
    assert "error" in data
    assert "message" in data["error"].lower() or "required" in data["error"].lower()


def test_api_chat_rejects_empty_message(client):
    r = client.post(
        "/api/chat",
        json={"message": "   "},
        content_type="application/json",
    )
    assert r.status_code == 400


def test_api_chat_returns_agent_reply(client):
    r = client.post(
        "/api/chat",
        json={"message": "Plane, 18 kg, here are my params."},
        content_type="application/json",
    )
    assert r.status_code == 200
    data = r.get_json()
    assert data["reply"] == "Mocked agent reply."


def test_api_chat_returns_400_on_value_error(client):
    with patch("webapp.app.get_agent_reply") as mock_reply:
        mock_reply.side_effect = ValueError("Set AGENT_URL in .env")
        from webapp.app import app
        app.config["TESTING"] = True
        with app.test_client() as c:
            r = c.post(
                "/api/chat",
                json={"message": "hello"},
                content_type="application/json",
            )
    assert r.status_code == 400
    assert "error" in r.get_json()


def test_api_chat_returns_500_on_generic_exception(client):
    with patch("webapp.app.get_agent_reply") as mock_reply:
        mock_reply.side_effect = RuntimeError("Network error")
        from webapp.app import app
        app.config["TESTING"] = True
        with app.test_client() as c:
            r = c.post(
                "/api/chat",
                json={"message": "hello"},
                content_type="application/json",
            )
    assert r.status_code == 500
    assert "error" in r.get_json()
