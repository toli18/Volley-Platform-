from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from backend.app.models import UserRole


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None


class TokenPayloadSchema(BaseModel):
    sub: str
    exp: int


class UserBaseSchema(BaseModel):
    email: EmailStr
    name: str
    role: UserRole
    club_id: Optional[int] = None


class UserCreateSchema(UserBaseSchema):
    password: str


class UserReadSchema(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class ClubSchema(BaseModel):
    id: int
    name: str
    city: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ExerciseBaseSchema(BaseModel):
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
    tags: List[str] = Field(default_factory=list)
    age_groups: List[str] = Field(default_factory=list)
    image_urls: List[str] = Field(default_factory=list)
    video_urls: List[str] = Field(default_factory=list)


class ExerciseCreateSchema(ExerciseBaseSchema):
    pass


class ExerciseReadSchema(ExerciseBaseSchema):
    id: int
    created_by: Optional[int] = None
    approved_by_admin: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ExerciseSuggestionCreateSchema(BaseModel):
    name: str
    main_category: Optional[str] = None
    description: Optional[str] = None


class ExerciseSuggestionReadSchema(BaseModel):
    id: int
    name: str
    status: str
    submitted_by: int
    created_at: datetime
    reviewed_by: Optional[int] = None

    model_config = {"from_attributes": True}


class ArticleBaseSchema(BaseModel):
    title: str
    content: str


class ArticleCreateSchema(ArticleBaseSchema):
    pass


class ArticleReadSchema(ArticleBaseSchema):
    id: int
    status: str
    created_at: datetime
    created_by: int
    approved_by: Optional[int] = None

    model_config = {"from_attributes": True}


class ArticleSuggestionSchema(BaseModel):
    id: int
    title: str
    content: str
    submitted_by: int
    status: str
    created_at: datetime
    reviewed_by: Optional[int] = None

    model_config = {"from_attributes": True}


class TrainingExerciseCreateSchema(BaseModel):
    exercise_id: int
    order_index: int
    custom_duration_min: Optional[int] = None
    notes: Optional[str] = None


class TrainingExerciseSchema(TrainingExerciseCreateSchema):
    training_id: int

    model_config = {"from_attributes": True}


class TrainingCreateSchema(BaseModel):
    club_id: int
    name: str
    description: Optional[str] = None
    age_group: Optional[str] = None
    total_duration_min: Optional[int] = None
    exercises: List[TrainingExerciseCreateSchema] = Field(default_factory=list)


class TrainingReadSchema(BaseModel):
    id: int
    club_id: int
    created_by: int
    name: str
    description: Optional[str]
    age_group: Optional[str]
    total_duration_min: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}


class ForumPostSchema(BaseModel):
    id: int
    topic_id: int
    content: str
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ForumTopicSchema(BaseModel):
    id: int
    category_id: int
    title: str
    created_by: int
    created_at: datetime
    posts: list[ForumPostSchema] | None = None

    model_config = ConfigDict(from_attributes=True)


class ForumCategorySchema(BaseModel):
    id: int
    title: str
    created_at: datetime
    topics: list[ForumTopicSchema] | None = None

    model_config = ConfigDict(from_attributes=True)
