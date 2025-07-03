from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, Boolean, Text

from app.constants import USER_ROLES, create_enum_constraint
from app.settings import settings


class User(settings.Base):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    bio = Column(Text, nullable=True)

    is_2fa_enabled = Column(Boolean, default=False, nullable=False)
    otp_secret = Column(String, nullable=True)

    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_login = Column(DateTime)

    __table_args__ = (
        CheckConstraint(
            create_enum_constraint("role", USER_ROLES, nullable=False),
            name="check_user_role",
        ),
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
