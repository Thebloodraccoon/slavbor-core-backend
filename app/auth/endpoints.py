from fastapi import APIRouter, Request, Response

from app.auth.schemas import (LoginRequest, LoginResponse, LoginResponseUnion,
                              LogoutResponse, RefreshResponse,
                              TwoFAVerifyRequest)
from app.core.dependencies import AuthServiceDep, CurrentUserDep

from fastapi import APIRouter, HTTPException, status, Depends, Response
from app.auth.schemas import RegisterRequest, RegisterResponse
from app.auth.utils import hash_password, create_jwt_token
from app.users.repository import UserRepo

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
    _: CurrentUserDep,
):
    access_token = (http_request.headers.get("Authorization") or "").replace(
        "Bearer ", ""
    )
    refresh_token = http_request.cookies.get("refresh_token", "")
    logout_response = await auth_service.logout_user(access_token, refresh_token)

    response.delete_cookie(
        key="refresh_token", httponly=True, samesite="none", secure=True
    )

    return logout_response


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_tokens(http_request: Request, auth_service: AuthServiceDep):
    refresh_token = http_request.cookies.get("refresh_token", "")
    return await auth_service.refresh_tokens(refresh_token)


@router.post("/auth/register", response_model=RegisterResponse, status_code=201)
async def register(
    request: RegisterRequest,
    response: Response,
    user_repo: UserRepo = Depends(),
):
    # 1. Проверка email
    if await user_repo.get_by_email(request.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    # 2. Проверка username
    if await user_repo.get_by_username(request.username):
        raise HTTPException(status_code=409, detail="Username already taken")

    # 3. Хэш пароля
    hashed_pw = hash_password(request.password)

    # 4. Создание юзера
    user = await user_repo.create_user(
        username=request.username.strip(),
        email=request.email.strip(),
        password_hash=hashed_pw
    )

    # 5. Генерация JWT
    access_token = create_jwt_token(user_id=user.id)

    # 6. Ставим httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=True
    )

    return RegisterResponse(access_token=access_token)