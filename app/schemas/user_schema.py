from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    related_id: Optional[int] = None
    status: str
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True