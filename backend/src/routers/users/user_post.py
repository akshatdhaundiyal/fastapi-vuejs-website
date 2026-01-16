from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.src.db.database import get_db
from backend.src.schemas.user_schema import UserBase, UserDisplay, UserUpdate
from backend.src.db import db_user
from backend.src.utils.auth_service.oauth2_util import get_current_user


router = APIRouter()

@router.post("/create", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    """
    Endpoint to create a new user.
    """
    # Logic to create a user would go here
    return db_user.create_user(db, request=request)

@router.post('/update',response_model=UserDisplay)
def update_user(request: UserUpdate, db: Session = Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    """
    Endpoint to update user details.
    """
    # Logic to update user details would go here
    check_request_id = db_user.get_user_by_username(db, username=request.backup_username)
    if not check_request_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if current_user.id != check_request_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own details.")
    request.id = check_request_id.id
    return db_user.update_user_details(db, request=request)