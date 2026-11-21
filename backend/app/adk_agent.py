from contextvars import ContextVar
from typing import List, Dict, Any

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from app.services.retrieval import retrieve_chunks
from app.services.tools import (
    book_appointment as tools_book_appointment,
    create_ticket as tools_create_ticket,
    save_lead as tools_save_lead,
)

current_business_id: ContextVar[str] = ContextVar("current_business_id", default="default")

INSTRUCTION = (
    "You are BizAgent, an AI agent for a small business. "
    "Answer ONLY from the business documents (use search_documents). "
    "If the user asks to book an appointment, create a ticket, or save a lead, use the matching tool. "
    "If the answer is not in the documents, say 'I don't know based on the documents provided.' "
    "Do not invent facts."
)


def search_documents(question: str, business_id: str = "") -> List[Dict[str, Any]]:
    """Search uploaded business documents for relevant information.

    Args:
        question: The user question or search query.
        business_id: Optional business identifier. Defaults to the current active business.

    Returns:
        List of chunks with text, document_id, filename, and business_id.
    """
    bid = business_id or current_business_id.get() or "default"
    return retrieve_chunks(question=question, business_id=bid)


def book_appointment(
    customer_name: str,
    phone: str,
    date: str,
    time: str,
    service: str,
    business_id: str = "",
) -> Dict[str, Any]:
    """Book an appointment for a customer.

    Args:
        customer_name: Customer's full name.
        phone: Customer's contact phone number.
        date: Appointment date in YYYY-MM-DD format.
        time: Appointment time in HH:MM format (24-hour).
        service: Requested service or consultation.
        business_id: Optional business identifier.

    Returns:
        Dict with appointment_id and status.
    """
    bid = business_id or current_business_id.get() or "default"
    return tools_book_appointment(
        customer_name=customer_name,
        phone=phone,
        date=date,
        time=time,
        service=service,
        business_id=bid,
    )


def create_ticket(
    title: str,
    description: str,
    business_id: str = "",
) -> Dict[str, Any]:
    """Create a support ticket.

    Args:
        title: Short title of the ticket.
        description: Full details of the issue.
        business_id: Optional business identifier.

    Returns:
        Dict with ticket_id and status.
    """
    bid = business_id or current_business_id.get() or "default"
    return tools_create_ticket(
        title=title,
        description=description,
        business_id=bid,
    )


def save_lead(
    name: str,
    phone: str,
    business_id: str = "",
    interest: str = "",
) -> Dict[str, Any]:
    """Save a prospective customer lead.

    Args:
        name: Lead's name.
        phone: Lead's contact phone number.
        business_id: Optional business identifier.
        interest: Optional topic or service of interest.

    Returns:
        Dict with lead_id.
    """
    bid = business_id or current_business_id.get() or "default"
    return tools_save_lead(
        name=name,
        phone=phone,
        business_id=bid,
        interest=interest,
    )


adk_tools = [
    FunctionTool(search_documents),
    FunctionTool(book_appointment),
    FunctionTool(create_ticket),
    FunctionTool(save_lead),
]

bizagent_agent = Agent(
    name="bizagent_agent",
    model="gemini-3.6-flash",
    instruction=INSTRUCTION,
    tools=adk_tools,
)
