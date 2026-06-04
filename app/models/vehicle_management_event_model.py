from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.connection import Base


class VehicleManagementEvent(Base):

    __tablename__ = "vehicle_management_events"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    event_type = Column(String(50), nullable=False)

    event_datetime = Column(DateTime, server_default=func.now())

    notes = Column(String(255), nullable=True)