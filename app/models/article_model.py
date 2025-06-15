from datetime import datetime

from sqlalchemy import (ARRAY, Boolean, CheckConstraint, Column, DateTime,
                        ForeignKey, Index, Integer, String, Text)
from sqlalchemy.orm import relationship

from app.constants import (ARTICLE_CATEGORIES, ARTICLE_STATUSES, ARTICLE_TYPES,
                           CANONICAL_STATUSES, DIFFICULTY_LEVELS,
                           RELIABILITY_LEVELS, SOURCE_TYPES, VISIBILITY_LEVELS,
                           create_enum_constraint)
from app.settings.base import Base


class Article(Base):
    __tablename__ = "articles"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Required basic information
    title = Column(String(300), nullable=False, index=True)
    content = Column(Text, nullable=False)
    article_type = Column(String(50), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="draft", index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    last_modified_by_user_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_by_user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )

    # Content structure and metadata
    subtitle = Column(String(500))
    summary = Column(Text)
    tags = Column(ARRAY(String))

    # Categorization and topic classification
    category = Column(String(50), index=True)
    subcategory = Column(String(50))
    topic = Column(String(100))
    historical_period = Column(String(100), index=True)

    # Relationships to world entities
    primary_character_id = Column(Integer, ForeignKey("characters.id"), index=True)
    primary_location_id = Column(Integer, ForeignKey("locations.id"), index=True)
    primary_faction_id = Column(Integer, ForeignKey("factions.id"), index=True)
    primary_race_id = Column(Integer, ForeignKey("races.id"), index=True)

    # Related entities (multiple relationships)
    related_characters = Column(ARRAY(Integer))
    related_locations = Column(ARRAY(Integer))
    related_factions = Column(ARRAY(Integer))
    related_races = Column(ARRAY(Integer))

    # Geographic and temporal context
    geographic_scope = Column(String(100))
    time_period_start = Column(Integer)
    time_period_end = Column(Integer)
    in_world_date = Column(String(100))

    # Content organization
    word_count = Column(Integer)
    reading_time_minutes = Column(Integer)
    difficulty_level = Column(String(20), default="medium", index=True)

    # Source and authenticity
    source_type = Column(String(30), default="original", index=True)
    source_documents = Column(ARRAY(String))
    canonical_status = Column(String(20), default="canon", index=True)
    reliability_level = Column(String(20), default="reliable")

    # Publication and visibility
    is_published = Column(Boolean, default=False, index=True)
    is_public = Column(Boolean, default=True, index=True)
    publication_date = Column(DateTime)
    visibility_level = Column(String(20), default="public", index=True)

    # Content structure metadata
    has_images = Column(Boolean, default=False)
    has_maps = Column(Boolean, default=False)
    has_timelines = Column(Boolean, default=False)
    has_character_sheets = Column(Boolean, default=False)

    # Cultural and linguistic context
    languages_mentioned = Column(ARRAY(String))
    cultural_context = Column(ARRAY(String))
    religious_context = Column(ARRAY(String))

    __table_args__ = (
        CheckConstraint(
            create_enum_constraint("article_type", ARTICLE_TYPES, nullable=False),
            name="check_article_type",
        ),
        CheckConstraint(
            create_enum_constraint("status", ARTICLE_STATUSES, nullable=False),
            name="check_article_status",
        ),
        CheckConstraint(
            create_enum_constraint("category", ARTICLE_CATEGORIES),
            name="check_article_category",
        ),
        CheckConstraint(
            create_enum_constraint(
                "difficulty_level", DIFFICULTY_LEVELS, nullable=False
            ),
            name="check_difficulty_level",
        ),
        CheckConstraint(
            create_enum_constraint("source_type", SOURCE_TYPES, nullable=False),
            name="check_source_type",
        ),
        CheckConstraint(
            create_enum_constraint(
                "canonical_status", CANONICAL_STATUSES, nullable=False
            ),
            name="check_canonical_status",
        ),
        CheckConstraint(
            create_enum_constraint("reliability_level", RELIABILITY_LEVELS),
            name="check_reliability_level",
        ),
        CheckConstraint(
            create_enum_constraint(
                "visibility_level", VISIBILITY_LEVELS, nullable=False
            ),
            name="check_visibility_level",
        ),
        CheckConstraint(
            "word_count IS NULL OR word_count >= 0", name="check_word_count_positive"
        ),
        CheckConstraint(
            "reading_time_minutes IS NULL OR reading_time_minutes >= 0",
            name="check_reading_time_positive",
        ),
        CheckConstraint(
            "time_period_start IS NULL OR time_period_start > 0",
            name="check_start_period_positive",
        ),
        CheckConstraint(
            "time_period_end IS NULL OR time_period_end > 0",
            name="check_end_period_positive",
        ),
        CheckConstraint(
            "time_period_end IS NULL OR time_period_start IS NULL OR time_period_end >= time_period_start",
            name="check_period_chronology",
        ),
        Index("idx_article_type_status", "article_type", "status"),
        Index("idx_article_category_published", "category", "is_published"),
        Index("idx_article_publication", "is_published", "publication_date"),
        Index("idx_article_visibility", "visibility_level", "is_public"),
        Index(
            "idx_article_period",
            "historical_period",
            "time_period_start",
            "time_period_end",
        ),
        Index("idx_article_created_by", "created_by_user_id", "created_at"),
        Index("idx_article_last_modified_by", "last_modified_by_user_id", "updated_at"),
        Index("idx_article_tags", "tags", postgresql_using="gin"),
        Index(
            "idx_article_related_chars", "related_characters", postgresql_using="gin"
        ),
        Index("idx_article_related_locs", "related_locations", postgresql_using="gin"),
        Index(
            "idx_article_related_factions", "related_factions", postgresql_using="gin"
        ),
        Index("idx_article_related_races", "related_races", postgresql_using="gin"),
        Index("idx_article_languages", "languages_mentioned", postgresql_using="gin"),
        Index(
            "idx_article_cultural_context", "cultural_context", postgresql_using="gin"
        ),
        Index(
            "idx_article_religious_context", "religious_context", postgresql_using="gin"
        ),
        Index("idx_article_sources", "source_documents", postgresql_using="gin"),
        Index(
            "idx_article_title_trgm",
            "title",
            postgresql_using="gin",
            postgresql_ops={"title": "gin_trgm_ops"},
        ),
        Index("idx_article_content_fts", "content", postgresql_using="gin"),
        Index("idx_article_summary_fts", "summary", postgresql_using="gin"),
    )

    # SQLAlchemy relationships
    created_by_user = relationship(
        "User", foreign_keys=[created_by_user_id], back_populates="created_articles"
    )
    last_modified_by_user = relationship(
        "User",
        foreign_keys=[last_modified_by_user_id],
        back_populates="last_modified_articles",
    )
    primary_character = relationship("Character", foreign_keys=[primary_character_id])
    primary_location = relationship("Location", foreign_keys=[primary_location_id])
    primary_faction = relationship(
        "Faction", foreign_keys=[primary_faction_id], back_populates="articles"
    )
    primary_race = relationship(
        "Race", foreign_keys=[primary_race_id], back_populates="articles"
    )

    def __repr__(self):
        return (
            f"<Article(id={self.id}, title='{self.title}', type='{self.article_type}')>"
        )
