from pydantic import BaseModel
from typing import Optional
from datetime import date

class IncidentBase(BaseModel):
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    type: str
    description: str
    incident_date: date
    status: Optional[str] = "pending"

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(IncidentBase):
    pass

class IncidentResponse(IncidentBase):
    id: int

    class Config:
        from_attributes = True