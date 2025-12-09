from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SqlEnum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from backend.app.database import Base


class UserRole(str, Enum):
    PLATFORM_ADMIN = "platform_admin"
    BFV_ADMIN = "bfv_admin"
    COACH = "coach"


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    city = Column(String(255))
    country = Column(String(255))
    address = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(255))
    website_url = Column(String(255))
    logo_url = Column(String(512))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("User", back_populates="club")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(SqlEnum(UserRole), nullable=False)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    club = relationship("Club", back_populates="users")
