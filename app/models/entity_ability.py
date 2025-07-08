from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, Index, Integer, String, UniqueConstraint

from app.constants import ENTITY_TYPES, create_enum_constraint
from app.settings import settings


class EntityAbility(settings.Base):  # type: ignore
    __tablename__ = "entity_abilities"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String(20), nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)
    ability_id = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    __table_args__ = (
        CheckConstraint(
            create_enum_constraint("entity_type", ENTITY_TYPES, nullable=False),
            name="check_entity_type",
        ),
        UniqueConstraint("entity_type", "entity_id", "ability_id", name="uq_entity_ability"),
        Index("idx_entity_ability_entity", "entity_type", "entity_id"),
        Index("idx_entity_ability_ability", "ability_id"),
        Index("idx_entity_ability_type", "entity_type"),
    )

    def __repr__(self):
        return f"<EntityAbility(entity_type='{self.entity_type}', entity_id={self.entity_id}, ability_id={self.ability_id})>"
