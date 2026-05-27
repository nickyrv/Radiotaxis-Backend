from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base

class VehicleHistory(Base):
    __tablename__ = "vehicle_history"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True)

    category = Column(String(100), nullable=False)
    detail = Column(String(150), nullable=True)
    event_date = Column(Date, nullable=False)
    cost = Column(Numeric(10, 2), nullable=True)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())