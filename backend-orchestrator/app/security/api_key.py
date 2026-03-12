"""
API Key authentication — OWASP: Broken Authentication mitigation.
In production, rotate keys and use Secret Manager.
"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config import get_settings

settings = get_settings()
_api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER, auto_error=False)


async def require_api_key(api_key: str = Security(_api_key_header)):
    # If no key configured, allow all (development mode)
    if not settings.SECRET_KEY or settings.DEBUG:
        return
    if not api_key or api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
