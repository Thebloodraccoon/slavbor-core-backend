from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.constants import USER_ROLES, create_enum_constraint
from app.settings.base import Base


class User(Base):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
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

    created_articles = relationship(
        "Article",
        foreign_keys="Article.created_by_user_id",
        back_populates="created_by_user",
    )
    last_modified_articles = relationship(
        "Article",
        foreign_keys="Article.last_modified_by_user_id",
        back_populates="last_modified_by_user",
    )
    player_characters = relationship(
        "Character",
        foreign_keys="Character.player_user_id",
        back_populates="player_user",
    )
    created_characters = relationship(
        "Character",
        foreign_keys="Character.created_by_user_id",
        back_populates="created_by_user",
    )
    created_locations = relationship(
        "Location",
        foreign_keys="Location.created_by_user_id",
        back_populates="created_by_user",
    )
    created_factions = relationship(
        "Faction",
        foreign_keys="Faction.created_by_user_id",
        back_populates="created_by_user",
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
