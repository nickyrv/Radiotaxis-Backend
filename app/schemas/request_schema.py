from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class RequestBase(BaseModel):
    requester_role: str
    requester_id: int

    owner_id: Optional[int] = None
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None

    request_type: str
    request_status: Optional[str] = "pending"

    deactivation_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    reason: Optional[str] = None
    details: Optional[str] = None

    admin_response: Optional[str] = None


class RequestCreate(RequestBase):
    pass


class RequestUpdate(BaseModel):
    request_status: Optional[str] = None
    admin_response: Optional[str] = None


class RequestResponse(RequestBase):
    id: int
    created_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True