import re
from typing import Union

from pydantic import BaseModel, field_validator, constr

from app.exceptions.user_exceptions import InvalidEmailException


class LoginRequest(BaseModel):
    username: constr(min_length=3, max_length=32)
    email: str
    password: constr(min_length=8)

    @field_validator("email")
    def validate_email(cls, email):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise InvalidEmailException()
        return email


class RegisterResponse(BaseModel):
    access_token: str


class LoginResponse(BaseModel):
    access_token: str


class TwoFASetupResponse(BaseModel):
    otp_uri: str
    temp_token: str


class TwoFARequiredResponse(BaseModel):
    temp_token: str


class TwoFAVerifyRequest(BaseModel):
    otp_code: str
    temp_token: str


class LogoutResponse(BaseModel):
    detail: str


class RefreshResponse(BaseModel):
    access_token: str


LoginResponseUnion = Union[LoginResponse, TwoFASetupResponse, TwoFARequiredResponse]
