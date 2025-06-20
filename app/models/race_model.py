from datetime import datetime

from sqlalchemy import (ARRAY, Boolean, CheckConstraint, Column, DateTime,
                        ForeignKey, Index, Integer, String, Text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.constants import RACE_RARITIES, RACE_SIZES, create_enum_constraint
from app.settings.base import Base


class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True)

    # Required basic information
    name = Column(String(100), nullable=False, unique=True, index=True)

    # Optional descriptive information
    description = Column(Text)
    size = Column(String(20), default="Средний", index=True)

    # Racial abilities and traits
    racial_abilities = Column(ARRAY(Text))  # type: ignore
    stat_bonuses = Column(JSONB, default={})
    languages = Column(ARRAY(String))  # type: ignore
    special_traits = Column(Text)

    # Physical characteristics
    average_height = Column(String(50))
    average_weight = Column(String(50))
    physical_features = Column(Text)

    # Gameplay mechanics
    is_playable = Column(Boolean, default=True, index=True)
    rarity = Column(String(20), default="обычная", index=True)

    # World integration
    homeland_regions = Column(ARRAY(String))  # type: ignore

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
        # Complex indexes only
        Index("idx_race_playable_size", "is_playable", "size"),
        Index("idx_race_stat_bonuses", "stat_bonuses", postgresql_using="gin"),
        Index("idx_race_abilities", "racial_abilities", postgresql_using="gin"),
        Index("idx_race_languages", "languages", postgresql_using="gin"),
        Index("idx_race_regions", "homeland_regions", postgresql_using="gin"),
        Index(
            "idx_race_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )

    # Relationships
    characters = relationship("Character", back_populates="race")
    articles = relationship("Article", back_populates="primary_race")

    def __repr__(self):
        return f"<Race(id={self.id}, name='{self.name}', size='{self.size}')>"
