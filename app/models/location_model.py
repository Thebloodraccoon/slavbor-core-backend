from datetime import datetime

from sqlalchemy import Column, Integer, CheckConstraint, String, DateTime, ForeignKey, ARRAY, Text, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.settings.base import Base


class Location(Base):
    __tablename__ = 'locations'

    # Primary key
    id = Column(Integer, primary_key=True)

    # Required basic information
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(30), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_by_user_id = Column(Integer, ForeignKey('users.id'), index=True)

    # Optional descriptive information
    description = Column(Text)
    alternative_names = Column(ARRAY(String))

    # Geographic hierarchy
    parent_location_id = Column(Integer, ForeignKey('locations.id'), index=True)
    region = Column(String(50), index=True)

    # Geographic and climate information
    climate = Column(String(30), index=True)
    terrain = Column(String(30))
    elevation = Column(Integer)

    # Settlement information
    population = Column(Integer, index=True)
    population_composition = Column(JSONB)

    # Political and administrative
    government_type = Column(String(50), index=True)
    current_ruler_name = Column(String(200), index=True)
    controlling_faction_name = Column(String(100), index=True)
    political_status = Column(String(30), default='независимая')

    # Economic information
    wealth_level = Column(String(20), index=True)
    main_trade_goods = Column(ARRAY(String))
    natural_resources = Column(ARRAY(String))
    trade_routes = Column(ARRAY(String))

    # Military and strategic
    fortification_level = Column(String(20), index=True)
    strategic_importance = Column(String(20), index=True)
    garrison_size = Column(Integer)

    # Historical information
    founded_year = Column(Integer, index=True)
    historical_periods = Column(ARRAY(String))
    major_events = Column(ARRAY(String))

    # Cultural and religious
    dominant_culture = Column(String(50))
    languages_spoken = Column(ARRAY(String))
    religious_sites = Column(ARRAY(String))
    cultural_landmarks = Column(ARRAY(String))

    # Physical features and infrastructure
    notable_features = Column(Text)
    infrastructure_level = Column(String(20))
    notable_buildings = Column(ARRAY(String))

    # Geographic coordinates
    map_x = Column(Integer, index=True)
    map_y = Column(Integer, index=True)

    # Accessibility and connections
    accessible_by = Column(ARRAY(String))
    connected_locations = Column(ARRAY(Integer))
    travel_restrictions = Column(Text)

    # Current status and condition
    current_status = Column(String(20), default='активная', index=True)
    habitability = Column(String(20), default='пригодная')
    danger_level = Column(String(20), default='безопасная', index=True)

    # Seasonal and temporal variations
    seasonal_changes = Column(Text)
    special_events = Column(ARRAY(String))

    __table_args__ = (
        CheckConstraint(
            """type IN (
                'континент', 'страна', 'регион', 'княжество', 'провинция',
                'город', 'столица', 'деревня', 'поселок', 'хутор',
                'крепость', 'замок', 'форт', 'застава',
                'храм', 'монастырь', 'святилище',
                'руины', 'развалины', 'древний_город',
                'порт', 'пристань', 'переправа',
                'дорога', 'торговый_путь', 'перевал',
                'лес', 'роща', 'болото', 'пустыня', 'горы',
                'река', 'озеро', 'море', 'залив'
            )""",
            name="check_location_type"
        ),

        CheckConstraint(
            """wealth_level IS NULL OR wealth_level IN (
                'нищая', 'бедная', 'скромная', 'средняя', 'богатая', 'очень_богатая', 'баснословно_богатая'
            )""",
            name="check_wealth_level"
        ),

        CheckConstraint(
            """fortification_level IS NULL OR fortification_level IN (
                'открытая', 'частично_укрепленная', 'укрепленная', 'крепость', 'неприступная_крепость'
            )""",
            name="check_fortification_level"
        ),

        CheckConstraint(
            """strategic_importance IS NULL OR strategic_importance IN (
                'незначительная', 'низкая', 'средняя', 'высокая', 'критическая'
            )""",
            name="check_strategic_importance"
        ),

        CheckConstraint(
            """current_status IN (
                'процветающая', 'активная', 'стабильная', 'в_упадке', 'заброшенная', 'руины', 'разрушенная'
            )""",
            name="check_current_status"
        ),

        CheckConstraint(
            """danger_level IS NULL OR danger_level IN (
                'очень_безопасная', 'безопасная', 'относительно_безопасная', 'опасная', 'очень_опасная', 'смертельная'
            )""",
            name="check_danger_level"
        ),

        CheckConstraint("population IS NULL OR population >= 0", name="check_population_positive"),
        CheckConstraint("garrison_size IS NULL OR garrison_size >= 0", name="check_garrison_positive"),
        CheckConstraint("founded_year IS NULL OR founded_year > 0", name="check_founded_year_positive"),

        # Complex indexes only
        Index('idx_location_type_region', 'type', 'region'),
        Index('idx_location_wealth_population', 'wealth_level', 'population'),
        Index('idx_location_strategic_military', 'strategic_importance', 'fortification_level'),
        Index('idx_location_coordinates', 'map_x', 'map_y'),
        Index('idx_location_trade_goods', 'main_trade_goods', postgresql_using='gin'),
        Index('idx_location_resources', 'natural_resources', postgresql_using='gin'),
        Index('idx_location_languages', 'languages_spoken', postgresql_using='gin'),
        Index('idx_location_routes', 'trade_routes', postgresql_using='gin'),
        Index('idx_location_events', 'major_events', postgresql_using='gin'),
        Index('idx_location_landmarks', 'cultural_landmarks', postgresql_using='gin'),
        Index('idx_location_name_trgm', 'name', postgresql_using='gin', postgresql_ops={'name': 'gin_trgm_ops'}),
        Index('idx_location_description_fts', 'description', postgresql_using='gin'),
    )

    # SQLAlchemy relationships
    parent_location = relationship("Location", remote_side=[id])
    child_locations = relationship("Location", remote_side=[parent_location_id])
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_locations")\

    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}', type='{self.type}')>"