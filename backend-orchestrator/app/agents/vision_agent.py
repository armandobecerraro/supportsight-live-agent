"""
Vision/Context Agent — interprets screenshots and visual error context.
Single Responsibility: visual analysis only.
"""
import logging
from typing import Optional
from app.infrastructure.gemini.client import GeminiClient
from app.prompts.loader import load_prompt

logger = logging.getLogger("supportsight.agents.vision")


class VisionAgent:
    def __init__(self, gemini: GeminiClient):
        self._gemini = gemini

    async def analyze(self, image_base64: str, description: str) -> str:
        """Describe what the agent sees in the screenshot."""
        prompt = load_prompt("vision_analysis").format(description=description)
        result = await self._gemini.generate(prompt, image_base64=image_base64)
        logger.info({"event": "vision_analysis_done", "chars": len(result)})
        return result
