from typing import Optional

from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    """Repository for the essence of User."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Getting a user for ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Obtaining a user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Obtaining a user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self, *, skip: int = 0, limit: int = 50) -> list[User]:
        """Obtaining all user with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, user_data: dict) -> User:
        """Creating a new user."""
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, update_data: dict) -> User:
        """Update the existing user."""
        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> bool:
        """Removing the user."""
        self.db.delete(user)
        self.db.commit()
        return True
