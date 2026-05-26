from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from app.database.connection import Base

class Incident(Base):
    __tablename__ = "incidents"

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

    type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    incident_date = Column(Date, nullable=False)
    status = Column(String(50), default="pending")