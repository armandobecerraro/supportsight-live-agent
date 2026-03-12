"""
Gemini Live API client — infrastructure layer.
Wraps Google GenAI SDK. Supports text, multimodal (vision) and streaming.
"""
import base64
import logging
from typing import Optional, AsyncGenerator

import google.generativeai as genai
from google.generativeai.types import GenerationConfig

from app.config import get_settings

logger = logging.getLogger("supportsight.gemini")
settings = get_settings()

genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiClient:
    """Single-responsibility: communicate with Gemini API."""

    def __init__(self):
        self._model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            generation_config=GenerationConfig(
                temperature=settings.GEMINI_TEMPERATURE,
                max_output_tokens=settings.GEMINI_MAX_TOKENS,
            ),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            ],
        )

    async def generate(self, prompt: str, image_base64: Optional[str] = None) -> str:
        """Generate a response from text + optional image."""
        parts = [prompt]
        if image_base64:
            parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": image_base64,
                }
            })
        try:
            response = await self._model.generate_content_async(parts)
            return response.text
        except Exception as exc:
            logger.error({"event": "gemini_error", "error": str(exc)})
            raise

    async def stream_generate(
        self, prompt: str, image_base64: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """Stream tokens from Gemini."""
        parts = [prompt]
        if image_base64:
            parts.append({"inline_data": {"mime_type": "image/png", "data": image_base64}})
        async for chunk in await self._model.generate_content_async(parts, stream=True):
            if chunk.text:
                yield chunk.text

    async def chat(self, history: list[dict], new_message: str) -> str:
        """Multi-turn conversation using chat session."""
        chat_session = self._model.start_chat(history=history)
        response = await chat_session.send_message_async(new_message)
        return response.text
