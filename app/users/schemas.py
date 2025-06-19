#import re
from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr, constr, field_validator

#from app.constants import USER_ROLES
#from app.exceptions import InvalidEmailException

UserRole = Literal["found_father", "keeper", "player"]

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = None


class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_]+$")] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    #model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        orm_mode = True  # ← позволяет возвращать SQLAlchemy‑объекты
        from_attributes = True
