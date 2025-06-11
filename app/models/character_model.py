from datetime import datetime

from sqlalchemy import Column, Integer, CheckConstraint, String, DateTime, ForeignKey, ARRAY, Text, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.settings.base import Base


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)

    # Required basic information
    name = Column(String(200), nullable=False, index=True)
    type = Column(String(20), nullable=False, default='npc', index=True)
    status = Column(String(20), nullable=False, default='alive', index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    player_user_id = Column(Integer, ForeignKey('users.id'), index=True)
    created_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Optional name information
    full_name = Column(String(400), index=True)
    titles = Column(ARRAY(String))
    epithets = Column(ARRAY(String))

    # Foreign key relationships
    race_id = Column(Integer, ForeignKey('races.id'), index=True)

    # Locations и factions
    current_location_name = Column(String(100), index=True)
    birth_location_name = Column(String(100), index=True)
    primary_faction_name = Column(String(100), index=True)

    # Biography information
    biography = Column(Text)
    personality_traits = Column(Text)
    birth_year = Column(Integer, index=True)
    death_year = Column(Integer, index=True)

    # D&D game statistics
    level = Column(Integer)
    strength = Column(Integer)
    dexterity = Column(Integer)
    constitution = Column(Integer)
    intelligence = Column(Integer)
    wisdom = Column(Integer)
    charisma = Column(Integer)

    # Social status information
    social_rank = Column(String(50), index=True)
    wealth_level = Column(String(30), index=True)

    # Family relationships
    father_name = Column(String(200), index=True)
    mother_name = Column(String(200), index=True)

    # Faction
    secondary_factions = Column(ARRAY(Integer))
    faction_roles = Column(JSONB)
    faction_status = Column(String(20), default='member')

    # Game session information
    campaign_id = Column(Integer, index=True)
    player_id = Column(Integer, index=True)

    # Notes and comments
    dm_notes = Column(Text)
    player_notes = Column(Text)

    __table_args__ = (
        CheckConstraint(
            "type IN ('npc', 'player', 'historical', 'deity', 'legendary', 'template')",
            name="check_character_type"
        ),

        CheckConstraint(
            "status IN ('alive', 'dead', 'missing', 'legendary', 'unknown')",
            name="check_character_status"
        ),

        CheckConstraint(
            """social_rank IS NULL OR social_rank IN (
                'император', 'король', 'князь', 'герцог', 'граф', 'боярин', 
                'рыцарь', 'дворянин', 'торговец', 'ремесленник', 'крестьянин', 'раб'
            )""",
            name="check_social_rank"
        ),

        CheckConstraint(
            """wealth_level IS NULL OR wealth_level IN (
                'нищий', 'бедный', 'средний', 'богатый', 'очень_богатый'
            )""",
            name="check_wealth_level"
        ),

        CheckConstraint("strength IS NULL OR (strength >= 1 AND strength <= 30)", name="check_strength_range"),
        CheckConstraint("dexterity IS NULL OR (dexterity >= 1 AND dexterity <= 30)", name="check_dexterity_range"),
        CheckConstraint("constitution IS NULL OR (constitution >= 1 AND constitution <= 30)", name="check_constitution_range"),
        CheckConstraint("intelligence IS NULL OR (intelligence >= 1 AND intelligence <= 30)", name="check_intelligence_range"),
        CheckConstraint("wisdom IS NULL OR (wisdom >= 1 AND wisdom <= 30)", name="check_wisdom_range"),
        CheckConstraint("charisma IS NULL OR (charisma >= 1 AND charisma <= 30)", name="check_charisma_range"),
        CheckConstraint("level IS NULL OR (level >= 1 AND level <= 30)", name="check_level_range"),

        CheckConstraint("birth_year IS NULL OR birth_year > 0", name="check_birth_year"),
        CheckConstraint("death_year IS NULL OR death_year > 0", name="check_death_year"),
        CheckConstraint(
            "death_year IS NULL OR birth_year IS NULL OR death_year >= birth_year",
            name="check_death_after_birth"
        ),

        # Complex indexes only
        Index('idx_character_type_status', 'type', 'status'),
        Index('idx_character_player_user', 'player_user_id', 'type'),  # ДОБАВЛЕНО обратно
        Index('idx_character_created_by', 'created_by_user_id', 'created_at'),  # ДОБАВЛЕНО обратно
        Index('idx_character_name_trgm', 'name', postgresql_using='gin', postgresql_ops={'name': 'gin_trgm_ops'}),
        Index('idx_character_secondary_factions', 'secondary_factions', postgresql_using='gin'),
        Index('idx_character_faction_roles', 'faction_roles', postgresql_using='gin'),
    )

    # SQLAlchemy relationships
    race = relationship("Race", back_populates="characters")
    player_user = relationship("User", foreign_keys=[player_user_id], back_populates="player_characters")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_characters")

    def __repr__(self):
        return f"<Character(id={self.id}, name='{self.name}', type='{self.type}')>"
