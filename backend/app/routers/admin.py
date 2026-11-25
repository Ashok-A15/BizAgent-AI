from typing import Dict, Any, List
from fastapi import APIRouter
from app.database import get_database, check_mongo_connection

router = APIRouter(prefix="/api/admin", tags=["admin"])


def clean_mongo_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB _id to string 'id'."""
    d = dict(doc)
    if "_id" in d:
        d["id"] = str(d.pop("_id"))
    return d


@router.get("/tickets")
def get_admin_tickets() -> Dict[str, List[Dict[str, Any]]]:
    """Return the 50 newest support tickets."""
    if not check_mongo_connection():
        return {"tickets": []}
    try:
        db = get_database()
        cursor = db.tickets.find().sort("_id", -1).limit(50)
        tickets = [clean_mongo_doc(doc) for doc in cursor]
        return {"tickets": tickets}
    except Exception:
        return {"tickets": []}


@router.get("/appointments")
def get_admin_appointments() -> Dict[str, List[Dict[str, Any]]]:
    """Return the 50 newest appointments."""
    if not check_mongo_connection():
        return {"appointments": []}
    try:
        db = get_database()
        cursor = db.appointments.find().sort("_id", -1).limit(50)
        appointments = [clean_mongo_doc(doc) for doc in cursor]
        return {"appointments": appointments}
    except Exception:
        return {"appointments": []}


@router.get("/leads")
def get_admin_leads() -> Dict[str, List[Dict[str, Any]]]:
    """Return the 50 newest leads."""
    if not check_mongo_connection():
        return {"leads": []}
    try:
        db = get_database()
        cursor = db.leads.find().sort("_id", -1).limit(50)
        leads = [clean_mongo_doc(doc) for doc in cursor]
        return {"leads": leads}
    except Exception:
        return {"leads": []}
