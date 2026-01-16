from fastapi import APIRouter, Depends

from backend.src.db.database import get_db
from sqlalchemy.orm import Session
from backend.src.db import db_article
from backend.src.schemas.article_schema import ArticleDisplay
router = APIRouter()

@router.get("/")
def article_root():
    """
    Root endpoint for article.
    """
    return {"message": "Welcome to the article root!"}

@router.get("/{id}",response_model=ArticleDisplay)
def get_article_by_id(id: int, db: Session = Depends(get_db)):
    """
    Endpoint to get a specific article by ID.
    """
    return db_article.get_article_by_id(db, article_id=id)
