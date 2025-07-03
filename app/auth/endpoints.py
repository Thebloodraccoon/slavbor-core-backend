from fastapi import APIRouter, Response

from app.auth.schemas import (
    LoginRequest, LoginResponse, TwoFAVerifyRequest, LoginResponseUnion
)
from app.core.dependencies import AuthServiceDep

router = APIRouter()


@router.post("/login", response_model=LoginResponseUnion)
def login(request: LoginRequest, response: Response, auth_service: AuthServiceDep):
    return auth_service.login(request, response)


@router.post("/2fa/verify", response_model=LoginResponse)
def verify_2fa(request: TwoFAVerifyRequest, response: Response, auth_service: AuthServiceDep):
    return auth_service.verify_2fa(request, response)


@router.post("/logout")
def logout():
    return {"LOGOUT": "TODO"}


@router.post("/refresh")
def refresh_tokens():
    return {"REFRESH_TOKENS": "TODO"}


@router.post("/register")
def register():
    return {"REGISTER": "TODO"}
