from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class VehicleHistoryBase(BaseModel):
    vehicle_id: int
    driver_id: Optional[int] = None
    category: str
    detail: Optional[str] = None
    event_date: date
    cost: Optional[Decimal] = None
    description: Optional[str] = None

class VehicleHistoryCreate(VehicleHistoryBase):
    pass

class VehicleHistoryUpdate(VehicleHistoryBase):
    pass

class VehicleHistoryResponse(VehicleHistoryBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True