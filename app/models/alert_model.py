from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey, Boolean
from app.database.connection import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)
    description = Column(Text)

    type = Column(String(50), nullable=False)  # vehicle / driver
    severity = Column(String(50), nullable=False)  # low / medium / high / expired
    status = Column(String(50), default="pending")  # pending / completed / expired / cancelled

    alert_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)

    related_entity = Column(String(50))
    related_id = Column(Integer)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)

    category = Column(String(100), nullable=True)

    estimated_cost = Column(Numeric(10, 2), nullable=True)
    final_cost = Column(Numeric(10, 2), nullable=True)

    is_recurring = Column(Boolean, default=False)

    recurrence_value = Column(Integer, nullable=True)

    recurrence_unit = Column(String(20), nullable=True)

    notes = Column(String(255), nullable=True)