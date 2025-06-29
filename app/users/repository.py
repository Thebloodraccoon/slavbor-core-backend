from typing import Optional

from sqlalchemy.orm import Session

from app.core.repository import BaseRepository
from app.models import User


class UserRepository(BaseRepository[User]):
    """Repository for the essence of User."""

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """Obtaining a user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Obtaining a user by username."""
        return self.db.query(User).filter(User.username == username).first()
