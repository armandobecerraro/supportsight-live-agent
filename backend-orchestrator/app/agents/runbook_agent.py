"""
Runbook/RAG Agent — queries local knowledge base for procedures and commands.
"""
import logging
from pathlib import Path
from app.infrastructure.gemini.client import GeminiClient
from app.prompts.loader import load_prompt

logger = logging.getLogger("supportsight.agents.runbook")

RUNBOOKS_DIR = Path(__file__).parent.parent.parent.parent / "docs" / "runbooks"


class RunbookAgent:
    def __init__(self, gemini: GeminiClient):
        self._gemini = gemini
        self._runbooks = self._load_runbooks()

    def _load_runbooks(self) -> str:
        """Load all runbook markdown files as context."""
        if not RUNBOOKS_DIR.exists():
            return ""
        content = []
        for f in RUNBOOKS_DIR.glob("*.md"):
            content.append(f"## {f.stem}\n{f.read_text()}")
        return "\n\n".join(content)

    async def query(self, incident_description: str, category: str) -> str:
        """Find relevant procedure from runbooks."""
        prompt = load_prompt("runbook_query").format(
            runbooks=self._runbooks or "No runbooks available.",
            description=incident_description,
            category=category,
        )
        return await self._gemini.generate(prompt)
