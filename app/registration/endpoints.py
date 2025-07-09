from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.registration.schemas import RegistrationRequest, RegistrationResponse
from app.settings.local import get_db
from app.users.services import UserService

router = APIRouter()


@router.post("/registration", response_model=RegistrationRequest, status_code=status.HTTP_201_CREATED)
def register(request: RegistrationRequest, response: RegistrationResponse, db: Session = Depends(get_db)):
    service = UserService(db)

    # Создать нового юзера с полной бизнес-логикой
    user = service.create_user(request)
