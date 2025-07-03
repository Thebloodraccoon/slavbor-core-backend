from fastapi import APIRouter, Response, Request, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import (LoginRequest, LoginResponse, LoginResponseUnion,
                              TwoFAVerifyRequest)
from app.core.dependencies import AuthServiceDep
from app.auth.schemas import LoginRequest, LoginResponse,LogoutResponse
from app.auth.services import AuthService
from app.core.dependencies import AuthServiceDep, CurrentUserDep, get_current_user
from app.settings import settings

router = APIRouter()


@router.post("/login", response_model=LoginResponseUnion)
def login(request: LoginRequest, response: Response, auth_service: AuthServiceDep):
    return auth_service.login(request, response)


@router.post("/2fa/verify", response_model=LoginResponse)
def verify_2fa(
    request: TwoFAVerifyRequest, response: Response, auth_service: AuthServiceDep
):
    return auth_service.verify_2fa(request, response)


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    http_request: Request,
    response: Response,
    auth_service: AuthServiceDep,
    _: CurrentUserDep = Depends(get_current_user),
):

    jwt_token = http_request.headers.get("Authorization").replace("Bearer ", "")
    logout_response = await auth_service.logout_user(jwt_token)

    response.delete_cookie("refresh_token")

    return logout_response


@router.post("/refresh")
def refresh_tokens():
    return {"REFRESH_TOKENS": "TODO"}


@router.post("/register")
def register():
    return {"REGISTER": "TODO"}
