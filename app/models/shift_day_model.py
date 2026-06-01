from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.connection import Base


class ShiftDay(Base):

    __tablename__ = "shift_days"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    driver_id = Column(
        Integer,
        ForeignKey("drivers.id"),
        nullable=False
    )

    shift_date = Column(Date, nullable=False)

    source = Column(String(50), default="automatic")

    notes = Column(String(255), nullable=True)

    created_at = Column(DateTime, server_default=func.now())