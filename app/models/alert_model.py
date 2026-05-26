from sqlalchemy import Column, Integer, String, Text, Date
from app.database.connection import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)
    severity = Column(String(50), nullable=False)
    status = Column(String(50), default="pending")
    alert_date = Column(Date, nullable=False)
    related_entity = Column(String(50))
    related_id = Column(Integer)