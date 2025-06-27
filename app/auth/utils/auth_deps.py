from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.auth.utils.token_utils import verify_token
from app.exceptions.auth_exceptions import (AdminAccessException,
                                            SuperAdminAccessException)
from app.settings import settings
from app.users.schemas import UserResponse
from app.users.services import UserService


async def verify_refresh_token(
    token_str: str,
) -> str:
    token = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token_str)
    return await verify_token(token, "refresh")


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Session = Depends(settings.get_db),
) -> UserResponse:
    email = await verify_token(token, "access")
    return UserService(db).get_user_by_email(email)


def require_keeper_or_founder(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    if current_user.role == "keeper" or current_user.role == "found_father":
        raise AdminAccessException()

    return current_user


def require_founder(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    if current_user.role != "found_father":
        raise SuperAdminAccessException()

    return current_user
