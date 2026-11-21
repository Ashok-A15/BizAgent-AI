from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException
from app.services.retrieval import retrieve_chunks
from app.services.chat import answer_question

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str
    business_id: Optional[str] = "default"
    top_k: Optional[int] = 4


@router.post("")
@router.post("/")
def chat_endpoint(request: ChatRequest):
    """Answer questions strictly based on uploaded business documents."""
    q = request.question.strip() if request.question else ""
    if len(q) < 3:
        raise HTTPException(
            status_code=400,
            detail="Question is required and must be at least 3 characters long.",
        )

    business_id = request.business_id or "default"
    top_k = request.top_k if (request.top_k and request.top_k > 0) else 4

    chunks = retrieve_chunks(question=q, business_id=business_id, top_k=top_k)
    chat_result = answer_question(question=q, chunks=chunks)

    return {
        "answer": chat_result["answer"],
        "sources": chat_result["sources"],
        "retrieved_chunks": len(chunks),
        "business_id": business_id,
    }
