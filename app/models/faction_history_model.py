from datetime import datetime

from sqlalchemy import (ARRAY, Column, DateTime, ForeignKey, Index, Integer,
                        String, Text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.settings.base import Base


class FactionCulture(Base):
    """Cultural and religious information about the faction"""

    __tablename__ = "faction_culture"

    id = Column(Integer, primary_key=True)
    faction_id = Column(
        Integer, ForeignKey("factions.id"), nullable=False, unique=True, index=True
    )

    # Cultural aspects
    dominant_culture = Column(String(50), index=True)
    primary_religion = Column(String(50), index=True)
    cultural_practices = Column(Text)
    symbols_and_heraldry = Column(Text)

    # Organizational culture
    internal_structure = Column(JSONB)
    key_positions = Column(ARRAY(String))  # type: ignore
    membership_requirements = Column(Text)
    internal_politics = Column(Text)

    # Current activities
    current_goals = Column(Text)
    current_conflicts = Column(Text)
    current_projects = Column(ARRAY(String))  # type: ignore

    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    __table_args__ = (
        Index("idx_faction_culture_religion", "dominant_culture", "primary_religion"),
        Index("idx_faction_structure", "internal_structure", postgresql_using="gin"),
        Index("idx_faction_projects", "current_projects", postgresql_using="gin"),
        Index("idx_faction_positions", "key_positions", postgresql_using="gin"),
    )

    faction = relationship("Faction", back_populates="culture")

    def __repr__(self):
        return f"<FactionCulture(faction_id={self.faction_id}, culture='{self.dominant_culture}')>"
