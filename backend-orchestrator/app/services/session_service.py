"""
Session Service — manages short-term session state with Redis (or in-memory fallback).
"""
import json
import logging
import uuid
from dataclasses import asdict
from datetime import datetime
from typing import Optional

from app.config import get_settings
from app.domain.models import SessionState

logger = logging.getLogger("supportsight.session")
settings = get_settings()

# In-memory fallback store (for local dev / demo)
_STORE: dict[str, dict] = {}


class SessionService:
    async def get_or_create(self, session_id: str, correlation_id: str) -> SessionState:
        raw = _STORE.get(session_id)
        if raw:
            return self._deserialize(raw)
        return SessionState(session_id=session_id, correlation_id=correlation_id)

    async def save(self, state: SessionState):
        _STORE[state.session_id] = self._serialize(state)

    async def get(self, session_id: str) -> Optional[SessionState]:
        raw = _STORE.get(session_id)
        return self._deserialize(raw) if raw else None

    def _serialize(self, state: SessionState) -> dict:
        data = asdict(state)
        data["created_at"] = state.created_at.isoformat()
        return data

    def _deserialize(self, data: dict) -> SessionState:
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        from app.domain.models import IncidentCategory, IncidentSeverity, Hypothesis, SuggestedAction, ActionStatus
        data["incident_category"] = IncidentCategory(data["incident_category"])
        data["severity"] = IncidentSeverity(data["severity"])
        data["active_hypotheses"] = [
            Hypothesis(**{**h, "category": IncidentCategory(h["category"])})
            for h in data.get("active_hypotheses", [])
        ]
        data["pending_actions"] = [
            SuggestedAction(**{**a, "status": ActionStatus(a["status"])})
            for a in data.get("pending_actions", [])
        ]
        return SessionState(**data)
