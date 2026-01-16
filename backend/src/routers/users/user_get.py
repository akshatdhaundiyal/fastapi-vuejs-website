from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.user_schema import UserDisplay
from src.db import db_user

router = APIRouter()

@router.get("/")
def users_root():
    """
    Root endpoint for users.
    """
    return {"message": "Welcome to the users root!"}

@router.get("/{id}",response_model=UserDisplay)
def get_user_by_id(id: int,db: Session = Depends(get_db)):
    """
    Endpoint to get a specific user by ID.
    """
    return db_user.get_user_by_id(id=id)