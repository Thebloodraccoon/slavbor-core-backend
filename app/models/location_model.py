from datetime import datetime

from sqlalchemy import (ARRAY, CheckConstraint, Column, DateTime, ForeignKey,
                        Index, Integer, String, Text)
from sqlalchemy.orm import relationship

from app.constants import (DANGER_LEVELS, LOCATION_STATUSES, LOCATION_TYPES,
                           create_enum_constraint)
from app.settings import settings


class Location(settings.Base):  # type: ignore
    """Основная модель локации - содержит базовую информацию"""

    __tablename__ = "locations"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Required basic information
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(30), nullable=False, index=True)

    # Basic description
    description = Column(Text)
    alternative_names = Column(ARRAY(String))  # type: ignore

    # Geographic hierarchy
    parent_location_id = Column(Integer, ForeignKey("locations.id"), index=True)
    region = Column(String(50), index=True)

    # Basic geographic information
    climate = Column(String(30), index=True)
    terrain = Column(String(30))

    # Current status
    current_status = Column(String(20), default="активная", index=True)
    danger_level = Column(String(20), default="безопасная", index=True)

    # Coordinates (basic positioning)
    map_x = Column(Integer, index=True)
    map_y = Column(Integer, index=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    created_by_user_id = Column(Integer, ForeignKey("users.id"), index=True)

    __table_args__ = (
        CheckConstraint(
            create_enum_constraint("type", LOCATION_TYPES, nullable=False),
            name="check_location_type",
        ),
        CheckConstraint(
            create_enum_constraint("current_status", LOCATION_STATUSES, nullable=False),
            name="check_current_status",
        ),
        CheckConstraint(
            create_enum_constraint("danger_level", DANGER_LEVELS),
            name="check_danger_level",
        ),
        # Basic indexes
        Index("idx_location_type_region", "type", "region"),
        Index("idx_location_coordinates", "map_x", "map_y"),
        Index("idx_location_status_danger", "current_status", "danger_level"),
        Index(
            "idx_location_name_trgm",
            "name",
            postgresql_using="gin",
            postgresql_ops={"name": "gin_trgm_ops"},
        ),
        Index(
            "idx_location_alternative_names",
            "alternative_names",
            postgresql_using="gin",
        ),
        Index("idx_location_description_fts", "description", postgresql_using="gin"),
    )

    # Relationships
    parent_location = relationship("Location", remote_side=[id])
    child_locations = relationship("Location", overlaps="parent_location")
    created_by_user = relationship(
        "User", foreign_keys=[created_by_user_id], back_populates="created_locations"
    )

    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}', type='{self.type}')>"
