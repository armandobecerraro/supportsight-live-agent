"""Test log parser Python fallback."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src/bridge"))
from server import _python_parse

def test_detects_errors():
    logs = "2026-01-01 10:00:00 INFO Starting\n2026-01-01 10:00:01 ERROR Connection refused\n"
    result = _python_parse(logs)
    assert len(result["errors"]) == 1
    assert "Connection refused" in result["probable_cause"]

def test_no_errors():
    logs = "2026-01-01 INFO All good\n"
    result = _python_parse(logs)
    assert result["errors"] == []
    assert "No errors" in result["probable_cause"]
