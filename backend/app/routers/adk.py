import uuid
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.adk_agent import bizagent_agent, current_business_id

router = APIRouter(prefix="/api/adk", tags=["adk"])

session_service = InMemorySessionService()


class ADKChatRequest(BaseModel):
    message: str
    business_id: Optional[str] = "default"


@router.post("/chat")
async def adk_chat(request: ADKChatRequest):
    """Run the Google ADK agent for chat with small business documents and tools."""
    if not request.message or len(request.message.strip()) < 3:
        raise HTTPException(
            status_code=400,
            detail="Message is required and must be at least 3 characters.",
        )

    business_id = request.business_id or "default"
    current_business_id.set(business_id)

    user_id = "user_default"
    session_id = f"session_{uuid.uuid4().hex[:8]}"

    session = await session_service.create_session(
        app_name="bizagent_app",
        user_id=user_id,
        session_id=session_id,
    )

    runner = Runner(
        app_name="bizagent_app",
        agent=bizagent_agent,
        session_service=session_service,
    )

    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=request.message.strip())],
    )

    action = "answer"
    tool_result = None
    reply_parts = []

    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=user_content,
        ):
            # Check function calls
            for fc in event.get_function_calls():
                fname = getattr(fc, "name", "")
                if fname in ("book_appointment", "create_ticket", "save_lead"):
                    action = fname

            # Check function responses
            for fr in event.get_function_responses():
                fname = getattr(fr, "name", "")
                if fname in ("book_appointment", "create_ticket", "save_lead"):
                    action = fname
                    raw_resp = getattr(fr, "response", None)
                    if isinstance(raw_resp, dict):
                        if "result" in raw_resp and isinstance(raw_resp["result"], dict):
                            tool_result = raw_resp["result"]
                        else:
                            tool_result = raw_resp
                    elif hasattr(raw_resp, "model_dump"):
                        dumped = raw_resp.model_dump()
                        if "result" in dumped and isinstance(dumped["result"], dict):
                            tool_result = dumped["result"]
                        else:
                            tool_result = dumped
                    else:
                        tool_result = raw_resp

            # Collect text reply parts
            if event.content and event.content.parts:
                for p in event.content.parts:
                    t = getattr(p, "text", None)
                    if t:
                        reply_parts.append(t)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    reply = "".join(reply_parts).strip()
    return {
        "reply": reply,
        "action": action,
        "tool_result": tool_result,
    }
