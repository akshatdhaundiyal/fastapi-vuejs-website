import datetime
from sqlalchemy.orm import Session
from backend.src.db.models import DbUser
from backend.src.schemas.user_schema import UserBase, UserUpdate
from backend.src.utils.auth_service.hash import Hash
from fastapi import HTTPException, status


def create_user(db: Session, request: UserBase):
    """
    Create a new user in the database.
    """
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
        fullname=request.fullname,
        bio=request.bio,
        registration_date= datetime.datetime.now(tz=datetime.timezone.utc),
        last_login=datetime.datetime.now(tz=datetime.timezone.utc)
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_details(db: Session, request: UserUpdate):
    """
    Update user details in the database.
    """
    updated_user = db.query(DbUser).filter(DbUser.id == request.id).first()
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
    for field, value in request.model_dump().items():
        if value is None:
            continue
        if field == "password":
            value = Hash.bcrypt(value)
        if field == "username":
            existing_user = db.query(DbUser).filter(DbUser.username == value).first()
            if existing_user and existing_user.id != request.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
        setattr(updated_user, field, value)
    db.commit()
    db.refresh(updated_user)
    return updated_user

def get_user_by_id(db: Session, user_id: int):
    """
    Retrieve a user by their ID.
    """
    return db.query(DbUser).filter(DbUser.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user by their ID.
    """
    return db.query(DbUser).filter(DbUser.username == username).first()

def update_last_login(db: Session, user_id: int):
    """
    Update the last login time for a user.
    """
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if user:
        user.last_login = datetime.datetime.now(tz=datetime.timezone.utc)
        db.commit()
        db.refresh(user)
    return user