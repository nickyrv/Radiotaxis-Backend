from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database.connection import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)

    plate = Column(String(20), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)

    owner_id = Column(Integer, nullable=True)

    service_type = Column(String(50), default="radio_taxi")
    radio_code = Column(String(20), nullable=True)

    status = Column(String(50), default="active")

    last_maintenance = Column(Date)
    next_maintenance = Column(Date)

    photo_url = Column(String(255), nullable=True)
    color = Column(String(50), nullable=True)
    restriction_day = Column(String(20), nullable=True)

    registration_date = Column(Date, nullable=True)
    deactivation_date = Column(Date, nullable=True)

    management_status = Column(String(50), default="active")
    management_type = Column(String(50), default="solo")

    current_driver_id = Column(
        Integer,
        ForeignKey("drivers.id", ondelete="SET NULL"),
        nullable=True
    )

    admin_id = Column(Integer, nullable=True)
    company_name = Column(String(100), nullable=True)