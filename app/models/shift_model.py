from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.connection import Base

class Shift(Base):

    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)

    driver_id = Column(
        Integer,
        ForeignKey("drivers.id", ondelete="SET NULL"),
        nullable=True
    )

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id", ondelete="SET NULL"),
        nullable=True
    )

    start_time = Column(DateTime, nullable=False)

    end_time = Column(DateTime, nullable=False)

    status = Column(String(50), default="scheduled")

    turn_order = Column(Integer, default=1)

    is_active = Column(Integer, default=1)