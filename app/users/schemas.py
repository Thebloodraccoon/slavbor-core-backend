from pydantic import BaseModel, EmailStr, constr
from typing import Literal, Optional
from app.constants import USER_ROLES


# ── Базовая часть, которую наследуем ─────────────────────────────────────────
class _UserBase(BaseModel):
    username: Username
    email: EmailStr


# ── Схемы I/O ────────────────────────────────────────────────────────────────
class UserCreate(_UserBase):
    password: str
    role: Optional[Literal[USER_ROLES]] = None


class UserUpdate(BaseModel):
    username: Username | None = None
    email: EmailStr | None = None


class UserResponse(_UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True  # ← позволяет возвращать SQLAlchemy‑объекты
