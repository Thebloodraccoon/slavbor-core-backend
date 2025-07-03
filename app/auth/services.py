from fastapi import Depends, Response
from jose import jwt
from sqlalchemy.orm import Session

from datetime import datetime, timezone

from app.auth.schemas import LoginRequest, LoginResponse
from app.auth.utils.pwd_utils import verify_password
from app.auth.utils.token_utils import (create_access_token,
                                        create_refresh_token, add_token_to_blacklist)
from app.exceptions.auth_exceptions import InvalidCredentialsException
from app.exceptions.token_exceptions import InvalidTokenException
from app.settings import settings
from app.users.repository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def login(self, request: LoginRequest, response: Response) -> LoginResponse:
        user = self.repository.get_by_email(request.email)

        if not user or not verify_password(request.password, user.hashed_password):
            raise InvalidCredentialsException()

        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="none",
            secure=True,
            max_age=30 * 24 * 60 * 60,
        )

        return LoginResponse(access_token=access_token)

    async def logout_user(token: str):
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        exp_timestamp = payload.get("exp")

        if not exp_timestamp:
            raise InvalidTokenException

        expire_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        await add_token_to_blacklist(token, expire_time)

        return {"success": True, "message": "Successfully logged out"}
