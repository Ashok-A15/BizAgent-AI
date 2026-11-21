import sys
from pathlib import Path

# Add backend directory to sys.path so app imports work cleanly
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv(backend_dir / ".env")

from mcp.server.fastmcp import FastMCP
from app.services.retrieval import retrieve_chunks
from app.services.tools import (
    book_appointment as tools_book_appointment,
    create_ticket as tools_create_ticket,
    save_lead as tools_save_lead,
)

mcp = FastMCP("bizagent-mcp")


@mcp.tool()
def search_documents(question: str, business_id: str = "default") -> list:
    """Search uploaded business documents for relevant information.

    Args:
        question: Question or search query.
        business_id: Business identifier.

    Returns:
        List of top chunks with filename and document_id.
    """
    return retrieve_chunks(question=question, business_id=business_id)


@mcp.tool()
def book_appointment(
    customer_name: str,
    phone: str,
    date: str,
    time: str,
    service: str,
    business_id: str = "default",
) -> dict:
    """Book an appointment for a customer.

    Args:
        customer_name: Customer's full name.
        phone: Customer's phone number.
        date: Appointment date in YYYY-MM-DD format.
        time: Appointment time in HH:MM format (24-hour).
        service: Requested service or consultation.
        business_id: Business identifier.

    Returns:
        Dict with appointment_id and status.
    """
    return tools_book_appointment(
        customer_name=customer_name,
        phone=phone,
        date=date,
        time=time,
        service=service,
        business_id=business_id,
    )


@mcp.tool()
def create_ticket(
    title: str,
    description: str,
    business_id: str = "default",
) -> dict:
    """Create a support ticket.

    Args:
        title: Short title of the ticket.
        description: Full details of the issue.
        business_id: Business identifier.

    Returns:
        Dict with ticket_id and status.
    """
    return tools_create_ticket(
        title=title,
        description=description,
        business_id=business_id,
    )


@mcp.tool()
def save_lead(
    name: str,
    phone: str,
    business_id: str = "default",
    interest: str = "",
) -> dict:
    """Save a prospective customer lead.

    Args:
        name: Lead's name.
        phone: Lead's contact phone number.
        business_id: Business identifier.
        interest: Optional topic or service of interest.

    Returns:
        Dict with lead_id.
    """
    return tools_save_lead(
        name=name,
        phone=phone,
        business_id=business_id,
        interest=interest,
    )


if __name__ == "__main__":
    mcp.run()
