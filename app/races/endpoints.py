from typing import List

from fastapi import APIRouter, Query
from starlette import status

from app.core.dependencies import AdminUserDep, FounderUserDep, RaceServiceDep
from app.races.schemas import (RaceCreate, RaceListResponse, RaceResponse,
                               RaceUpdate)
from app.races.utils import normalize_rarity

router = APIRouter()


@router.get("/", response_model=RaceListResponse)
def get_all_races(
    race_service: RaceServiceDep,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
):
    """Get all races with pagination."""
    return race_service.get_races_with_pagination(page=page, size=size)


@router.get("/playable", response_model=List[RaceResponse])
def get_playable_races(
    race_service: RaceServiceDep,
):
    """Get only playable races."""
    return race_service.get_playable_races()


@router.get("/by-rarity/{rarity}", response_model=List[RaceResponse])
def get_races_by_rarity(
    rarity: str,
    race_service: RaceServiceDep,
):
    """Get races by rarity level."""
    normalized_rarity = normalize_rarity(rarity)
    return race_service.get_races_by_rarity(normalized_rarity)


@router.get("/{race_id}", response_model=RaceResponse)
def get_race_by_id(
    race_id: int,
    race_service: RaceServiceDep,
):
    """Get a specific race by ID."""
    return race_service.get_race_by_id(race_id)


@router.post("/", response_model=RaceResponse, status_code=status.HTTP_201_CREATED)
def create_race(race: RaceCreate, race_service: RaceServiceDep, _: AdminUserDep):
    """Create a new race."""
    return race_service.create_race(race)


@router.post("/{race_id}", response_model=RaceResponse)
def update_race(
    race_id: int, race: RaceUpdate, race_service: RaceServiceDep, _: AdminUserDep
):
    """Full update of a race."""
    return race_service.update_race(race_id, race)


@router.patch("/{race_id}", response_model=RaceResponse)
def update_race_patch(
    race_id: int, race: RaceUpdate, race_service: RaceServiceDep, _: AdminUserDep
):
    """Partial update of a race."""
    return race_service.update_race(race_id, race)


@router.patch("/{race_id}/toggle-playable", response_model=RaceResponse)
def toggle_race_playable_status(
    race_id: int, race_service: RaceServiceDep, _: FounderUserDep
):
    """Toggle the playable status of a race."""
    return race_service.toggle_playable_status(race_id)


@router.delete("/{race_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_race(race_id: int, race_service: RaceServiceDep, _: FounderUserDep):
    """Delete a race."""
    race_service.delete_race(race_id)
    return None
