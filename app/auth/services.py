from datetime import datetime, timedelta, timezone

from fastapi import Request, Response
from sqlalchemy.orm import Session

from app.auth.schemas import (LoginRequest, LoginResponse, LoginResponseUnion,
                              LogoutResponse, RefreshResponse,
                              TwoFARequiredResponse, TwoFASetupResponse,
                              TwoFAVerifyRequest)
from app.auth.utils.pwd_utils import verify_password
from app.auth.utils.token_utils import (add_token_to_blacklist,
                                        create_access_token,
                                        create_refresh_token,
                                        create_temp_token, decode_temp_token,
                                        decode_token, verify_refresh_token)
from app.auth.utils.twofa_utils import (generate_otp_secret, generate_otp_uri,
                                        verify_otp_code)
from app.exceptions.auth_exceptions import (InvalidCodeException,
                                            InvalidCredentialsException)
from app.exceptions.token_exceptions import (InvalidTokenException,
                                             TokenBlacklistedException)
from app.settings import settings
from app.users.repository import UserRepository


def create_login_response(user, response: Response) -> LoginResponse:
    """Create login response with tokens and cookies."""
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


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def login(self, request: LoginRequest, response: Response) -> LoginResponseUnion:
        """Handle login with 2FA support."""
        user = self.user_repo.get_by_email(request.email)

        if not user or not verify_password(request.password, user.hashed_password):
            raise InvalidCredentialsException()

        if user.email == settings.ADMIN_LOGIN:
            updated_user = self.user_repo.update_last_login(user)
            return create_login_response(updated_user, response)

        if not user.is_2fa_enabled:
            if not user.otp_secret:
                otp_secret = generate_otp_secret()
                user = self.user_repo.setup_2fa(user, otp_secret)

            return TwoFASetupResponse(
                otp_uri=generate_otp_uri(str(user.email), str(user.otp_secret)),
                temp_token=create_temp_token(int(user.id)),
            )

        return TwoFARequiredResponse(temp_token=create_temp_token(int(user.id)))

    def verify_2fa(
        self, request: TwoFAVerifyRequest, response: Response
    ) -> LoginResponse:
        """Verify 2FA code and complete login."""
        user_id = decode_temp_token(request.temp_token)
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise InvalidCredentialsException()

        if not verify_otp_code(str(user.otp_secret), request.otp_code):
            raise InvalidCodeException()

        if not user.is_2fa_enabled:
            updated_user = self.user_repo.complete_2fa_setup(user)
        else:
            updated_user = self.user_repo.update_last_login(user)
        return create_login_response(updated_user, response)

    async def refresh_tokens(self, http_request: Request) -> RefreshResponse:
        refresh_token = http_request.cookies.get("refresh_token", "")

        if not refresh_token:
            raise InvalidTokenException

        email = await verify_refresh_token(refresh_token)

        if not email:
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

    async def logout_user(
        self, access_token: str, refresh_token: str
    ) -> LogoutResponse:
        payload = decode_token(access_token)
        exp = payload.get("exp")
        if exp is None:
            raise ValueError("Token payload missing 'exp' field")

        blacklist_access = await add_token_to_blacklist(
            access_token, datetime.fromtimestamp(float(exp), tz=timezone.utc)
        )
        if refresh_token:
            await add_token_to_blacklist(
                refresh_token, datetime.fromtimestamp(exp, tz=timezone.utc)
            )

        if blacklist_access:
            return LogoutResponse(detail="Successful logout")

        return LogoutResponse(detail="Token is already expired")
