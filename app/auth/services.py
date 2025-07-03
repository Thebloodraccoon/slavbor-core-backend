from fastapi import Depends, Response
from sqlalchemy.orm import Session

from app.auth.schemas import LoginRequest, LoginResponse
from app.auth.utils.pwd_utils import verify_password
from app.auth.utils.token_utils import (create_access_token,
                                        create_refresh_token)
from app.exceptions.auth_exceptions import InvalidCredentialsException
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
