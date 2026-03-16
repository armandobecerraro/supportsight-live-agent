"""
Session Service — manages short-term session state with Redis.
"""
import json
import logging
import uuid
import redis.asyncio as redis
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Optional

from app.config import get_settings
from app.domain.models import SessionState, IncidentCategory, IncidentSeverity, Hypothesis, SuggestedAction, ActionStatus

logger = logging.getLogger("supportsight.session")
settings = get_settings()

class SessionService:
    def __init__(self, redis_url: str = settings.REDIS_URL):
        self._redis = redis.from_url(redis_url, decode_responses=True)
        self._ttl = settings.SESSION_TTL_SECONDS

    async def get_or_create(self, session_id: str, correlation_id: str) -> SessionState:
        state = await self.get(session_id)
        if state:
            return state
        return SessionState(session_id=session_id, correlation_id=correlation_id)

    async def save(self, state: SessionState):
        try:
            data = self._serialize(state)
            await self._redis.setex(
                f"session:{state.session_id}",
                self._ttl,
                json.dumps(data)
            )
        except Exception as e:
            logger.error(f"Error saving session to Redis: {e}")

    async def get(self, session_id: str) -> Optional[SessionState]:
        try:
            raw = await self._redis.get(f"session:{session_id}")
            if not raw:
                return None
            return self._deserialize(json.loads(raw))
        except Exception as e:
            logger.error(f"Error retrieving session from Redis: {e}")
            return None

    def _serialize(self, state: SessionState) -> dict:
        data = asdict(state)
        data["created_at"] = state.created_at.isoformat()
        # Convert enums to values for JSON serialization
        data["incident_category"] = state.incident_category.value
        data["severity"] = state.severity.value
        data["active_hypotheses"] = [
            {**asdict(h), "category": h.category.value}
            for h in state.active_hypotheses
        ]
        data["pending_actions"] = [
            {**asdict(a), "status": a.status.value}
            for a in state.pending_actions
        ]
        return data

    def _deserialize(self, data: dict) -> SessionState:
        data["created_at"] = datetime.fromisoformat(data["created_at"])
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
