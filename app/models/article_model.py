from datetime import datetime

from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, ForeignKey,
                        Index, Integer, String, Text)
from sqlalchemy.orm import relationship

from app.constants import (ARTICLE_CATEGORIES, ARTICLE_STATUSES, ARTICLE_TYPES,
                           create_enum_constraint)
from app.settings import settings


class Article(settings.Base):  # type: ignore
    __tablename__ = "articles"
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

    # Categorization
    category = Column(String(50), index=True)
    historical_period = Column(String(100), index=True)

    # Primary entity relationships
    primary_character_id = Column(
        Integer, ForeignKey("characters.id", ondelete="SET NULL"), index=True
    )
    primary_location_id = Column(
        Integer, ForeignKey("locations.id", ondelete="SET NULL"), index=True
    )
    primary_faction_id = Column(
        Integer, ForeignKey("factions.id", ondelete="SET NULL"), index=True
    )
    primary_race_id = Column(
        Integer, ForeignKey("races.id", ondelete="SET NULL"), index=True
    )

    # Publication
    is_published = Column(Boolean, default=False, index=True)
    publication_date = Column(DateTime)

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
        Index("idx_article_type_status", "article_type", "status"),
        Index("idx_article_category_published", "category", "is_published"),
        Index("idx_article_created_by", "created_by_user_id", "created_at"),
        Index(
            "idx_article_title_trgm",
            "title",
            postgresql_using="gin",
            postgresql_ops={"title": "gin_trgm_ops"},
        ),
        Index("idx_article_content_fts", "content", postgresql_using="gin"),
    )

    def __repr__(self):
        return (
            f"<Article(id={self.id}, title='{self.title}', type='{self.article_type}')>"
        )
