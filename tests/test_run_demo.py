"""
Unit tests for run_demo: DEMO_MESSAGE and main() calls send_message.
"""
from unittest.mock import patch

import pytest

from run_demo import DEMO_MESSAGE, main


def test_demo_message_contains_plane_specs():
    assert "plane" in DEMO_MESSAGE.lower()
    assert "18" in DEMO_MESSAGE
    assert "3.2" in DEMO_MESSAGE
    assert "catapult" in DEMO_MESSAGE.lower()
    assert "parameter" in DEMO_MESSAGE.lower()


def test_main_calls_send_message_with_demo_message():
    with patch("run_demo.send_message") as mock_send:
        mock_send.return_value = "Agent reply here"
        main()
    mock_send.assert_called_once()
    call_args = mock_send.call_args[0]
    assert call_args[0] == DEMO_MESSAGE
    assert mock_send.call_args[1]["include_retrieval_info"] is True
    assert mock_send.call_args[1]["max_tokens"] == 4096
