"""
Pytest fixtures and configuration for drone_preflight_ai_check tests.
"""
import sys
from pathlib import Path

import pytest

# Ensure project root is on path for imports
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def valid_agent_env(monkeypatch):
    """Patch agent_client so get_client() succeeds (no real API key needed)."""
    import agent_client as ac
    monkeypatch.setattr(ac, "AGENT_URL", "https://test.agents.do-ai.run")
    monkeypatch.setattr(ac, "AGENT_API_KEY", "test-key-123")
    return ac
