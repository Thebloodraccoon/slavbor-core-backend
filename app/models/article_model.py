from datetime import datetime

from sqlalchemy import (ARRAY, Boolean, CheckConstraint, Column, DateTime,
                        ForeignKey, Index, Integer, String, Text)
from sqlalchemy.orm import relationship

from app.constants import (ARTICLE_CATEGORIES, ARTICLE_STATUSES, ARTICLE_TYPES,
                           CANONICAL_STATUSES, SOURCE_TYPES, VISIBILITY_LEVELS,
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

    # Authorship and timestamps
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    last_modified_by_user_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_by_user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )

    # Content structure
    summary = Column(Text)
    tags = Column(ARRAY(String))  # type: ignore

    # Categorization
    category = Column(String(50), index=True)
    historical_period = Column(String(100), index=True)

    # Primary entity relationships (only one main subject)
    primary_character_id = Column(Integer, ForeignKey("characters.id"), index=True)
    primary_location_id = Column(Integer, ForeignKey("locations.id"), index=True)
    primary_faction_id = Column(Integer, ForeignKey("factions.id"), index=True)
    primary_race_id = Column(Integer, ForeignKey("races.id"), index=True)

    # Related entities (multiple relationships)
    related_characters = Column(ARRAY(Integer))  # type: ignore
    related_locations = Column(ARRAY(Integer))  # type: ignore
    related_factions = Column(ARRAY(Integer))  # type: ignore
    related_races = Column(ARRAY(Integer))  # type: ignore

    # Source and authenticity
    source_type = Column(String(30), default="original", index=True)
    canonical_status = Column(String(20), default="canon", index=True)

    # Publication
    is_published = Column(Boolean, default=False, index=True)
    publication_date = Column(DateTime)
    visibility_level = Column(String(20), default="public", index=True)

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
            create_enum_constraint(
                "visibility_level", VISIBILITY_LEVELS, nullable=False
            ),
            name="check_visibility_level",
        ),
        Index("idx_article_type_status", "article_type", "status"),
        Index("idx_article_category_published", "category", "is_published"),
        Index("idx_article_publication", "is_published", "publication_date"),
        Index("idx_article_created_by", "created_by_user_id", "created_at"),
        Index("idx_article_tags", "tags", postgresql_using="gin"),
        Index(
            "idx_article_related_chars", "related_characters", postgresql_using="gin"
        ),
        Index("idx_article_related_locs", "related_locations", postgresql_using="gin"),
        Index(
            "idx_article_related_factions", "related_factions", postgresql_using="gin"
        ),
        Index("idx_article_related_races", "related_races", postgresql_using="gin"),
        Index(
            "idx_article_title_trgm",
            "title",
            postgresql_using="gin",
            postgresql_ops={"title": "gin_trgm_ops"},
        ),
        Index("idx_article_content_fts", "content", postgresql_using="gin"),
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
