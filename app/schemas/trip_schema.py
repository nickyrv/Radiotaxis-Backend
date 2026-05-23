from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class TripBase(BaseModel):
    origin: str
    destination: str
    trip_date: datetime
    price: Decimal
    status: Optional[str] = "pending"
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    passenger_name: Optional[str] = None
    passenger_phone: Optional[str] = None
    observations: Optional[str] = None

class TripCreate(TripBase):
    pass

class TripUpdate(TripBase):
    pass

class TripResponse(TripBase):
    id: int

    class Config:
        from_attributes = True