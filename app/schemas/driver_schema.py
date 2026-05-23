from pydantic import BaseModel
from typing import Optional
from datetime import date

class DriverBase(BaseModel):

    name: str
    ci: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    license: Optional[str] = None
    license_expiry: Optional[date] = None

    address: Optional[str] = None

    status: Optional[str] = "active"

    vehicle_id: Optional[int] = None


class DriverCreate(DriverBase):
    pass


class DriverUpdate(DriverBase):
    pass


class DriverResponse(DriverBase):

    id: int

    class Config:
        from_attributes = True