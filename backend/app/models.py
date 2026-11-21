from typing import Optional
from pydantic import BaseModel


class Business(BaseModel):
    id: Optional[str] = None
    name: str
    email: str


class Lead(BaseModel):
    id: Optional[str] = None
    name: str
    phone: str
    business_id: str
    interest: Optional[str] = ""


class Ticket(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    business_id: str
    status: str = "open"


class Appointment(BaseModel):
    id: Optional[str] = None
    business_id: str
    customer_name: str
    phone: str
    date: str  # format YYYY-MM-DD
    time: str  # format HH:MM
    service: str
    status: str = "booked"
