from datetime import datetime
from typing import Dict, Any
from app.database import get_database


def is_valid_date(date_str: str) -> bool:
    """Validate string matches YYYY-MM-DD exactly."""
    if not isinstance(date_str, str):
        return False
    try:
        dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d") == date_str.strip()
    except ValueError:
        return False


def is_valid_time(time_str: str) -> bool:
    """Validate string matches HH:MM (24-hour format) exactly."""
    if not isinstance(time_str, str):
        return False
    try:
        dt = datetime.strptime(time_str.strip(), "%H:%M")
        return dt.strftime("%H:%M") == time_str.strip()
    except ValueError:
        return False


def create_ticket(title: str, description: str, business_id: str) -> Dict[str, Any]:
    """Create a support ticket in MongoDB with status 'open'.

    Args:
        title: Short title of the ticket.
        description: Full details of the issue.
        business_id: Business identifier.

    Returns:
        Dict with real MongoDB inserted_id and status 'open'.
    """
    db = get_database()
    doc = {
        "title": title,
        "description": description,
        "business_id": business_id,
        "status": "open",
        "created_at": datetime.utcnow().isoformat(),
    }
    result = db.tickets.insert_one(doc)
    return {
        "ticket_id": str(result.inserted_id),
        "status": "open",
    }


def book_appointment(
    customer_name: str,
    phone: str,
    date: str,
    time: str,
    service: str,
    business_id: str,
) -> Dict[str, Any]:
    """Validate date and time, and save an appointment in MongoDB with status 'booked'.

    Args:
        customer_name: Customer's full name.
        phone: Customer's contact number.
        date: Appointment date in YYYY-MM-DD format.
        time: Appointment time in HH:MM format.
        service: Requested service or consultation.
        business_id: Business identifier.

    Returns:
        Dict with real MongoDB inserted_id and status 'booked', or error dict on invalid input.
    """
    date_clean = (date or "").strip()
    time_clean = (time or "").strip()

    if not is_valid_date(date_clean):
        return {
            "error": f"Invalid date format '{date}'. Please provide date in YYYY-MM-DD format.",
            "status": 400,
        }

    if not is_valid_time(time_clean):
        return {
            "error": f"Invalid time format '{time}'. Please provide time in HH:MM format (24-hour).",
            "status": 400,
        }

    db = get_database()
    doc = {
        "customer_name": customer_name,
        "phone": phone,
        "date": date_clean,
        "time": time_clean,
        "service": service,
        "business_id": business_id,
        "status": "booked",
        "created_at": datetime.utcnow().isoformat(),
    }
    result = db.appointments.insert_one(doc)
    return {
        "appointment_id": str(result.inserted_id),
        "status": "booked",
    }


def save_lead(name: str, phone: str, business_id: str, interest: str = "") -> Dict[str, Any]:
    """Save a prospective customer lead in MongoDB.

    Args:
        name: Lead's name.
        phone: Lead's contact number.
        business_id: Business identifier.
        interest: Optional topic or service of interest.

    Returns:
        Dict with real MongoDB inserted_id.
    """
    db = get_database()
    doc = {
        "name": name,
        "phone": phone,
        "business_id": business_id,
        "interest": interest or "",
        "created_at": datetime.utcnow().isoformat(),
    }
    result = db.leads.insert_one(doc)
    return {
        "lead_id": str(result.inserted_id),
    }
