from sqlalchemy import Column, ForeignKey, Index, Integer, String, UniqueConstraint

from app.settings import settings


class ArticleTag(settings.Base):  # type: ignore
    __tablename__ = "article_tags"
    id = Column(Integer, primary_key=True)

    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    tag = Column(String(50), nullable=False)

    __table_args__ = (
        Index("idx_article_tags_article", "article_id"),
        Index("idx_article_tags_tag", "tag"),
        UniqueConstraint("article_id", "tag", name="uq_article_tag"),
    )
