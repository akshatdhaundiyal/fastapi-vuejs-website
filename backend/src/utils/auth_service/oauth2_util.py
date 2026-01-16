from fastapi import Depends, HTTPException,status
from sqlalchemy.orm import Session
from backend.src.db.database import get_db
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import datetime
from jose import jwt

from backend.src.db.models import DbUser

from backend.src.config import settings
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
 
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
  else:
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    """Retrieve the current user from the token."""
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      user_id: int = int(payload.get("sub"))
      if user_id is None:
          raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
                   detail="Couldnt validate cretentials due to missing user ID",
                           headers={"WWW-Authenticate": "Bearer"}
                                   )
    except jwt.JWTError:
      # raise jwt.JWTError
      raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
                   detail="Couldnt validate cretentials because of JWT decode error",
                           headers={"WWW-Authenticate": "Bearer"}
                                   )
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if user is None:
        raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
                   detail="Couldnt validate cretentials due to user not found"
                                   )
    return user