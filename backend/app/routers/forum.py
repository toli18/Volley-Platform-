from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db_session, require_role, get_current_user
from app.models import ForumCategory, ForumTopic, ForumPost, UserRole

router = APIRouter(prefix="/forum", tags=["forum"])


@router.get("/categories", response_model=List[ForumCategory])
def list_categories(db: Session = Depends(get_db_session)):
    return db.query(ForumCategory).all()


@router.post(
    "/categories",
    response_model=ForumCategory,
    dependencies=[Depends(require_role(UserRole.platform_admin, UserRole.bfv_admin))],
)
def create_category(payload: dict, db: Session = Depends(get_db_session)):
    title = payload.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    category = ForumCategory(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/categories/{category_id}/topics", response_model=List[ForumTopic])
def list_topics(category_id: int, db: Session = Depends(get_db_session)):
    return db.query(ForumTopic).filter(ForumTopic.category_id == category_id).all()


@router.post(
    "/categories/{category_id}/topics",
    response_model=ForumTopic,
    dependencies=[Depends(require_role(UserRole.coach, UserRole.bfv_admin, UserRole.platform_admin))],
)
def create_topic(category_id: int, payload: dict, db: Session = Depends(get_db_session), user=Depends(get_current_user)):
    title = payload.get("title")
    if not title:
        raise HTTPException(status_code=400, detail="title is required")
    topic = ForumTopic(category_id=category_id, title=title, created_by=user.id)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


@router.get("/topics/{topic_id}", response_model=ForumTopic)
def get_topic(topic_id: int, db: Session = Depends(get_db_session)):
    topic = db.query(ForumTopic).filter(ForumTopic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.get("/topics/{topic_id}/posts", response_model=List[ForumPost])
def list_posts(topic_id: int, db: Session = Depends(get_db_session)):
    return db.query(ForumPost).filter(ForumPost.topic_id == topic_id).all()


@router.post(
    "/topics/{topic_id}/posts",
    response_model=ForumPost,
    dependencies=[Depends(require_role(UserRole.coach, UserRole.bfv_admin, UserRole.platform_admin))],
)
def create_post(topic_id: int, payload: dict, db: Session = Depends(get_db_session), user=Depends(get_current_user)):
    content = payload.get("content")
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
    post = ForumPost(topic_id=topic_id, content=content, created_by=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
