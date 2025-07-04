from app.races.repository import RaceRepository


def test_get_by_id_success(db_session, test_race):
    """Test getting race by ID successfully"""
    repo = RaceRepository(db_session)

    result = repo.get_by_id(test_race.id)

    assert result is not None
    assert result.id == test_race.id
    assert result.name == test_race.name


def test_get_by_id_not_found(db_session):
    """Test getting race by non-existent ID"""
    repo = RaceRepository(db_session)

    result = repo.get_by_id(999)

    assert result is None


def test_get_by_name_success(db_session, test_race):
    """Test getting race by name successfully"""
    repo = RaceRepository(db_session)

    result = repo.get_by_name(test_race.name)

    assert result is not None
    assert result.name == test_race.name


def test_get_by_name_not_found(db_session):
    """Test getting race by non-existent name"""
    repo = RaceRepository(db_session)

    result = repo.get_by_name("Non-existent Race")

    assert result is None


def test_create_race(db_session):
    """Test creating a new race"""
    repo = RaceRepository(db_session)
    race_data = {
        "name": "New Race",
        "description": "Test description",
        "size": "Средний",
        "is_playable": True,
    }

    result = repo.create(race_data)

    assert result.id is not None
    assert result.name == race_data["name"]
    assert result.description == race_data["description"]


def test_update_race(db_session, test_race):
    """Test updating existing race"""
    repo = RaceRepository(db_session)
    update_data = {"name": "Updated Name", "description": "Updated description"}

    result = repo.update(test_race, update_data)

    assert result.name == update_data["name"]
    assert result.description == update_data["description"]


def test_delete_race(db_session, test_race):
    """Test deleting a race"""
    repo = RaceRepository(db_session)
    race_id = test_race.id

    result = repo.delete(test_race)

    assert result is True
    deleted_race = repo.get_by_id(race_id)
    assert deleted_race is None


def test_exists_by_name_true(db_session, test_race):
    """Test checking if race exists by name - exists"""
    repo = RaceRepository(db_session)

    result = repo.exists_by_name(test_race.name)

    assert result is True


def test_exists_by_name_false(db_session):
    """Test checking if race exists by name - doesn't exist"""
    repo = RaceRepository(db_session)

    result = repo.exists_by_name("Non-existent Race")

    assert result is False


def test_get_playable_races(db_session, create_race):
    """Test getting only playable races"""
    repo = RaceRepository(db_session)
    create_race(name="Playable", is_playable=True)
    create_race(name="Non-Playable", is_playable=False)

    result = repo.get_playable_races()

    assert len(result) == 1
    assert result[0].name == "Playable"
    assert result[0].is_playable is True


def test_count_all(db_session, create_race):
    """Test counting all races"""
    repo = RaceRepository(db_session)
    create_race(name="Race 1")
    create_race(name="Race 2")
    create_race(name="Race 3")

    result = repo.count_all()

    assert result == 3


def test_get_all_with_pagination(db_session, create_race):
    """Test getting all races with pagination"""
    repo = RaceRepository(db_session)
    for i in range(5):
        create_race(name=f"Race {i}")

    result = repo.get_all(skip=2, limit=2)

    assert len(result) == 2
