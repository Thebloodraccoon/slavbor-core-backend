from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Index, Integer, String, Text

from app.constants import CLASS_TYPES, create_enum_constraint
from app.settings import settings


class Class(settings.Base):  # type: ignore
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    type = Column(String(50), nullable=False, index=True)

    hit_dice = Column(String(10), default="d8")
    primary_ability = Column(String(20))

    is_spellcaster = Column(Boolean, default=False)
    is_playable = Column(Boolean, default=True, index=True)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    __table_args__ = (
        CheckConstraint(
            create_enum_constraint("type", CLASS_TYPES, nullable=False),
            name="check_class_type",
        ),
        Index(
            "idx_class_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
    )

    def __repr__(self):
        return f"<Class(id={self.id}, name='{self.name}', type='{self.type}')>"
