import enum
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
    JSON,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# ---------------------------------------
# USER ROLE ENUM
# ---------------------------------------
class UserRole(str, enum.Enum):
    platform_admin = "platform_admin"
    bfv_admin = "bfv_admin"
    coach = "coach"


# ---------------------------------------
# USERS
# ---------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    club = relationship("Club", back_populates="coaches")


# ---------------------------------------
# CLUBS
# ---------------------------------------
class Club(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    city = Column(String(255))

    # 🔥 Добавени липсващи полета
    address = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(255), nullable=True)
    website_url = Column(String(255), nullable=True)

    logo_url = Column(String(512), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    coaches = relationship("User", back_populates="club")
    trainings = relationship("Training", back_populates="club")


# ---------------------------------------
# EXERCISES
# ---------------------------------------
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    main_category = Column(String(255), nullable=False)
    sub_category = Column(String(255))
    level = Column(String(100))
    goal = Column(Text)
    description = Column(Text)
    players_required = Column(Integer)

    intensity = Column(String(100))
    duration_min = Column(Integer)
    duration_max = Column(Integer)

    tags = Column(JSON, default=list)
    age_groups = Column(JSON, default=list)
    image_urls = Column(JSON, default=list)
    video_urls = Column(JSON, default=list)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_by_admin = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


# ---------------------------------------
# TRAININGS
# ---------------------------------------
class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey("clubs.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(Text)
    age_group = Column(String(100))
    total_duration_min = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    club = relationship("Club", back_populates="trainings")
    exercises = relationship("TrainingExercise", back_populates="training")


# ---------------------------------------
# TRAINING EXERCISE LINK TABLE
# ---------------------------------------
class TrainingExercise(Base):
    __tablename__ = "training_exercises"
    __table_args__ = (
        UniqueConstraint(
            "training_id",
            "exercise_id",
            "order_index",
            name="uq_training_exercise",
        ),
    )

    training_id = Column(Integer, ForeignKey("trainings.id"), primary_key=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), primary_key=True)
    order_index = Column(Integer, primary_key=True)

    custom_duration_min = Column(Integer)
    notes = Column(Text)

    training = relationship("Training", back_populates="exercises")
    exercise = relationship("Exercise")


# ---------------------------------------
# EXERCISE SUGGESTION
# ---------------------------------------
class ExerciseSuggestion(Base):
    __tablename__ = "exercise_suggestions"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    main_category = Column(String(255))
    description = Column(Text)

    submitted_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)


# ---------------------------------------
# ARTICLES
# ---------------------------------------
class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    status = Column(String(50), default="published")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class ArticleSuggestion(Base):
    __tablename__ = "article_suggestions"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    submitted_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="pending")

    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)


# ---------------------------------------
# FORUM
# ---------------------------------------
class ForumCategory(Base):
    __tablename__ = "forum_categories"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ForumTopic(Base):
    __tablename__ = "forum_topics"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("forum_categories.id"), nullable=False)
    title = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class ForumPost(Base):
    __tablename__ = "forum_posts"

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("forum_topics.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
