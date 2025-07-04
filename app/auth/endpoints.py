from datetime import datetime, timedelta

from fastapi import APIRouter, Request, Response

from app.auth.schemas import (LoginRequest, LoginResponse, LoginResponseUnion,
                              LogoutResponse, RefreshResponse,
                              TwoFAVerifyRequest)
from app.auth.utils.token_utils import (add_token_to_blacklist,
                                        create_access_token, decode_token)
from app.core.dependencies import AuthServiceDep, CurrentUserDep
from app.exceptions.token_exceptions import (InvalidTokenException,
                                             TokenBlacklistedException)

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
def refresh_tokens(http_request: Request):
    refresh_token = http_request.cookies.get("refresh_token", "")

    if not refresh_token:
        raise InvalidTokenException

    payload = decode_token(refresh_token)
    token_exp_timestamp = payload.get("exp")

    if token_exp_timestamp is not None:
        token_exp: datetime = datetime.fromtimestamp(token_exp_timestamp)
    else:
        token_exp = datetime.now() + timedelta(days=30)

    if add_token_to_blacklist(refresh_token, token_exp):
        raise TokenBlacklistedException

    user_id = payload.get("sub")

    if not user_id:
        raise InvalidTokenException

    new_access_token = create_access_token(data={"sub": user_id})

    return new_access_token


@router.post("/register")
def register():
    return {"REGISTER": "TODO"}
