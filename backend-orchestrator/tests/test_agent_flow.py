"""Test: agent/issue endpoint with mocked Gemini."""
import pytest
import os
os.environ["GEMINI_API_KEY"] = "test-key"
os.environ["DEBUG"] = "true"

from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_issue_endpoint_returns_session():
    with patch("app.agents.vision_agent.VisionAgent.analyze", new_callable=AsyncMock) as mv, \
         patch("app.agents.incident_analyst.IncidentAnalystAgent.analyze", new_callable=AsyncMock) as ma, \
         patch("app.agents.runbook_agent.RunbookAgent.query", new_callable=AsyncMock) as mr, \
         patch("app.agents.action_agent.ActionAgent.prepare", new_callable=AsyncMock) as mp:
        mv.return_value = ""
        ma.return_value = ([], __import__("app.domain.models", fromlist=["IncidentCategory"]).IncidentCategory.UNKNOWN, "No root cause")
        mr.return_value = "Check the logs"
        mp.return_value = []
        r = client.post("/agent/issue", json={"description": "Service is down, 500 errors in API"})
        assert r.status_code == 200
        data = r.json()
        assert "session_id" in data
        assert "recommendations" in data
