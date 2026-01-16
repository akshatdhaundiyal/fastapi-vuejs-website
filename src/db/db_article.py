import datetime
from sqlalchemy.orm import Session

from src.db.models import DbArticle, DbVote
from src.schemas.article_schema import ArticleBase, VoteBase

def create_article(db: Session,request: ArticleBase):
    """
    Create a new article in the database.
    """
    tags_str = '|'.join([request.tags]) if request.tags is not None else request.tags
    new_article = DbArticle(
        title=request.title,
        content=request.content,
        author_id=request.author_id,
        created_at=datetime.datetime.now(tz=datetime.timezone.utc),
        tags= tags_str,
        is_published=request.is_published,
        image_url=request.image_url,
        category=request.category
        )
    
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def get_article_by_id(db: Session, article_id: int):
    """
    Retrieve an article by its ID.
    """
    return db.query(DbArticle).filter(DbArticle.id == article_id).first()


def edit_article(db:Session, request: ArticleBase, current_user: int):
    """
    Edit an existing article in the database.
    """
    if request.author_id != current_user:
        return None  # Or raise an exception for unauthorized access
    
    article = get_article_by_id(db, request.id)
    if not article:
        return None
    
    article.title = request.title
    article.content = request.content
    article.tags = '|'.join([request.tags]) if request.tags is not None else request.tags
    article.is_published = request.is_published
    article.image_url = request.image_url
    article.category = request.category
    article.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)

    db.commit()
    db.refresh(article)
    return article

def vote_article(db: Session, request: VoteBase):
    """
    Function to handle voting for an article.
    """
    ## Check if the article exists
    article = get_article_by_id(db, request.article_id)
    if not article:
        return {"error": "Article not found"}
    
    ## Check if the user has already voted on this article
    existing_vote = db.query(DbVote).filter(
        DbVote.article_id == request.article_id,
        DbVote.user_id == request.user_id
    ).first()

    if existing_vote:
        existing_vote.vote_type = request.vote_type
        existing_vote.vote_value = request.vote_value
        existing_vote.voted_at = datetime.datetime.now(tz=datetime.timezone.utc)
        db.commit()
        db.refresh(existing_vote)
    else:
        # Here you would implement the logic to record the vote.
        # This is a placeholder implementation.
        commit_vote = DbVote(
            article_id=request.article_id,
            user_id=request.user_id,
            voted_at=datetime.datetime.now(tz=datetime.timezone.utc),
            vote_type=request.vote_type,
            vote_value=request.vote_value
        )
        db.add(commit_vote)
        db.commit()
        db.refresh(commit_vote)
    if existing_vote:
        return existing_vote
    else:
        return commit_vote