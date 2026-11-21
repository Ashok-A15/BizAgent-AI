import json
import re
import time
from typing import Dict, Any
import google.generativeai as genai
from app.config import GEMINI_API_KEY
from app.services.retrieval import retrieve_chunks
from app.services.chat import answer_question
from app.services.tools import create_ticket, book_appointment, save_lead, is_valid_date

AGENT_MODEL_NAME = "gemini-3.6-flash"

DECISION_PROMPT = """You are an AI decision engine for a business agent platform.
Decide ONE action from this message. Output ONLY valid JSON, no other text.
Actions:
- "answer": a normal question, greeting, inquiry, or if required info is missing.
- "book_appointment": customer wants to book an appointment.
  Fields to extract: customer_name, phone, date, time, service.
- "create_ticket": support issue or ticket.
  Fields to extract: title, description.
- "save_lead": customer lead or contact capture.
  Fields to extract: name, phone, interest.

If a required field is missing or invalid, or if details are incomplete, you may still choose "book_appointment", "create_ticket", or "save_lead" and extract what is present, or use action "answer" and ask for the missing field in plain words.

Output format (strictly valid JSON with no markdown formatting):
{
  "action": "answer" | "book_appointment" | "create_ticket" | "save_lead",
  "missing_info_question": null or "string asking for missing info",
  "fields": {
    "customer_name": null or "string",
    "name": null or "string",
    "phone": null or "string",
    "date": null or "string",
    "time": null or "string",
    "service": null or "string",
    "title": null or "string",
    "description": null or "string",
    "interest": null or "string"
  }
}

Message:
"""


def _clean_json_text(text: str) -> str:
    """Strip markdown code fence blocks if present."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _generate_content_with_retry(model, prompt, max_retries=3):
    """Generate content with retry for transient network timeouts."""
    last_err = None
    for attempt in range(max_retries):
        try:
            return model.generate_content(prompt)
        except Exception as e:
            last_err = e
            if attempt < max_retries - 1:
                time.sleep(1.5)
            else:
                raise last_err


def run_agent(message: str, business_id: str = "default") -> Dict[str, Any]:
    """Decide and execute an agent action (answer or tool call) for a user message."""
    if not message or not message.strip():
        return {
            "reply": "Please provide a valid message.",
            "action": "answer",
            "tool_result": None,
            "sources": [],
            "retrieved_chunks": 0,
        }

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name=AGENT_MODEL_NAME)

    # 1. Decide action with Gemini
    decision_response = _generate_content_with_retry(model, DECISION_PROMPT + message)
    raw_decision = _clean_json_text(decision_response.text or "{}")

    try:
        decision_data = json.loads(raw_decision)
    except Exception:
        decision_data = {"action": "answer", "fields": {}}

    action = decision_data.get("action", "answer")
    fields = decision_data.get("fields", {}) or {}
    missing_q = decision_data.get("missing_info_question")

    # Check for date format in message if appointment intent exists
    date_match = re.search(r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{4})\b", message)
    if "appointment" in message.lower() and date_match:
        raw_d = date_match.group(1)
        if not is_valid_date(raw_d):
            return {
                "reply": f"The date '{raw_d}' is invalid. Please provide the appointment date in YYYY-MM-DD format (for example 2026-11-25).",
                "action": "book_appointment",
                "tool_result": {"error": "Invalid date format. Expected YYYY-MM-DD.", "status": 400},
                "sources": [],
                "retrieved_chunks": 0,
            }

    # 2. Execute matching action
    if action == "book_appointment":
        customer_name = fields.get("customer_name") or fields.get("name") or "Customer"
        phone = fields.get("phone") or "Not provided"
        date_val = fields.get("date") or ""
        time_val = fields.get("time") or ""
        service = fields.get("service") or "General Consultation"

        # Validate date format explicitly
        if not is_valid_date(date_val):
            return {
                "reply": "Please provide the appointment date in YYYY-MM-DD format (for example 2026-11-25).",
                "action": "book_appointment",
                "tool_result": {"error": "Invalid date format. Expected YYYY-MM-DD.", "status": 400},
                "sources": [],
                "retrieved_chunks": 0,
            }

        tool_result = book_appointment(
            customer_name=customer_name,
            phone=phone,
            date=date_val,
            time=time_val,
            service=service,
            business_id=business_id,
        )

        if "error" in tool_result:
            return {
                "reply": f"{tool_result['error']}",
                "action": "book_appointment",
                "tool_result": tool_result,
                "sources": [],
                "retrieved_chunks": 0,
            }

        appt_id = tool_result.get("appointment_id")
        conf_prompt = (
            f"Write a friendly 1-2 sentence confirmation to the customer for their booked appointment. "
            f"Customer: {customer_name}, Date: {date_val}, Time: {time_val}, Service: {service}. "
            f"You MUST include the confirmation ID: {appt_id}."
        )
        try:
            conf_res = _generate_content_with_retry(model, conf_prompt)
            reply = conf_res.text.strip() if conf_res.text else f"Appointment confirmed with ID: {appt_id}."
        except Exception:
            reply = f"Appointment confirmed for {customer_name} on {date_val} at {time_val} with ID: {appt_id}."

        return {
            "reply": reply,
            "action": "book_appointment",
            "tool_result": tool_result,
            "sources": [],
            "retrieved_chunks": 0,
        }

    elif action == "create_ticket":
        title = fields.get("title") or message[:50]
        desc = fields.get("description") or message
        tool_result = create_ticket(title=title, description=desc, business_id=business_id)
        ticket_id = tool_result.get("ticket_id")

        conf_prompt = (
            f"Write a polite 1-2 sentence confirmation to the customer that their support ticket has been created. "
            f"Issue: {title}. You MUST include the Ticket ID: {ticket_id}."
        )
        try:
            conf_res = _generate_content_with_retry(model, conf_prompt)
            reply = conf_res.text.strip() if conf_res.text else f"Ticket created successfully with ID: {ticket_id}."
        except Exception:
            reply = f"Support ticket created successfully with ID: {ticket_id}."

        return {
            "reply": reply,
            "action": "create_ticket",
            "tool_result": tool_result,
            "sources": [],
            "retrieved_chunks": 0,
        }

    elif action == "save_lead":
        name = fields.get("name") or fields.get("customer_name") or "Prospective Customer"
        phone = fields.get("phone") or "Not provided"
        interest = fields.get("interest") or ""

        tool_result = save_lead(name=name, phone=phone, business_id=business_id, interest=interest)
        lead_id = tool_result.get("lead_id")

        conf_prompt = (
            f"Write a polite 1-2 sentence message acknowledging the saved lead for {name}. "
            f"You MUST include the Lead ID: {lead_id}."
        )
        try:
            conf_res = _generate_content_with_retry(model, conf_prompt)
            reply = conf_res.text.strip() if conf_res.text else f"Lead saved successfully with ID: {lead_id}."
        except Exception:
            reply = f"Lead details saved successfully for {name} with ID: {lead_id}."

        return {
            "reply": reply,
            "action": "save_lead",
            "tool_result": tool_result,
            "sources": [],
            "retrieved_chunks": 0,
        }

    # Action is 'answer'
    if missing_q:
        return {
            "reply": missing_q,
            "action": "answer",
            "tool_result": None,
            "sources": [],
            "retrieved_chunks": 0,
        }

    # Standard RAG flow using retrieval and chat
    chunks = retrieve_chunks(question=message, business_id=business_id, top_k=4)
    chat_result = answer_question(question=message, chunks=chunks)

    return {
        "reply": chat_result["answer"],
        "action": "answer",
        "tool_result": None,
        "sources": chat_result["sources"],
        "retrieved_chunks": len(chunks),
    }
