from datetime import datetime

from sqlalchemy import (ARRAY, CheckConstraint, Column, DateTime, ForeignKey,
                        Index, Integer, String, Text)
from sqlalchemy.orm import relationship

from app.constants import (CHARACTER_STATUSES, CHARACTER_TYPES, SOCIAL_RANKS,
                           create_enum_constraint)
from app.settings import settings


class Character(settings.Base):  # type: ignore
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)

    # Required basic information
    name = Column(String(200), nullable=False, index=True)
    type = Column(String(20), nullable=False, default="npc", index=True)
    status = Column(String(20), nullable=False, default="alive", index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    player_user_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_by_user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )

    # Optional name information
    full_name = Column(String(400), index=True)

    race_id = Column(Integer, ForeignKey("races.id", ondelete="SET NULL"), index=True)

    # Biography information
    biography = Column(Text)
    personality_traits = Column(Text)
    birth_year = Column(Integer, index=True)
    death_year = Column(Integer, index=True)

    # Social status information
    social_rank = Column(String(50), index=True)

    # Notes and comments
    dm_notes = Column(Text)
    player_notes = Column(Text)

    __table_args__ = (
        CheckConstraint(
            create_enum_constraint("type", CHARACTER_TYPES, nullable=False),
            name="check_character_type",
        ),
        CheckConstraint(
            create_enum_constraint("status", CHARACTER_STATUSES, nullable=False),
            name="check_character_status",
        ),
        CheckConstraint(
            create_enum_constraint("social_rank", SOCIAL_RANKS),
            name="check_social_rank",
        ),
        CheckConstraint(
            "birth_year IS NULL OR birth_year > 0", name="check_birth_year"
        ),
        CheckConstraint(
            "death_year IS NULL OR death_year > 0", name="check_death_year"
        ),
        CheckConstraint(
            "death_year IS NULL OR birth_year IS NULL OR death_year >= birth_year",
            name="check_death_after_birth",
        ),
        Index("idx_character_type_status", "type", "status"),
        Index("idx_character_player_user", "player_user_id", "type"),
        Index("idx_character_created_by", "created_by_user_id", "created_at"),
        Index(
            "idx_character_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )

    def __repr__(self):
        return f"<Character(id={self.id}, name='{self.name}', type='{self.type}')>"
