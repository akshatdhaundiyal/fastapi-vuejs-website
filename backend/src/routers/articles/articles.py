from fastapi import APIRouter, Depends

from src.db.database import get_db
from src.routers.articles import article_get, article_post

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    dependencies=[Depends(get_db)]
)

router.include_router(article_get.router)
router.include_router(article_post.router)