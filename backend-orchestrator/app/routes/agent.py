"""
Agent routes — main entry point for incident analysis.
"""
import uuid
from fastapi import APIRouter, Request, Depends, HTTPException
from app.domain.schemas import IssueRequest, AgentResponse, ActionConfirmRequest
from app.services.orchestrator import OrchestratorService
from app.services.session_service import SessionService
from app.security.api_key import require_api_key

router = APIRouter()
_session_service = SessionService()
_orchestrator = OrchestratorService(_session_service)


@router.post("/issue", response_model=AgentResponse)
async def analyze_issue(
    request_body: IssueRequest,
    request: Request,
    _=Depends(require_api_key),
):
    correlation_id = getattr(request.state, "correlation_id", str(uuid.uuid4()))
    return await _orchestrator.process_issue(request_body, correlation_id)


@router.post("/confirm-action")
async def confirm_action(
    body: ActionConfirmRequest,
    request: Request,
    _=Depends(require_api_key),
):
    state = await _session_service.get(body.session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    action = next((a for a in state.pending_actions if a.id == body.action_id), None)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    from app.domain.models import ActionStatus
    action.status = ActionStatus.APPROVED if body.approved else ActionStatus.REJECTED
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    state.add_timeline_event("action_confirmed", {"action_id": body.action_id, "approved": body.approved})
    await _session_service.save(state)
    return {"action_id": body.action_id, "status": action.status.value}
