from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class PaymentBase(BaseModel):
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    trip_id: Optional[int] = None
    amount: Decimal
    type: str
    concept: str
    payment_date: date
    status: Optional[str] = "paid"
    observations: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int

    class Config:
        from_attributes = True