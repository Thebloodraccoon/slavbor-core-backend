from typing import Optional

from sqlalchemy.orm import Session

from app.models.race_model import Race


class RaceRepository:
    """Repository for working with Race in the database"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, race_id: int) -> Optional[Race]:
        """Getting a race for ID."""
        return self.db.query(Race).filter(Race.id == race_id).first()

    def get_by_name(self, name: str) -> Optional[Race]:
        """Obtaining a race by name."""
        return self.db.query(Race).filter(Race.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Race]:
        """Obtaining all races with pagination."""
        return self.db.query(Race).offset(skip).limit(limit).all()

    def count_all(self) -> int:
        """Calculation of the total number of races."""
        return self.db.query(Race).count()

    def create(self, race_data: dict) -> Race:
        """Creating a new race."""
        race = Race(**race_data)
        self.db.add(race)
        self.db.commit()
        self.db.refresh(race)
        return race

    def update(self, race: Race, update_data: dict) -> Race:
        """Update the existing race."""
        for field, value in update_data.items():
            setattr(race, field, value)

        self.db.commit()
        self.db.refresh(race)
        return race

    def delete(self, race: Race) -> bool:
        """Removing the race."""
        self.db.delete(race)
        self.db.commit()
        return True

    def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Checking the existence of a race by name."""
        query = self.db.query(Race).filter(Race.name == name)
        if exclude_id:
            query = query.filter(Race.id != exclude_id)
        return query.first() is not None

    def get_by_rarity(self, rarity: str) -> list[Race]:
        """Obtaining races by rarity."""
        return self.db.query(Race).filter(Race.rarity == rarity).all()

    def get_playable_races(self) -> list[Race]:
        """Obtaining only playable races."""
        return self.db.query(Race).filter(Race.is_playable).all()
