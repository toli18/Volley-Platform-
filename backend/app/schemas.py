from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from backend.app.models import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None


class TokenPayload(BaseModel):
    sub: str
    exp: int


class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: UserRole
    club_id: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ExerciseBase(BaseModel):
    name: str
    main_category: str
    sub_category: Optional[str] = None
    level: Optional[str] = None
    goal: Optional[str] = None
    description: Optional[str] = None
    players_required: Optional[int] = None
    intensity: Optional[str] = None
    duration_min: Optional[int] = None
    duration_max: Optional[int] = None
    tags: List[str] = []
    age_groups: List[str] = []
    image_urls: List[str] = []
    video_urls: List[str] = []


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseRead(ExerciseBase):
    id: int
    created_by: Optional[int] = None
    approved_by_admin: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True


class ExerciseSuggestionCreate(BaseModel):
    name: str
    main_category: Optional[str] = None
    description: Optional[str] = None


class ExerciseSuggestionRead(BaseModel):
    id: int
    name: str
    status: str
    submitted_by: int
    created_at: datetime

    class Config:
        orm_mode = True


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreate(ArticleBase):
    pass


class ArticleRead(ArticleBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class TrainingExerciseCreate(BaseModel):
    exercise_id: int
    order_index: int
    custom_duration_min: Optional[int] = None
    notes: Optional[str] = None


class TrainingCreate(BaseModel):
    club_id: int
    name: str
    description: Optional[str] = None
    age_group: Optional[str] = None
    total_duration_min: Optional[int] = None
    exercises: List[TrainingExerciseCreate] = []


class TrainingRead(BaseModel):
    id: int
    club_id: int
    name: str
    description: Optional[str]
    age_group: Optional[str]
    total_duration_min: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
