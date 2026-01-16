import datetime
from pydantic import BaseModel
from typing import List, Optional

class ArticleBase(BaseModel):
    title: str
    content: str
    author_id: Optional[int]
    created_at: datetime.datetime
    tags: str | None = None
    is_published: bool = True
    image_url: str | None = None
    category: str | None = None

    class ConfigDict():
        from_attributes = True


class ArticleDisplay(ArticleBase):
    updated_at: datetime.datetime | None = None
    likes: int = 0
    comments_count: int = 0
    views: int = 0

    class ConfigDict():
        from_attributes = True

class ArticleEditDisplay(ArticleBase):
    id: int

    class ConfigDict():
        from_attributes = True

class VoteBase(BaseModel):
    article_id: int
    user_id: int
    vote_type: str  # 'like/dislike' or 'rating'
    vote_value: str  # 'like' or 'dislike' or rating value
    voted_at: datetime.datetime

    class ConfigDict():
        from_attributes = True