from app.users.schemas import UserCreate


class RegistrationRequest(UserCreate):
    pass


class RegistrationResponse:
    access_token: str
