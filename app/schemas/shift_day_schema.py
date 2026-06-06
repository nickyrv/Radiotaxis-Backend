from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ShiftDayBase(BaseModel):

    vehicle_id: int
    driver_id: Optional[int] = None
    shift_date: date

    source: Optional[str] = "automatic"
    notes: Optional[str] = None


class ShiftDayCreate(ShiftDayBase):
    pass


class ShiftDayUpdate(BaseModel):

    driver_id: Optional[int] = None
    source: Optional[str] = "manual"
    notes: Optional[str] = None


class ShiftDayResponse(ShiftDayBase):

    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True