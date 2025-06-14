from datetime import datetime

from sqlalchemy import (ARRAY, CheckConstraint, Column, DateTime, ForeignKey,
                        Index, Integer, String, Text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.constants import (ENTITY_WEALTH_LEVELS, FACTION_STATUSES,
                           FACTION_TYPES, HISTORICAL_IMPORTANCE_LEVELS,
                           LEADERSHIP_TYPES, POWER_LEVELS,
                           create_enum_constraint)
from app.settings.base import Base


class Faction(Base):
    __tablename__ = "factions"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Required basic information
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)

    # Extended naming
    full_name = Column(String(200), index=True)
    alternative_names = Column(ARRAY(String))
    dynastic_title = Column(String(100))

    # Basic description
    description = Column(Text)

    # Hierarchical structure
    parent_faction_id = Column(Integer, ForeignKey("factions.id"), index=True)
    faction_branch = Column(String(100))

    # Geographic control and influence
    primary_territory = Column(String(100), index=True)
    controlled_cities = Column(ARRAY(String))
    controlled_regions = Column(ARRAY(String))
    trade_routes_controlled = Column(ARRAY(String))

    # Political and administrative
    government_structure = Column(String(50))
    leadership_type = Column(String(30), index=True)
    current_leader_name = Column(String(200), index=True)
    succession_rules = Column(Text)

    # Status and timeline
    status = Column(String(30), default="активная", index=True)
    founded_year = Column(Integer, index=True)
    peak_power_period = Column(String(100))
    decline_started_year = Column(Integer)
    fallen_year = Column(Integer)

    # Allies and enemies
    traditional_allies = Column(ARRAY(String))
    traditional_enemies = Column(ARRAY(String))
    current_allies = Column(ARRAY(Integer))
    current_enemies = Column(ARRAY(Integer))
    diplomatic_status = Column(JSONB)

    # Power and influence metrics
    military_strength = Column(String(20), index=True)
    economic_power = Column(String(20), index=True)
    political_influence = Column(String(20), index=True)
    territorial_control = Column(String(20))

    # Economic information
    wealth_level = Column(String(30), index=True)
    primary_income_sources = Column(ARRAY(String))
    trade_specialization = Column(ARRAY(String))
    economic_assets = Column(JSONB)

    # Military information
    military_assets = Column(JSONB)
    military_specialization = Column(ARRAY(String))
    famous_military_units = Column(ARRAY(String))

    # Cultural and religious aspects
    dominant_culture = Column(String(50))
    primary_religion = Column(String(50))
    cultural_practices = Column(Text)
    symbols_and_heraldry = Column(Text)

    # Historical significance
    historical_importance = Column(String(20), index=True)
    major_achievements = Column(ARRAY(String))
    major_conflicts = Column(ARRAY(String))
    historical_events = Column(ARRAY(String))

    # Organizational structure
    internal_structure = Column(JSONB)
    key_positions = Column(ARRAY(String))
    membership_requirements = Column(Text)
    internal_politics = Column(Text)

    # Legacy and influence
    cultural_contributions = Column(ARRAY(String))
    legal_legacy = Column(Text)
    architectural_legacy = Column(ARRAY(String))

    # Current operations and activities
    current_goals = Column(Text)
    current_conflicts = Column(Text)
    current_projects = Column(ARRAY(String))

    # Metadata
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    created_by_user_id = Column(Integer, ForeignKey("users.id"), index=True)
    source_material = Column(String(100))

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
            create_enum_constraint("military_strength", POWER_LEVELS),
            name="check_military_strength",
        ),
        CheckConstraint(
            create_enum_constraint("economic_power", POWER_LEVELS),
            name="check_economic_power",
        ),
        CheckConstraint(
            create_enum_constraint("political_influence", POWER_LEVELS),
            name="check_political_influence",
        ),
        CheckConstraint(
            create_enum_constraint("wealth_level", ENTITY_WEALTH_LEVELS),
            name="check_wealth_level",
        ),
        CheckConstraint(
            create_enum_constraint(
                "historical_importance", HISTORICAL_IMPORTANCE_LEVELS
            ),
            name="check_historical_importance",
        ),
        # Constraints: Years must be reasonable
        CheckConstraint(
            "founded_year IS NULL OR founded_year > 0",
            name="check_founded_year_positive",
        ),
        CheckConstraint(
            "decline_started_year IS NULL OR decline_started_year > 0",
            name="check_decline_year_positive",
        ),
        CheckConstraint(
            "fallen_year IS NULL OR fallen_year > 0", name="check_fallen_year_positive"
        ),
        CheckConstraint(
            "decline_started_year IS NULL OR founded_year IS NULL OR decline_started_year >= founded_year",
            name="check_decline_after_founding",
        ),
        CheckConstraint(
            "fallen_year IS NULL OR founded_year IS NULL OR fallen_year >= founded_year",
            name="check_fall_after_founding",
        ),
        # Complex indexes only
        Index("idx_faction_type_status", "type", "status"),
        Index(
            "idx_faction_power_analysis",
            "military_strength",
            "economic_power",
            "political_influence",
        ),
        Index("idx_faction_territorial", "primary_territory", "status"),
        Index("idx_faction_historical", "founded_year", "historical_importance"),
        Index("idx_faction_hierarchy", "parent_faction_id", "type"),
        # Array indexes for complex searches
        Index("idx_faction_cities", "controlled_cities", postgresql_using="gin"),
        Index("idx_faction_regions", "controlled_regions", postgresql_using="gin"),
        Index(
            "idx_faction_trade_routes",
            "trade_routes_controlled",
            postgresql_using="gin",
        ),
        Index(
            "idx_faction_income_sources",
            "primary_income_sources",
            postgresql_using="gin",
        ),
        Index("idx_faction_trade_spec", "trade_specialization", postgresql_using="gin"),
        Index("idx_faction_achievements", "major_achievements", postgresql_using="gin"),
        Index("idx_faction_conflicts", "major_conflicts", postgresql_using="gin"),
        Index("idx_faction_allies", "traditional_allies", postgresql_using="gin"),
        Index("idx_faction_enemies", "traditional_enemies", postgresql_using="gin"),
        Index("idx_faction_current_allies", "current_allies", postgresql_using="gin"),
        Index("idx_faction_current_enemies", "current_enemies", postgresql_using="gin"),
        # JSON indexes for complex data
        Index("idx_faction_military_assets", "military_assets", postgresql_using="gin"),
        Index("idx_faction_economic_assets", "economic_assets", postgresql_using="gin"),
        Index("idx_faction_diplomacy", "diplomatic_status", postgresql_using="gin"),
        Index("idx_faction_structure", "internal_structure", postgresql_using="gin"),
        # Full-text search indexes
        Index(
            "idx_faction_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
        Index("idx_faction_description_fts", "description", postgresql_using="gin"),
    )

    # Relationships
    parent_faction = relationship("Faction", remote_side=[id])
    child_factions = relationship("Faction", overlaps="parent_faction")
    created_by_user = relationship(
        "User", foreign_keys=[created_by_user_id], back_populates="created_factions"
    )
    created_by_user = relationship(
        "User", foreign_keys=[created_by_user_id], back_populates="created_factions"
    )

    articles = relationship(
        "Article",
        foreign_keys="Article.primary_faction_id",
        back_populates="primary_faction",
    )

    def __repr__(self):
        return f"<Faction(id={self.id}, name='{self.name}', type='{self.type}')>"
