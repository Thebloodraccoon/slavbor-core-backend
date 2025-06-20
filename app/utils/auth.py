from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.exceptions.token_exceptions import InvalidJWTException
from app.settings.base import JWT_ALGORITHM, JWT_SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt


# 15 minutes lifetime
def create_access_token(sub: str, user_email: str):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    access_token = {"exp": expire, "sub": sub, "user_email": user_email}
    return create_token(access_token)


# 30 days lifetime
def create_refresh_token(sub: str, user_email: str):
    expire = datetime.now(tz=timezone.utc) + timedelta(days=30)
    refresh_token = {"exp": expire, "sub": sub, "user_email": user_email}
    return create_token(refresh_token)


# validate token
def verify_token(token):
    try:
        decode_token(token)
    except JWTError:
        raise InvalidJWTException


# get payload
def decode_token(token):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    return payload
