"""
Domain models — pure Python dataclasses.
No framework dependencies (SOLID: Dependency Inversion).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class IncidentCategory(str, Enum):
    NETWORK = "network"
    DATABASE = "database"
    BACKEND = "backend"
    FRONTEND = "frontend"
    DEPLOYMENT = "deployment"
    PERMISSIONS = "permissions"
    EXTERNAL_INTEGRATION = "external_integration"
    PERFORMANCE = "performance"
    UNKNOWN = "unknown"


class IncidentSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ActionStatus(str, Enum):
    PENDING = "pending"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    FAILED = "failed"


@dataclass
class Hypothesis:
    description: str
    confidence: float          # 0.0 – 1.0
    evidence: list[str] = field(default_factory=list)
    category: IncidentCategory = IncidentCategory.UNKNOWN


@dataclass
class SuggestedAction:
    id: str
    title: str
    command: Optional[str]
    description: str
    is_destructive: bool = False
    requires_confirmation: bool = True
    status: ActionStatus = ActionStatus.PENDING


@dataclass
class SessionState:
    session_id: str
    correlation_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    problem_summary: str = ""
    active_hypotheses: list[Hypothesis] = field(default_factory=list)
    attempted_steps: list[str] = field(default_factory=list)
    incident_category: IncidentCategory = IncidentCategory.UNKNOWN
    severity: IncidentSeverity = IncidentSeverity.MEDIUM
    pending_actions: list[SuggestedAction] = field(default_factory=list)
    resolved: bool = False
    timeline: list[dict] = field(default_factory=list)

    def add_timeline_event(self, event_type: str, payload: dict):
        self.timeline.append({
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "payload": payload,
        })
