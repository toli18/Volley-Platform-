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
# Drill status (workflow)
# =========================
class DrillStatus(str, Enum):
    draft = "draft"         # създаден от coach
    pending = "pending"     # изпратен за одобрение
    approved = "approved"   # одобрен
    rejected = "rejected"   # отказан


# =========================
# Clubs
# =========================
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

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="club")
    drills = relationship("Drill", back_populates="club")


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

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    club = relationship("Club", back_populates="users")
    drills_created = relationship("Drill", back_populates="creator")


# =========================
# Drills (Упражнения)
# =========================
class Drill(Base):
    __tablename__ = "drills"

    id = Column(Integer, primary_key=True, index=True)

    # --- Основна информация ---
    name = Column(String(255), nullable=False)
    category = Column(String(255))
    level = Column(String(255))

    skill_focus = Column(Text)
    goal = Column(Text)
    description = Column(Text)
    variations = Column(Text)

    players = Column(Text)
    equipment = Column(Text)

    # --- Натоварване и време ---
    rpe = Column(String(50))
    duration_min = Column(Integer)
    duration_max = Column(Integer)

    # --- Медия ---
    image_urls = Column(Text)
    video_urls = Column(Text)

    # --- Генераторни / филтърни полета ---
    skill_domains = Column(Text)       # attack;block;defense
    game_phases = Column(Text)         # transition;break_point
    tactical_focus = Column(Text)
    technical_focus = Column(Text)
    position_focus = Column(Text)
    zone_focus = Column(Text)

    complexity_level = Column(Integer)
    decision_level = Column(Integer)

    age_min = Column(Integer)
    age_max = Column(Integer)

    intensity_type = Column(String(100))
    training_goal = Column(Text)
    type_of_drill = Column(String(100))

    # --- Workflow ---
    status = Column(
        SqlEnum(DrillStatus),
        nullable=False,
        default=DrillStatus.draft,
    )

    # --- Ownership ---
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    creator = relationship("User", back_populates="drills_created")
    club = relationship("Club", back_populates="drills")
