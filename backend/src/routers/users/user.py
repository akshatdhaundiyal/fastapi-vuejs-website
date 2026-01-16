from fastapi import APIRouter, Depends

from src.db.database import get_db
from src.routers.users import user_get, user_post

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_db)]
)

router.include_router(user_get.router)
router.include_router(user_post.router)