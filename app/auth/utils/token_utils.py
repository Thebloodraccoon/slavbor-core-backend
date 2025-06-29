from datetime import datetime, timedelta, timezone

from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from app.exceptions.token_exceptions import (InvalidTokenException,
                                             TokenBlacklistedException)
from app.settings import settings


def create_token(data: dict, token_type: str, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode.update({"token_type": token_type})
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(data: dict):
    return create_token(data, "access", timedelta(minutes=30))


def create_refresh_token(data: dict):
    return create_token(data, "refresh", timedelta(days=30))


async def add_token_to_blacklist(token: str, expire_time: datetime):
    async with settings.get_redis() as redis:
        token_ttl = int((expire_time - datetime.now(timezone.utc)).total_seconds())
        if token_ttl > 0:
            await redis.setex(f"blacklist:{token}", token_ttl, "blacklist_token")
            return True

        return False


async def is_token_blacklisted(token: str):
    async with settings.get_redis() as redis:
        return await redis.exists(f"blacklist:{token}")


def decode_token(token: HTTPAuthorizationCredentials):
    return jwt.decode(
        token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )


async def verify_token(
    token: HTTPAuthorizationCredentials, required_token_type: str
) -> str:
    if await is_token_blacklisted(token.credentials):
        raise TokenBlacklistedException()

    payload = decode_token(token)
    email: str = payload.get("sub")
    token_type: str = payload.get("token_type")

    if email is None:
        raise InvalidTokenException()

    if token_type != required_token_type:
        raise InvalidTokenException()

    return email


async def verify_refresh_token(
    token_str: str,
) -> str:
    token = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token_str)
    return await verify_token(token, "refresh")
