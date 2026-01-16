from typing import List
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.src.db.database import Base
import datetime

def utc_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)

class DbUser(Base):
    """
    DbUser model for the database. This model represents users in the social media application.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    fullname = Column(String,default=None)
    bio = Column(String,default=None)
    # profile_picture = Column(String,default=None)
    registration_date = Column(DateTime
                               , server_default=func.now()
                               )
    last_login = Column(DateTime
                        , server_default=func.now()
                        )
    articles = relationship("DbArticle", back_populates="user")

class DbArticle(Base):
    """
    DbArticle model for the database. This  model represents articles
    written by users in the social media application.
    """
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(Integer,
                       ForeignKey(
                           "users.id",
                           ondelete="CASCADE"
                       ),nullable=False)  # Foreign key to DbUser
    created_at = Column(DateTime
                        , server_default=func.now()
                        )
    updated_at = Column(DateTime
                        , server_default=func.now()
                        )
    tags= Column(String)  # Comma-separated tags
    is_published = Column(Boolean, default=True)
    image_url = Column(String, default=None)
    category = Column(String, default=None)
    user = relationship("DbUser", back_populates="articles")

class DbVote(Base):
    """
    DbVote model for the database. This model represents votes (likes/dislikes) on articles.
    """
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,
                     ForeignKey(
                           "users.id",
                           ondelete="CASCADE"
                       ),nullable=False)  # Foreign key to DbUser
    article_id = Column(Integer,
                        ForeignKey(
                           "articles.id",
                           ondelete="CASCADE"
                       ),nullable=False)  # Foreign key to DbArticle
    vote_type = Column(String)  # 'like/dislike' or 'rating'
    vote_value = Column(String)  # 'like' or 'dislike' or rating value
    voted_at = Column(DateTime
                        , server_default=func.now()
                        )