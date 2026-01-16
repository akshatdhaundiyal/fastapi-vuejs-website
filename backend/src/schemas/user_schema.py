from operator import ge
from typing import Optional
from pydantic import BaseModel

from backend.src.utils.pydantic.generate_partial_model import generate_partial_model

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    fullname: Optional[str] = None
    bio: Optional[str] = None
    # profile_picture: Optional(str) = None
    
    class ConfigDict:
        from_attributes = True


class UserUpdate(generate_partial_model(UserBase, model_name="UserUpdate")):
    backup_username: str
    id: Optional[int] = None
    pass

class UserDisplay(BaseModel):
    username: str
    email: str
    fullname: Optional[str] = None
    bio: Optional[str] = None
    # profile_picture: Optional(str) = None
    
    class ConfigDict:
        from_attributes = True