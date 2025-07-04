from typing import List

from sqlalchemy.orm import Session

from app.exceptions.race_exceptions import (RaceAlreadyExistsException,
                                            RaceNotFoundException)
from app.races.repository import RaceRepository
from app.races.schemas import (RaceCreate, RaceListResponse, RaceResponse,
                               RaceUpdate)


class RaceService:
    """Service for working with races"""

    def __init__(self, db: Session):
        self.repository = RaceRepository(db)

    def get_race_by_id(self, race_id: int) -> RaceResponse:
        """Obtaining a race by ID."""
        race = self.repository.get_by_id(race_id)
        if race is None:
            raise RaceNotFoundException(race_id)

        return RaceResponse.model_validate(race)

    def get_race_by_name(self, name: str) -> RaceResponse:
        """Obtaining a race by name."""
        race = self.repository.get_by_name(name)
        if race is None:
            raise RaceNotFoundException(f"Race with name '{name}' not found")  # type: ignore

        return RaceResponse.model_validate(race)

    def get_all_races(self, skip: int = 0, limit: int = 100) -> List[RaceResponse]:
        """Obtaining all races with pagination."""
        races = self.repository.get_all(skip=skip, limit=limit)
        return [RaceResponse.model_validate(race) for race in races]

    def get_races_with_pagination(
        self, page: int = 1, size: int = 10
    ) -> RaceListResponse:
        """Obtaining races with pagination and metadata."""
        skip = (page - 1) * size
        races = self.repository.get_all(skip=skip, limit=size)
        total = self.repository.count_all()

        race_responses = [RaceResponse.model_validate(race) for race in races]

        return RaceListResponse(races=race_responses, total=total, page=page, size=size)

    def create_race(self, race_data: RaceCreate) -> RaceResponse:
        """Creating a new race."""
        if self.repository.exists_by_name(race_data.name):
            raise RaceAlreadyExistsException(race_data.name)

        race_dict = race_data.model_dump()
        created_race = self.repository.create(race_dict)

        return RaceResponse.model_validate(created_race)

    def update_race(self, race_id: int, race_data: RaceUpdate) -> RaceResponse:
        """Update the existing race."""
        race = self.repository.get_by_id(race_id)
        if race is None:
            raise RaceNotFoundException(race_id)

        update_data = race_data.model_dump(exclude_unset=True)
        if "name" in update_data and update_data["name"] != race.name:
            if self.repository.exists_by_name(update_data["name"], exclude_id=race_id):
                raise RaceAlreadyExistsException(update_data["name"])

        updated_race = self.repository.update(race, update_data)

        return RaceResponse.model_validate(updated_race)

    def delete_race(self, race_id: int) -> bool:
        """Removing the race."""
        race = self.repository.get_by_id(race_id)
        if race is None:
            raise RaceNotFoundException(race_id)

        return self.repository.delete(race)

    def get_playable_races(self) -> List[RaceResponse]:
        """Obtaining only playable races."""
        races = self.repository.get_playable_races()
        return [RaceResponse.model_validate(race) for race in races]

    def toggle_playable_status(self, race_id: int) -> RaceResponse:
        """Switching the status of playing the race."""
        race = self.repository.get_by_id(race_id)
        if race is None:
            raise RaceNotFoundException(race_id)

        update_data = {"is_playable": not race.is_playable}
        updated_race = self.repository.update(race, update_data)

        return RaceResponse.model_validate(updated_race)
