"""Test: health endpoint returns 200."""
import pytest
from fastapi.testclient import TestClient

import os
os.environ["GEMINI_API_KEY"] = "test-key"
os.environ["DEBUG"] = "true"

from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_readiness():
    r = client.get("/readiness")
    assert r.status_code == 200
