from pydantic import BaseModel
from typing import Optional
from datetime import date


class VehicleBase(BaseModel):

    plate: str
    model: str
    year: int

    owner_id: Optional[int] = None

    service_type: Optional[str] = "radio_taxi"
    radio_code: Optional[str] = None

    status: Optional[str] = "active"

    last_maintenance: Optional[date] = None
    next_maintenance: Optional[date] = None

    photo_url: Optional[str] = None
    color: Optional[str] = None

    restriction_day: Optional[str] = None

    registration_date: Optional[date] = None
    deactivation_date: Optional[date] = None

    management_status: Optional[str] = "active"
    management_type: Optional[str] = "solo"

    current_driver_id: Optional[int] = None

    admin_id: Optional[int] = None
    company_name: Optional[str] = None


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(VehicleBase):
    pass


class VehicleResponse(VehicleBase):

    id: int

    class Config:
        from_attributes = True