"""
Action Agent — prepares executable actions with mandatory human confirmation.
Safety-first: all destructive actions require explicit approval.
"""
import logging
import uuid
from typing import Optional
from app.domain.models import SuggestedAction, ActionStatus
from app.infrastructure.gemini.client import GeminiClient
from app.prompts.loader import load_prompt

logger = logging.getLogger("supportsight.agents.action")

# Allowlist of safe commands — everything else is flagged as destructive
SAFE_COMMANDS_PREFIX = [
    "grep ", "cat ", "tail ", "head ", "ls ", "df ", "du ", "ps ",
    "curl -X GET", "kubectl get", "kubectl describe", "kubectl logs",
]


class ActionAgent:
    def __init__(self, gemini: GeminiClient):
        self._gemini = gemini

    async def prepare(
        self, description: str, hypotheses: list, runbook_context: str
    ) -> list[SuggestedAction]:
        prompt = load_prompt("action_preparation").format(
            description=description,
            hypotheses="\n".join([h.description for h in hypotheses]),
            runbook_context=runbook_context,
        )
        raw = await self._gemini.generate(prompt)
        return self._parse_actions(raw)

    def _parse_actions(self, raw: str) -> list[SuggestedAction]:
        import json
        try:
            data = json.loads(raw.strip("```json\n").strip("```"))
            actions = []
            for a in data.get("actions", [])[:5]:  # max 5 actions
                cmd = a.get("command")
                is_safe = cmd and any(cmd.startswith(p) for p in SAFE_COMMANDS_PREFIX)
                actions.append(SuggestedAction(
                    id=str(uuid.uuid4()),
                    title=a.get("title", "Action"),
                    command=cmd,
                    description=a.get("description", ""),
                    is_destructive=not is_safe,
                    requires_confirmation=True,
                    status=ActionStatus.AWAITING_CONFIRMATION,
                ))
            return actions
        except Exception as exc:
            logger.warning({"event": "action_parse_error", "error": str(exc)})
            return []
