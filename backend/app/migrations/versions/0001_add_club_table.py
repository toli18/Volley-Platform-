from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from backend.app.database import Base


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    city = Column(String(255))
    address = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(255))
    website_url = Column(String(255))
    logo_url = Column(String(512))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    coaches = relationship("User", back_populates="club")
    trainings = relationship("Training", back_populates="club")

