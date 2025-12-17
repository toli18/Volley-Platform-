from typing import Optional
from enum import Enum
from pydantic import BaseModel


# ===== Drill status (READ-ONLY for coach) =====
class DrillStatus(str, Enum):
    draft = "draft"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


# ===== Base =====
class DrillBase(BaseModel):
    name: str
    category: Optional[str] = None
    level: Optional[str] = None

    skill_focus: Optional[str] = None
    goal: Optional[str] = None
    description: Optional[str] = None
    variations: Optional[str] = None

    players: Optional[str] = None
    equipment: Optional[str] = None

    rpe: Optional[str] = None
    duration_min: Optional[int] = None
    duration_max: Optional[int] = None

    image_urls: Optional[str] = None
    video_urls: Optional[str] = None

    skill_domains: Optional[str] = None
    game_phases: Optional[str] = None
    tactical_focus: Optional[str] = None
    technical_focus: Optional[str] = None
    position_focus: Optional[str] = None
    zone_focus: Optional[str] = None

    complexity_level: Optional[int] = None
    decision_level: Optional[int] = None

    age_min: Optional[int] = None
    age_max: Optional[int] = None

    intensity_type: Optional[str] = None
    training_goal: Optional[str] = None
    type_of_drill: Optional[str] = None


# ===== Create (coach НЕ подава status) =====
class DrillCreate(DrillBase):
    pass


# ===== Read (status се вижда) =====
class DrillRead(DrillBase):
    id: int
    status: DrillStatus

    class Config:
        from_attributes = True
