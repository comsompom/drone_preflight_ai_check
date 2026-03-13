"""
Unit tests for agent_client: get_client, send_message.
"""
from unittest.mock import MagicMock, patch

import pytest

import agent_client


def test_get_client_raises_when_agent_url_missing(monkeypatch):
    monkeypatch.setattr(agent_client, "AGENT_URL", "")
    monkeypatch.setattr(agent_client, "AGENT_API_KEY", "key")
    with pytest.raises(ValueError) as exc_info:
        agent_client.get_client()
    assert "AGENT_URL" in str(exc_info.value)


def test_get_client_raises_when_api_key_missing(monkeypatch):
    monkeypatch.setattr(agent_client, "AGENT_URL", "https://x.agents.do-ai.run")
    monkeypatch.setattr(agent_client, "AGENT_API_KEY", "")
    with pytest.raises(ValueError) as exc_info:
        agent_client.get_client()
    assert "AGENT_API_KEY" in str(exc_info.value)


def test_get_client_raises_both_when_both_missing(monkeypatch):
    monkeypatch.setattr(agent_client, "AGENT_URL", "")
    monkeypatch.setattr(agent_client, "AGENT_API_KEY", "")
    with pytest.raises(ValueError) as exc_info:
        agent_client.get_client()
    assert "AGENT_URL" in str(exc_info.value)
    assert "AGENT_API_KEY" in str(exc_info.value)


def test_get_client_returns_openai_client(valid_agent_env):
    client = agent_client.get_client()
    assert client is not None
    assert client.base_url == "https://test.agents.do-ai.run/api/v1/"
    assert client.api_key == "test-key-123"


def test_send_message_calls_api_and_returns_reply(valid_agent_env):
    fake_content = "Agent says OK."
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content=fake_content))
    ]

    with patch.object(agent_client, "get_client") as mock_get:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_get.return_value = mock_client

        result = agent_client.send_message("Hello")

    assert result == fake_content
    mock_client.chat.completions.create.assert_called_once()
    call_kw = mock_client.chat.completions.create.call_args[1]
    assert call_kw["model"] == "agent"
    assert call_kw["messages"] == [{"role": "user", "content": "Hello"}]
    assert call_kw["max_tokens"] == 4096
    assert call_kw["extra_body"]["include_retrieval_info"] is True


def test_send_message_respects_max_tokens_and_retrieval(valid_agent_env):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="R"))]

    with patch.object(agent_client, "get_client") as mock_get:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_get.return_value = mock_client

        agent_client.send_message(
            "Hi",
            include_retrieval_info=False,
            max_tokens=1024,
        )

    call_kw = mock_client.chat.completions.create.call_args[1]
    assert call_kw["max_tokens"] == 1024
    assert call_kw["extra_body"]["include_retrieval_info"] is False


def test_send_message_returns_no_response_when_empty_content(valid_agent_env):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=None))]

    with patch.object(agent_client, "get_client") as mock_get:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_get.return_value = mock_client

        result = agent_client.send_message("Hi")

    assert result == "(No response)"
