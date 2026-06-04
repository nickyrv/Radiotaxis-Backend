from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal


class AlertBase(BaseModel):

    title: str
    description: Optional[str] = None

    type: str
    severity: str
    status: Optional[str] = "pending"

    alert_date: date
    due_date: Optional[date] = None
    completed_date: Optional[date] = None

    related_entity: Optional[str] = None
    related_id: Optional[int] = None

    vehicle_id: Optional[int] = None
    driver_id: Optional[int] = None

    category: Optional[str] = None

    estimated_cost: Optional[Decimal] = None
    final_cost: Optional[Decimal] = None

    is_recurring: Optional[bool] = False
    recurrence_value: Optional[int] = None
    recurrence_unit: Optional[str] = None

    notes: Optional[str] = None


class AlertCreate(AlertBase):
    pass


class AlertUpdate(AlertBase):
    pass


class AlertResponse(AlertBase):

    id: int

    class Config:
        from_attributes = True

class AlertComplete(BaseModel):
    final_cost: Optional[Decimal] = None
    notes: Optional[str] = None