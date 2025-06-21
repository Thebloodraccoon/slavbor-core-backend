from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.races.schemas import (RaceCreate, RaceListResponse, RaceResponse,
                               RaceUpdate)
from app.races.services import RaceService
from app.races.utils import normalize_rarity
from app.settings import settings

router = APIRouter()


@router.get("/", response_model=List[RaceResponse])
def get_all_races(
    db: Session = Depends(settings.get_db),
):
    """Get all races with pagination."""
    return RaceService(db).get_all_races()


@router.get("/paginated", response_model=RaceListResponse)
def get_races_paginated(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    db: Session = Depends(settings.get_db),
):
    """Get races with pagination and metadata."""
    return RaceService(db).get_races_with_pagination(page=page, size=size)


@router.get("/playable", response_model=List[RaceResponse])
def get_playable_races(
    db: Session = Depends(settings.get_db),
):
    """Get only playable races."""
    return RaceService(db).get_playable_races()


@router.get("/by-rarity/{rarity}", response_model=List[RaceResponse])
def get_races_by_rarity(
    rarity: str,
    db: Session = Depends(settings.get_db),
):
    """Get races by rarity level."""
    normalized_rarity = normalize_rarity(rarity)
    return RaceService(db).get_races_by_rarity(normalized_rarity)


@router.get("/{race_id}", response_model=RaceResponse)
def get_race_by_id(
    race_id: int,
    db: Session = Depends(settings.get_db),
):
    """Get a specific race by ID."""
    return RaceService(db).get_race_by_id(race_id)


@router.post("/", response_model=RaceResponse, status_code=status.HTTP_201_CREATED)
def create_race(
    race: RaceCreate,
    db: Session = Depends(settings.get_db),
):
    """Create a new race."""
    return RaceService(db).create_race(race)


@router.post("/{race_id}", response_model=RaceResponse)
def update_race(
    race_id: int,
    race: RaceUpdate,
    db: Session = Depends(settings.get_db),
):
    """Full update of a race."""
    return RaceService(db).update_race(race_id, race)


@router.patch("/{race_id}", response_model=RaceResponse)
def update_race_patch(
    race_id: int,
    race: RaceUpdate,
    db: Session = Depends(settings.get_db),
):
    """Partial update of a race."""
    return RaceService(db).update_race(race_id, race)


@router.patch("/{race_id}/toggle-playable", response_model=RaceResponse)
def toggle_race_playable_status(
    race_id: int,
    db: Session = Depends(settings.get_db),
):
    """Toggle the playable status of a race."""
    return RaceService(db).toggle_playable_status(race_id)


@router.delete("/{race_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_race(
    race_id: int,
    db: Session = Depends(settings.get_db),
):
    """Delete a race."""
    RaceService(db).delete_race(race_id)
    return None
