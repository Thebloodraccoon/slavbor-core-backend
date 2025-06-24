import re
from datetime import datetime
from typing import Literal, Optional

from pydantic import (BaseModel, ConfigDict, constr, field_validator,
                      model_validator)

from app.exceptions.user_exceptions import (InvalidEmailException,
                                            InvalidPasswordException)


class UserBase(BaseModel):
    username: str
    role: Literal["found_father", "keeper", "player"] = None  # type: ignore
    email: str

    @field_validator("email")
    def validate_email(cls, email):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise InvalidEmailException()
        return email

    @field_validator("username")
    def validate_username(cls, username):
        if len(username) < 3 or len(username) > 32:
            raise ValueError("Username must be between 3 and 32 characters long")
        return username


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise InvalidPasswordException(
                "Password must be at least 8 characters long"
            )
        return password


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Literal["found_father", "keeper", "player"]] = None

    @field_validator("email")
    def validate_email(cls, email):
        if email is not None and not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email
        ):
            raise InvalidEmailException()
        return email

    @model_validator(mode="before")
    def validate_data(cls, values):
        if not any(key for key in values if key != "id" and values[key] is not None):
            raise ValueError("At least one updatable field must be provided.")
        return values


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
