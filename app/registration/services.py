from fastapi import Response
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
                                        get_token_expiration,
                                        verify_refresh_token)
from app.auth.utils.twofa_utils import (generate_otp_secret, generate_otp_uri,
                                        verify_otp_code)
from app.exceptions.auth_exceptions import (InvalidCodeException,
                                            InvalidCredentialsException)
from app.settings import settings
from app.users.repository import UserRepository


class RegistrationService:
    ...
