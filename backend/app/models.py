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


class Ticket(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    business_id: str
    status: str = "open"
