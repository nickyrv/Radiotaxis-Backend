from sqlalchemy import Column, Integer, String, Date, Numeric, Text, ForeignKey
from app.database.connection import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="SET NULL"), nullable=True)

    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(String(50), nullable=False)
    concept = Column(String(150), nullable=False)
    payment_date = Column(Date, nullable=False)
    status = Column(String(50), default="paid")
    observations = Column(Text)