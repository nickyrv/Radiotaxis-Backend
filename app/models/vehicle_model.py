from sqlalchemy import Column, Integer, String, Date
from app.database.connection import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String(20), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    owner_id = Column(Integer)
    status = Column(String(50), default="active")
    last_maintenance = Column(Date)
    next_maintenance = Column(Date)
    document_expiry = Column(Date)