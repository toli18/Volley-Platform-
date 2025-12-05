from sqlalchemy import Column, DateTime, Integer, String, func

from .database import Base


class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    city = Column(String(255))
    country = Column(String(255))
    address = Column(String(255))
    contact_email = Column(String(255))
    contact_phone = Column(String(50))
    website_url = Column(String(255))
    logo_url = Column(String(512))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
