from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.services.agent import run_agent

router = APIRouter(prefix="/api/agent", tags=["agent"])


class AgentChatRequest(BaseModel):
    message: str
    business_id: Optional[str] = "default"


@router.post("/chat")
def agent_chat(request: AgentChatRequest):
    """Agent chat endpoint that intelligently decides whether to answer via RAG or trigger tools."""
    msg = request.message.strip() if request.message else ""
    if len(msg) < 3:
        raise HTTPException(
            status_code=400,
            detail="Message is required and must be at least 3 characters long.",
        )

    business_id = request.business_id or "default"
    result = run_agent(message=msg, business_id=business_id)
    return result
