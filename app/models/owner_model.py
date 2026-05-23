from sqlalchemy import Column, Integer, String, Date
from app.database.connection import Base

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    ci = Column(String(30))
    phone = Column(String(30))
    email = Column(String(100))
    address = Column(String(150))
    status = Column(String(50), default="active")
    join_date = Column(Date)