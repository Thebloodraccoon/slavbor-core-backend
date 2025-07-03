from datetime import datetime

from sqlalchemy import (CheckConstraint, Column, DateTime, ForeignKey,
                        Index, Integer, String, Text)

from app.constants import (FACTION_STATUSES, FACTION_TYPES, LEADERSHIP_TYPES,
                           create_enum_constraint)
from app.settings import settings


class Faction(settings.Base):  # type: ignore
    __tablename__ = "factions"
    id = Column(Integer, primary_key=True)

    # Basic info
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)
    description = Column(Text)

    # Hierarchy
    parent_faction_id = Column(Integer, ForeignKey("factions.id"), index=True)

    # Status
    status = Column(String(30), default="активная", index=True)
    founded_year = Column(Integer, index=True)
    fallen_year = Column(Integer)

    # Leadership
    leadership_type = Column(String(30), index=True)
    current_leader_name = Column(String(200), index=True)

    # Culture
    dominant_culture = Column(String(50), index=True)
    primary_religion = Column(String(50), index=True)
    current_goals = Column(Text)

    # Metadata
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    created_by_user_id = Column(Integer, ForeignKey("users.id"), index=True)

    __table_args__ = (
        CheckConstraint(
            create_enum_constraint("type", FACTION_TYPES, nullable=False),
            name="check_faction_type",
        ),
        CheckConstraint(
            create_enum_constraint("leadership_type", LEADERSHIP_TYPES),
            name="check_leadership_type",
        ),
        CheckConstraint(
            create_enum_constraint("status", FACTION_STATUSES, nullable=False),
            name="check_faction_status",
        ),
        CheckConstraint(
            "founded_year IS NULL OR founded_year > 0",
            name="check_founded_year_positive",
        ),
        CheckConstraint(
            "fallen_year IS NULL OR fallen_year > 0", name="check_fallen_year_positive"
        ),
        CheckConstraint(
            "fallen_year IS NULL OR founded_year IS NULL OR fallen_year >= founded_year",
            name="check_fall_after_founding",
        ),
        # Basic indexes
        Index("idx_faction_type_status", "type", "status"),
        Index("idx_faction_hierarchy", "parent_faction_id", "type"),
        Index(
            "idx_faction_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
        Index("idx_faction_culture_religion", "dominant_culture", "primary_religion"),
    )

    def __repr__(self):
        return f"<Faction(id={self.id}, name='{self.name}', type='{self.type}')>"
