from fastapi import APIRouter, Depends
from app.domain.schemas import LogAnalysisRequest, LogAnalysisResponse
from app.security.api_key import require_api_key
import httpx
from app.config import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/analyze", response_model=LogAnalysisResponse)
async def analyze_logs(body: LogAnalysisRequest, _=Depends(require_api_key)):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{settings.LOGS_SERVICE_URL}/analyze", json=body.model_dump())
            if r.status_code == 200:
                return r.json()
    except Exception:
        pass
    # Fallback: basic Python parsing
    lines = body.raw_logs.splitlines()
    errors = [l for l in lines if "ERROR" in l or "FATAL" in l]
    warnings = [l for l in lines if "WARN" in l]
    return LogAnalysisResponse(
        errors=errors[:20], warnings=warnings[:20], anomalies=[],
        probable_cause="Logs service unavailable — basic parsing applied."
    )
