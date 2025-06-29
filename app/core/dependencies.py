from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.auth.utils.token_utils import verify_token
from app.exceptions.auth_exceptions import (AdminAccessException,
                                            SuperAdminAccessException)
from app.races.services import RaceService
from app.settings import settings
from app.users.schemas import UserResponse
from app.users.services import UserService

DatabaseDep = Annotated[Session, Depends(settings.get_db)]


def get_user_service(db: DatabaseDep) -> UserService:
    """Get User service instance."""
    return UserService(db)


def get_race_service(db: DatabaseDep) -> RaceService:
    """Get Race service instance."""
    return RaceService(db)


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Session = Depends(settings.get_db),
) -> UserResponse:
    email = await verify_token(token, "access")
    return UserService(db).get_user_by_email(email)


def require_keeper_or_founder(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    if current_user.role not in ["keeper", "found_father"]:
        raise AdminAccessException()

    return current_user


def require_founder(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    if current_user.role != "found_father":
        raise SuperAdminAccessException()

    return current_user


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
RaceServiceDep = Annotated[RaceService, Depends(get_race_service)]

CurrentUserDep = Annotated[UserResponse, Depends(get_current_user)]
AdminUserDep = Annotated[UserResponse, Depends(require_keeper_or_founder)]
FounderUserDep = Annotated[UserResponse, Depends(require_founder)]
