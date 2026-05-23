from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database.connection import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    ci = Column(String(30))
    phone = Column(String(30))
    email = Column(String(100))

    license = Column(String(50))
    license_expiry = Column(Date)

    address = Column(String(150))

    status = Column(String(50), default="active")

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id", ondelete="SET NULL"),
        nullable=True
    )