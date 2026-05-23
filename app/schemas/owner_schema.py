from pydantic import BaseModel
from typing import Optional
from datetime import date

class OwnerBase(BaseModel):
    name: str
    ci: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = "active"
    join_date: Optional[date] = None

class OwnerCreate(OwnerBase):
    pass

class OwnerUpdate(OwnerBase):
    pass

class OwnerResponse(OwnerBase):
    id: int

    class Config:
        from_attributes = True