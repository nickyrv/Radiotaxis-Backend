from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VehicleManagementEventBase(BaseModel):

    vehicle_id: int
    event_type: str
    notes: Optional[str] = None


class VehicleManagementEventCreate(VehicleManagementEventBase):
    pass


class VehicleManagementEventResponse(VehicleManagementEventBase):

    id: int
    event_datetime: Optional[datetime] = None

    class Config:
        from_attributes = True