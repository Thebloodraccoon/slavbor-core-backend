from datetime import datetime

from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, Index,
                        Integer, String, Text)

from app.constants import (ABILITY_CATEGORIES, create_enum_constraint,
                           create_range_constraint)
from app.settings import settings


class Ability(settings.Base):  # type: ignore
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(30), nullable=False, index=True)

    usage_type = Column(String(20), default="passive", index=True)
    resource_cost = Column(Integer, default=0)
    resource_type = Column(String(20))
    duration = Column(String(50))
    recharge = Column(String(20))

    attack_type = Column(String(20))
    damage_dice = Column(String(20))
    damage_type = Column(String(20))
    save_required = Column(String(20))
    save_dc = Column(Integer)

    strength_modifier = Column(Integer, default=0)
    dexterity_modifier = Column(Integer, default=0)
    constitution_modifier = Column(Integer, default=0)
    intelligence_modifier = Column(Integer, default=0)
    wisdom_modifier = Column(Integer, default=0)
    charisma_modifier = Column(Integer, default=0)

    resistances_text = Column(Text)
    special_effects_text = Column(Text)

    level_requirement = Column(Integer, default=1)
    class_requirement_id = Column(Integer)
    race_requirement_id = Column(Integer)
    other_requirements = Column(Text)

    is_magical = Column(Boolean, default=False)
    is_attack = Column(Boolean, default=False)
    is_spell = Column(Boolean, default=False)
    is_concentration = Column(Boolean, default=False)
    is_ritual = Column(Boolean, default=False)
    is_homebrew = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            create_enum_constraint("category", ABILITY_CATEGORIES, nullable=False),
            name="check_ability_category",
        ),
        CheckConstraint(
            create_range_constraint("level_requirement", 1, 20),
            name="check_level_requirement_range",
        ),
        CheckConstraint(
            "resource_cost IS NULL OR resource_cost >= 0",
            name="check_resource_cost_positive",
        ),
        CheckConstraint(
            "save_dc IS NULL OR save_dc > 0",
            name="check_save_dc_positive",
        ),
        CheckConstraint(
            create_range_constraint("strength_modifier", -10, 10),
            name="check_strength_modifier_range",
        ),
        CheckConstraint(
            create_range_constraint("dexterity_modifier", -10, 10),
            name="check_dexterity_modifier_range",
        ),
        CheckConstraint(
            create_range_constraint("constitution_modifier", -10, 10),
            name="check_constitution_modifier_range",
        ),
        CheckConstraint(
            create_range_constraint("intelligence_modifier", -10, 10),
            name="check_intelligence_modifier_range",
        ),
        CheckConstraint(
            create_range_constraint("wisdom_modifier", -10, 10),
            name="check_wisdom_modifier_range",
        ),
        CheckConstraint(
            create_range_constraint("charisma_modifier", -10, 10),
            name="check_charisma_modifier_range",
        ),
        Index("idx_ability_category", "category"),
        Index("idx_ability_usage_type", "usage_type"),
        Index("idx_ability_level_requirement", "level_requirement"),
        Index("idx_ability_class_requirement", "class_requirement_id"),
        Index("idx_ability_race_requirement", "race_requirement_id"),
        Index(
            "idx_ability_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
        Index("idx_ability_description_fts", "description", postgresql_using="gin"),
    )

    def __repr__(self):
        return (
            f"<Ability(id={self.id}, name='{self.name}', category='{self.category}')>"
        )
