import pytest

from app.exceptions.race_exceptions import (RaceAlreadyExistsException,
                                            RaceNotFoundException)
from app.races.schemas import RaceCreate, RaceUpdate
from app.races.services import RaceService


def test_get_race_by_id_success(db_session, test_race):
    """Test getting race by ID successfully"""
    service = RaceService(db_session)

    result = service.get_race_by_id(test_race.id)

    assert result.id == test_race.id
    assert result.name == test_race.name


def test_get_race_by_id_not_found(db_session):
    """Test getting race by non-existent ID raises exception"""
    service = RaceService(db_session)

    with pytest.raises(RaceNotFoundException):
        service.get_race_by_id(999)


def test_get_race_by_name_success(db_session, test_race):
    """Test getting race by name successfully"""
    service = RaceService(db_session)

    result = service.get_race_by_name(test_race.name)

    assert result.id == test_race.id
    assert result.name == test_race.name


def test_get_race_by_name_not_found(db_session):
    """Test getting race by non-existent name raises exception"""
    service = RaceService(db_session)

    with pytest.raises(RaceNotFoundException):
        service.get_race_by_name("Non-existent Race")


def test_get_all_races(db_session, create_race):
    """Test getting all races with pagination parameters"""
    service = RaceService(db_session)
    for i in range(5):
        create_race(name=f"Race {i}")

    result = service.get_all_races(skip=1, limit=3)

    assert len(result) == 3


def test_create_race_success(db_session):
    """Test creating a new race successfully"""
    service = RaceService(db_session)
    race_data = RaceCreate(
        name="New Race",
        description="Test description",
        size="Средний",
        is_playable=True,
        rarity="обычная",
    )

    result = service.create_race(race_data)

    assert result.name == race_data.name
    assert result.description == race_data.description


def test_create_race_duplicate_name(db_session, test_race):
    """Test creating race with duplicate name raises exception"""
    service = RaceService(db_session)
    race_data = RaceCreate(name=test_race.name, is_playable=True)

    with pytest.raises(RaceAlreadyExistsException):
        service.create_race(race_data)


def test_update_race_success(db_session, test_race):
    """Test updating race successfully"""
    service = RaceService(db_session)
    update_data = RaceUpdate(name="Updated Name", description="Updated description")

    result = service.update_race(test_race.id, update_data)

    assert result.name == update_data.name
    assert result.description == update_data.description


def test_update_race_not_found(db_session):
    """Test updating non-existent race raises exception"""
    service = RaceService(db_session)
    update_data = RaceUpdate(name="Won't work")

    with pytest.raises(RaceNotFoundException):
        service.update_race(999, update_data)


def test_update_race_duplicate_name(db_session, create_race):
    """Test updating race with duplicate name raises exception"""
    service = RaceService(db_session)
    race1 = create_race(name="Race 1")
    race2 = create_race(name="Race 2")
    update_data = RaceUpdate(name=race1.name)

    with pytest.raises(RaceAlreadyExistsException):
        service.update_race(race2.id, update_data)


def test_delete_race_success(db_session, test_race):
    """Test deleting race successfully"""
    service = RaceService(db_session)
    race_id = test_race.id

    result = service.delete_race(race_id)

    assert result is True
    with pytest.raises(RaceNotFoundException):
        service.get_race_by_id(race_id)


def test_delete_race_not_found(db_session):
    """Test deleting non-existent race raises exception"""
    service = RaceService(db_session)

    with pytest.raises(RaceNotFoundException):
        service.delete_race(999)


def test_get_playable_races(db_session, create_race):
    """Test getting only playable races"""
    service = RaceService(db_session)
    create_race(name="Playable", is_playable=True)
    create_race(name="Non-Playable", is_playable=False)

    result = service.get_playable_races()

    assert len(result) == 1
    assert result[0].name == "Playable"


def test_get_races_by_rarity(db_session, create_race):
    """Test getting races by rarity"""
    service = RaceService(db_session)
    create_race(name="Common", rarity="обычная")
    create_race(name="Rare", rarity="редкая")

    result = service.get_races_by_rarity("обычная")

    assert len(result) == 1
    assert result[0].name == "Common"


def test_toggle_playable_status(db_session, test_race):
    """Test toggling playable status"""
    service = RaceService(db_session)
    original_status = test_race.is_playable

    result = service.toggle_playable_status(test_race.id)

    assert result.is_playable != original_status


def test_toggle_playable_status_not_found(db_session):
    """Test toggling playable status of non-existent race"""
    service = RaceService(db_session)

    with pytest.raises(RaceNotFoundException):
        service.toggle_playable_status(999)


def test_get_races_with_pagination(db_session, create_race):
    """Test getting races with pagination"""
    service = RaceService(db_session)
    for i in range(5):
        create_race(name=f"Race {i}")

    result = service.get_races_with_pagination(page=1, size=3)

    assert result.total == 5
    assert result.page == 1
    assert result.size == 3
    assert len(result.races) == 3


def test_race_update_empty_validation():
    """Test that RaceUpdate requires at least one field"""
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        RaceUpdate()

    assert "At least one field should be provided for update" in str(exc_info.value)
