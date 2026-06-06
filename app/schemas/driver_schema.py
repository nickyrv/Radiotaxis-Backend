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
    address_lat: Optional[float] = None
    address_lng: Optional[float] = None

    status: Optional[str] = "active"

    vehicle_id: Optional[int] = None
    has_tic: Optional[bool] = False
    license_category: Optional[str] = None
    photo_url: Optional[str] = None
    house_door_photo_url: Optional[str] = None
    ci_front_photo_url: Optional[str] = None
    ci_back_photo_url: Optional[str] = None
    electricity_bill_photo_url: Optional[str] = None
    criminal_record_pdf_url: Optional[str] = None

class DriverCreate(DriverBase):
    pass


class DriverUpdate(DriverBase):
    pass


class DriverResponse(DriverBase):

    id: int

    class Config:
        from_attributes = True