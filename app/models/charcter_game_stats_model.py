from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer

from app.constants import create_range_constraint
from app.settings import settings


class CharacterGameStats(settings.Base):  # type: ignore
    __tablename__ = "character_game_stats"
    id = Column(Integer, primary_key=True)

    # Foreign key to character
    character_id = Column(
        Integer,
        ForeignKey("characters.id"),
        nullable=False,
        unique=True,
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

    # Character Build
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="SET NULL"))
    subclass_id = Column(Integer, ForeignKey("classes.id", ondelete="SET NULL"))

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    __table_args__ = (
        CheckConstraint(create_range_constraint("level", 1, 20), name="check_level_range"),
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
        CheckConstraint("armor_class IS NULL OR armor_class > 0", name="check_ac_positive"),
        CheckConstraint("hit_points_max IS NULL OR hit_points_max > 0", name="check_hp_max_positive"),
        CheckConstraint(
            "hit_points_current IS NULL OR hit_points_current >= 0",
            name="check_hp_current_nonnegative",
        ),
    )

    def __repr__(self):
        return f"<CharacterGameStats(character_id={self.character_id}, level={self.level}, class='{self.character_class}')>"
