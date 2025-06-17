from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.users.schemas import UserCreate, UserUpdate
from app.utils.auth import get_password_hash


class UserService:
    """Бизнес‑логика для сущности `User`."""

    def __init__(self, db: Session):
        self.db = db

    # ─────────── helpers ──────────────────────────────────────────────────────
    def _unique_or_raise(
        self, *, username: str | None, email: str | None, skip_id: int | None = None
    ):
        """Проверяем уникальность username/email"""
        stmt = select(
            exists().where((User.username == username) | (User.email == email))
        )
        if skip_id:
            stmt = stmt.where(User.id != skip_id)
        if self.db.scalar(stmt):
            raise HTTPExeption("username or email already taken")

    # ─────────── CRUD ────────────────────────────────────────────────────────
    def create_user(self, data: UserCreate) -> User:
        self._unique_or_raise(username=data.username, email=data.email)

        db_user = User(
            username=data.username,
            email=data.email,
            hashed_password=get_password_hash(data.password),
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_all_users(self, *, skip: int = 0, limit: int = 50) -> list[User]:
        return self.db.query(User).order_by(User.id).offset(skip).limit(limit).all()

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_user(user_id)
        if not user:
            raise LookupError("user not found")

        if data.username or data.email:
            self._unique_or_raise(
                username=data.username or user.username,
                email=data.email or user.email,
                skip_id=user_id,
            )

        if data.username:
            user.username = data.username
        if data.email:
            user.email = data.email
        if data.password:
            user.hashed_password = get_password_hash(data.password)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        if not user:
            raise LookupError("user not found")
        self.db.delete(user)
        self.db.commit()
