from pydantic import BaseModel
from typing import Optional
from datetime import date

class VehicleBase(BaseModel):
    plate: str
    model: str
    year: int
    owner_id: Optional[int] = None
    status: Optional[str] = "active"
    last_maintenance: Optional[date] = None
    next_maintenance: Optional[date] = None
    document_expiry: Optional[date] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int

    class Config:
        from_attributes = True