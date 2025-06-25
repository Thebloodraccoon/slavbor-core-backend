from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.exceptions.token_exceptions import InvalidJWTException
from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def create_access_token(sub: str, user_email: str):
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    access_token = {"exp": expire, "sub": sub, "user_email": user_email}
    return create_token(access_token)


def create_refresh_token(sub: str, user_email: str):
    expire = datetime.now(tz=timezone.utc) + timedelta(days=30)
    refresh_token = {"exp": expire, "sub": sub, "user_email": user_email}
    return create_token(refresh_token)


def verify_token(token):
    try:
        decode_token(token)
    except JWTError:
        raise InvalidJWTException


def decode_token(token):
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    return payload


async def add_token_to_blacklist(token, expiry):
    async with settings.get_redis() as redis:
        current_time = datetime.now(tz=timezone.utc)
        token_ttl = (expiry - current_time).total_seconds()

        if token_ttl > 0:
            await redis.setex(f"blacklist: {token}", token_ttl, "blacklist_token")
            return True
        else:
            return False


async def is_token_blacklisted(token):
    async with settings.get_redis() as redis:
        return await redis.exists(f"blacklist: {token}")
