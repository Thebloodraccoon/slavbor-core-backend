from datetime import datetime

from sqlalchemy import (ARRAY, CheckConstraint, Column, DateTime, ForeignKey,
                        Index, Integer, String)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.constants import create_range_constraint
from app.settings.base import Base


class CharacterGameStats(Base):
    """D&d game statistics"""

    __tablename__ = "character_game_stats"
    id = Column(Integer, primary_key=True)

    # Foreign key to character
    character_id = Column(
        Integer, ForeignKey("characters.id"), nullable=False, unique=True, index=True
    )

    # D&D Core Statistics
    level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)

    # Ability Scores
    strength = Column(Integer, default=10)
    dexterity = Column(Integer, default=10)
    constitution = Column(Integer, default=10)
    intelligence = Column(Integer, default=10)
    wisdom = Column(Integer, default=10)
    charisma = Column(Integer, default=10)

    # Combat Statistics
    armor_class = Column(Integer)
    hit_points_max = Column(Integer)
    hit_points_current = Column(Integer)
    hit_dice = Column(String(20))  # e.g., "8d8"

    # Proficiency and Skills
    proficiency_bonus = Column(Integer)
    proficient_skills = Column(ARRAY(String))  # type: ignore
    proficient_saves = Column(ARRAY(String))  # type: ignore

    # Character Build
    character_class = Column(String(50))  # 'Fighter', 'Wizard', etc.
    character_subclass = Column(String(50))  # 'Champion', 'Evocation', etc.
    background = Column(String(50))  # 'Soldier', 'Noble', etc.
    alignment = Column(String(20))  # 'Lawful Good', etc.

    # Additional D&D specific info
    languages = Column(ARRAY(String))  # type: ignore
    tool_proficiencies = Column(ARRAY(String))  # type: ignore
    weapon_proficiencies = Column(ARRAY(String))  # type: ignore
    armor_proficiencies = Column(ARRAY(String))  # type: ignore

    # Spellcasting (if applicable)
    spellcasting_ability = Column(String(20))  # 'Intelligence', 'Wisdom', etc.
    spell_save_dc = Column(Integer)
    spell_attack_bonus = Column(Integer)
    spell_slots = Column(JSONB)  # {"1": 4, "2": 3, "3": 2} etc.
    spells_known = Column(ARRAY(String))  # type: ignore

    # Timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            create_range_constraint("level", 1, 20), name="check_level_range"
        ),
        CheckConstraint(
            "experience_points IS NULL OR experience_points >= 0",
            name="check_exp_positive",
        ),
        CheckConstraint(
            create_range_constraint("strength", 1, 30),
            name="check_strength_range",
        ),
        CheckConstraint(
            create_range_constraint("dexterity", 1, 30),
            name="check_dexterity_range",
        ),
        CheckConstraint(
            create_range_constraint("constitution", 1, 30),
            name="check_constitution_range",
        ),
        CheckConstraint(
            create_range_constraint("intelligence", 1, 30),
            name="check_intelligence_range",
        ),
        CheckConstraint(
            create_range_constraint("wisdom", 1, 30),
            name="check_wisdom_range",
        ),
        CheckConstraint(
            create_range_constraint("charisma", 1, 30),
            name="check_charisma_range",
        ),
        CheckConstraint(
            "armor_class IS NULL OR armor_class > 0", name="check_ac_positive"
        ),
        CheckConstraint(
            "hit_points_max IS NULL OR hit_points_max > 0", name="check_hp_max_positive"
        ),
        CheckConstraint(
            "hit_points_current IS NULL OR hit_points_current >= 0",
            name="check_hp_current_nonnegative",
        ),
        Index("idx_game_stats_level_class", "level", "character_class"),
        Index("idx_game_stats_abilities", "strength", "dexterity", "constitution"),
        Index("idx_game_stats_skills", "proficient_skills", postgresql_using="gin"),
        Index("idx_game_stats_spells", "spells_known", postgresql_using="gin"),
    )

    # Relationships
    character = relationship("Character", back_populates="game_stats")

    def __repr__(self):
        return f"<CharacterGameStats(character_id={self.character_id}, level={self.level}, class='{self.character_class}')>"
