from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ShiftBase(BaseModel):

    driver_id: Optional[int] = None

    vehicle_id: Optional[int] = None

    start_time: datetime

    end_time: datetime

    status: Optional[str] = "scheduled"

    turn_order: Optional[int] = 1

    is_active: Optional[int] = 1


class ShiftCreate(ShiftBase):
    pass


class ShiftUpdate(ShiftBase):
    pass


class ShiftResponse(ShiftBase):

    id: int

    class Config:
        from_attributes = True