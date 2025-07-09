from fastapi import APIRouter, Request, Response, HTTPException, Depends

from app.auth.schemas import (LoginRequest, LoginResponse, LoginResponseUnion,
                              LogoutResponse, RefreshResponse,
                              TwoFAVerifyRequest)
from app.core.dependencies import AuthServiceDep, CurrentUserDep

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.auth.schemas import RegisterRequest, RegisterResponse
from app.users.services import UserService
from app.settings.local import get_db
from app.auth.utils.token_utils import create_access_token

router = APIRouter()



@router.post("/registration", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    service = UserService(db)

    # Создать нового юзера с полной бизнес-логикой
    user = service.create_user(request)

    # Сгенерировать токен
    access_token = create_access_token({"sub": str(user.id)})

    # Поставить httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=True
    )

    return RegisterResponse(access_token=access_token)