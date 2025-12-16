from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from backend.app.database import Base


# =========================
# User roles
# =========================
class UserRole(str, Enum):
    platform_admin = "platform_admin"
    bfv_admin = "bfv_admin"
    coach = "coach"


# =========================
# Drill status (LIFECYCLE)
# =========================
class DrillStatus(str, Enum):
    draft = "draft"         # coach – чернова
    submitted = "submitted" # coach → bfv
    approved = "approved"   # bfv_admin


# =========================
# Clubs
# =========================
class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = relationship("User", back_populates="club")


# =========================
# Users
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(SqlEnum(UserRole), nullable=False)

    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    club = relationship("Club", back_populates="users")


# =========================
# Drills
# =========================
class Drill(Base):
    __tablename__ = "drills"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)
    level = Column(String(255))

    description = Column(Text)

    age_min = Column(Integer)
    age_max = Column(Integer)

    # ⭐ НОВО
    status = Column(
        SqlEnum(DrillStatus),
        nullable=False,
        default=DrillStatus.draft,
        server_default=DrillStatus.draft.value,
    )

    created_at = Column(DateTime, server_default=func.now())
