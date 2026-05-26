from pydantic import BaseModel
from typing import Optional
from datetime import date

class AlertBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: str
    severity: str
    status: Optional[str] = "pending"
    alert_date: date
    related_entity: Optional[str] = None
    related_id: Optional[int] = None

class AlertCreate(AlertBase):
    pass

class AlertUpdate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int

    class Config:
        from_attributes = True