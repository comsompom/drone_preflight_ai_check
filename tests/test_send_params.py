"""
Unit tests for send_params: message building and file handling.
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Project root on path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_send_params_builds_message_with_intro(tmp_path):
    param_file = tmp_path / "test.param"
    param_file.write_text("SYSID_THISMAV,1\nBATT_CAPACITY,5000\n")

    with patch("send_params.send_message") as mock_send:
        mock_send.return_value = "OK"
        with patch.object(sys, "argv", ["send_params.py", str(param_file), "--intro", "Plane, 18 kg"]):
            from send_params import main
            main()

    mock_send.assert_called_once()
    message = mock_send.call_args[0][0]
    assert "Plane, 18 kg" in message
    assert "SYSID_THISMAV" in message
    assert "BATT_CAPACITY" in message
    assert "test.param" in message


def test_send_params_builds_message_without_intro(tmp_path):
    param_file = tmp_path / "mission.waypoints"
    param_file.write_text("QGC WPL 110\n0\t0\t0\t16\t0\t0\t0\t0\t0\t0\t0\t1\n")

    with patch("send_params.send_message") as mock_send:
        mock_send.return_value = "OK"
        with patch.object(sys, "argv", ["send_params.py", str(param_file)]):
            from send_params import main
            main()

    mock_send.assert_called_once()
    message = mock_send.call_args[0][0]
    assert "mission.waypoints" in message
    assert "QGC WPL" in message
    assert "parameters / mission" in message


def test_send_params_exits_when_file_not_found():
    with patch.object(sys, "argv", ["send_params.py", "/nonexistent/file.param"]):
        with pytest.raises(SystemExit) as exc_info:
            from send_params import main
            main()
    assert exc_info.value.code == 1


def test_send_params_passes_no_retrieval_and_max_tokens(tmp_path):
    param_file = tmp_path / "p.param"
    param_file.write_text("A,1\n")

    with patch("send_params.send_message") as mock_send:
        mock_send.return_value = "OK"
        with patch.object(sys, "argv", ["send_params.py", str(param_file), "--no-retrieval"]):
            from send_params import main
            main()

    mock_send.assert_called_once()
    assert mock_send.call_args[1]["include_retrieval_info"] is False
    assert mock_send.call_args[1]["max_tokens"] == 8192
