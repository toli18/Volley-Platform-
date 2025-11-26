from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app import models
from backend.app.schemas import (
    ForumCategorySchema,
    ForumTopicSchema,
    ForumTopicCreateSchema,
    ForumPostSchema,
    ForumPostCreateSchema,
)

router = APIRouter(prefix="/forum", tags=["forum"])


@router.get("/categories", response_model=List[ForumCategorySchema])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.ForumCategory).all()
    return categories


@router.get("/categories/{category_id}/topics", response_model=List[ForumTopicSchema])
def get_topics(category_id: int, db: Session = Depends(get_db)):
    topics = (
        db.query(models.ForumTopic)
        .filter(models.ForumTopic.category_id == category_id)
        .order_by(models.ForumTopic.created_at.desc())
        .all()
    )
    return topics


@router.post("/categories/{category_id}/topics", response_model=ForumTopicSchema)
def create_topic(category_id: int, topic_data: ForumTopicCreateSchema, db: Session = Depends(get_db)):
    category = db.query(models.ForumCategory).filter_by(id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    topic = models.ForumTopic(
        title=topic_data.title,
        content=topic_data.content,
        user_id=topic_data.user_id,
        category_id=category_id,
    )

    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


@router.get("/topics/{topic_id}/posts", response_model=List[ForumPostSchema])
def get_posts(topic_id: int, db: Session = Depends(get_db)):
    posts = (
        db.query(models.ForumPost)
        .filter(models.ForumPost.topic_id == topic_id)
        .order_by(models.ForumPost.created_at.asc())
        .all()
    )
    return posts


@router.post("/topics/{topic_id}/posts", response_model=ForumPostSchema)
def create_post(topic_id: int, post_data: ForumPostCreateSchema, db: Session = Depends(get_db)):
    topic = db.query(models.ForumTopic).filter_by(id=topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    post = models.ForumPost(
        content=post_data.content,
        user_id=post_data.user_id,
        topic_id=topic_id,
    )

    db.add(post)
    db.commit()
    db.refresh(post)
    return post
