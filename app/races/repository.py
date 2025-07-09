from sqlalchemy.orm import Session

from app.core.repository import BaseRepository
from app.models import Race


class RaceRepository(BaseRepository[Race]):
    """Repository for working with Race in the database"""

    def __init__(self, db: Session):
        super().__init__(Race, db)

    def get_by_name(self, name: str) -> Race | None:
        """Obtaining a race by name."""
        return self.db.query(Race).filter(Race.name == name).first()

    def exists_by_name(self, name: str, exclude_id: int | None = None) -> bool:
        """Checking the existence of a race by name."""
        query = self.db.query(Race).filter(Race.name == name)
        if exclude_id:
            query = query.filter(Race.id != exclude_id)
        return query.first() is not None

    def get_playable_races(self) -> list[Race]:
        """Obtaining only playable races."""
        return self.db.query(Race).filter(Race.is_playable).all()
