from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, ForeignKey
from app.database.connection import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(150), nullable=False)
    destination = Column(String(150), nullable=False)
    trip_date = Column(DateTime, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), default="pending")

    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True)

    passenger_name = Column(String(100))
    passenger_phone = Column(String(30))
    observations = Column(Text)