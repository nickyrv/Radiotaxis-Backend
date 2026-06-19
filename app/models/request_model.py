from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.connection import Base


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)

    requester_role = Column(String(50), nullable=False)
    requester_id = Column(Integer, nullable=False)

    owner_id = Column(Integer, ForeignKey("owners.id", ondelete="SET NULL"), nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id", ondelete="SET NULL"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True)

    request_type = Column(String(50), nullable=False)
    request_status = Column(String(50), nullable=False, default="pending")

    deactivation_type = Column(String(50), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    reason = Column(Text, nullable=True)
    details = Column(Text, nullable=True)

    admin_response = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    reviewed_at = Column(DateTime, nullable=True)