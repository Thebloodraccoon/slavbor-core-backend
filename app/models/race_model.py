from datetime import datetime

from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, Index,
                        Integer, String, Text)

from app.constants import RACE_RARITIES, RACE_SIZES, create_enum_constraint
from app.settings import settings


class Race(settings.Base):  # type: ignore
    __tablename__ = "races"

    id = Column(Integer, primary_key=True)

    # Required basic information
    name = Column(String(100), nullable=False, unique=True, index=True)

    # Optional descriptive information
    description = Column(Text)
    size = Column(String(20), default="Средний", index=True)
    special_traits = Column(Text)

    # Gameplay mechanics
    is_playable = Column(Boolean, default=True, index=True)
    rarity = Column(String(20), default="обычная", index=True)

    # Metadata and versioning
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            create_enum_constraint("size", RACE_SIZES, nullable=False),
            name="check_race_size",
        ),
        CheckConstraint(
            create_enum_constraint("rarity", RACE_RARITIES),
            name="check_race_rarity",
        ),
        Index(
            "idx_race_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )

    def __repr__(self):
        return f"<Race(id={self.id}, name='{self.name}', size='{self.size}')>"
