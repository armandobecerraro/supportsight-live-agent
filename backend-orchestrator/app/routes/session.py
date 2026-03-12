from fastapi import APIRouter, HTTPException, Depends
from app.services.session_service import SessionService
from app.security.api_key import require_api_key
import json

router = APIRouter()
_session_service = SessionService()

@router.get("/{session_id}")
async def get_session(session_id: str, _=Depends(require_api_key)):
    state = await _session_service.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": state.session_id,
        "incident_category": state.incident_category.value,
        "severity": state.severity.value,
        "resolved": state.resolved,
        "timeline": state.timeline,
        "hypotheses": [{"description": h.description, "confidence": h.confidence} for h in state.active_hypotheses],
    }

@router.get("/{session_id}/report")
async def get_report(session_id: str, _=Depends(require_api_key)):
    state = await _session_service.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    md = f"""# Incident Report — {session_id}

**Category:** {state.incident_category.value}
**Severity:** {state.severity.value}
**Status:** {"Resolved" if state.resolved else "Open"}

## Hypotheses
{chr(10).join(f"- {h.description} (confidence: {h.confidence:.0%})" for h in state.active_hypotheses)}

## Timeline
{chr(10).join(f"- `{e['timestamp']}` **{e['type']}**" for e in state.timeline)}
"""
    return {"session_id": session_id, "markdown_report": md, "timeline": state.timeline}
