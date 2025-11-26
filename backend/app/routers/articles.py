from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.dependencies import get_db_session, require_role, get_current_user
from backend.app.models import Article, ArticleSuggestion, UserRole
from backend.app.schemas import ArticleCreate, ArticleRead

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=List[ArticleRead])
def list_articles(db: Session = Depends(get_db_session)):
    return db.query(Article).all()


@router.post("/", response_model=ArticleRead, dependencies=[Depends(require_role(UserRole.platform_admin, UserRole.bfv_admin))])
def create_article(payload: ArticleCreate, db: Session = Depends(get_db_session), user=Depends(get_current_user)):
    article = Article(title=payload.title, content=payload.content, created_by=user.id, status="published", approved_by=user.id)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.post("/suggestions", dependencies=[Depends(require_role(UserRole.coach, UserRole.bfv_admin, UserRole.platform_admin))])
def propose_article(payload: ArticleCreate, db: Session = Depends(get_db_session), user=Depends(get_current_user)):
    suggestion = ArticleSuggestion(title=payload.title, content=payload.content, submitted_by=user.id, status="pending")
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)
    return suggestion


@router.post("/suggestions/{suggestion_id}/approve", response_model=ArticleRead, dependencies=[Depends(require_role(UserRole.platform_admin, UserRole.bfv_admin))])
def approve_article(suggestion_id: int, db: Session = Depends(get_db_session), user=Depends(get_current_user)):
    suggestion = db.query(ArticleSuggestion).filter(ArticleSuggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    article = Article(
        title=suggestion.title,
        content=suggestion.content,
        created_by=suggestion.submitted_by,
        status="published",
        approved_by=user.id,
    )
    suggestion.status = "approved"
    db.add(article)
    db.commit()
    db.refresh(article)
    return article
