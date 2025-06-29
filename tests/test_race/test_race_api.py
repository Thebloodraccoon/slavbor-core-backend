def test_get_all_races_success(client, test_race):
    """Test successful retrieval of all races"""
    response = client.get("/races?page=1&size=5")

    assert response.status_code == 200
    data = response.json()
    assert "races" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["size"] == 5
    assert len(data["races"]) == 1


def test_get_all_races_empty_db(client):
    """Test successful retrieval from empty database"""
    response = client.get("/races")

    assert response.status_code == 200
    data = response.json()
    assert "races" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["size"] == 10
    assert len(data["races"]) == 0


def test_get_playable_races_success(client, create_race):
    """Test getting only playable races"""
    create_race(name="Playable Race", is_playable=True)
    create_race(name="Non-Playable Race", is_playable=False)

    response = client.get("/races/playable")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Playable Race"
    assert data[0]["is_playable"] is True


def test_get_playable_races_empty(client):
    """Test getting playable races when none exist"""
    response = client.get("/races/playable")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_get_races_by_rarity_success(client, create_race):
    """Test getting races by rarity"""
    create_race(name="Common Race", rarity="обычная")
    create_race(name="Rare Race", rarity="редкая")

    response = client.get("/races/by-rarity/обычная")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Common Race"
    assert data[0]["rarity"] == "обычная"


def test_get_races_by_rarity_empty(client):
    """Test getting races by rarity when none exist"""
    response = client.get("/races/by-rarity/редкая")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_get_race_by_id_success(client, test_race):
    """Test getting a specific race by ID"""
    response = client.get(f"/races/{test_race.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_race.id
    assert data["name"] == test_race.name
    assert data["description"] == test_race.description


def test_get_race_by_id_not_found(client):
    """Test getting a race that doesn't exist"""
    response = client.get("/races/999")

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["error"]["detail"]


def test_create_race_success(client):
    """Test creating a new race"""
    race_data = {
        "name": "New Test Race",
        "description": "A new test race",
        "size": "Средний",
        "special_traits": "Special abilities",
        "is_playable": True,
        "rarity": "обычная",
    }

    response = client.post("/races/", json=race_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == race_data["name"]
    assert data["description"] == race_data["description"]
    assert data["size"] == race_data["size"]
    assert data["is_playable"] == race_data["is_playable"]


def test_create_race_invalid_data(client):
    """Test creating a race with invalid data"""
    race_data = {"name": "", "size": "InvalidSize", "rarity": "invalid_rarity"}

    response = client.post("/races/", json=race_data)

    assert response.status_code == 422


def test_create_race_duplicate_name(client, test_race):
    """Test creating a race with duplicate name"""
    race_data = {
        "name": test_race.name,
        "description": "Another description",
        "size": "Большой",
        "is_playable": False,
    }

    response = client.post("/races/", json=race_data)

    assert response.status_code == 400
    data = response.json()
    assert "already exists" in data["error"]["detail"]


def test_update_race_post_success(client, test_race):
    """Test full update of a race using POST"""
    update_data = {
        "name": "Updated Race Name",
        "description": "Updated description",
        "size": "Большой",
        "special_traits": "Updated traits",
        "is_playable": False,
        "rarity": "редкая",
    }

    response = client.post(f"/races/{test_race.id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["size"] == update_data["size"]
    assert data["is_playable"] == update_data["is_playable"]


def test_update_race_post_not_found(client):
    """Test updating a race that doesn't exist using POST"""
    update_data = {"name": "Non-existent Race", "description": "This won't work"}

    response = client.post("/races/999", json=update_data)

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["error"]["detail"]


def test_update_race_post_duplicate_name(client, create_race):
    """Test updating a race with duplicate name using POST"""
    race1 = create_race(name="Race 1")
    race2 = create_race(name="Race 2")

    update_data = {"name": race1.name, "description": "Updated description"}

    response = client.post(f"/races/{race2.id}", json=update_data)

    assert response.status_code == 400
    data = response.json()
    assert "already exists" in data["error"]["detail"]


def test_update_race_patch_success(client, test_race):
    """Test partial update of a race using PATCH"""
    update_data = {"name": "Partially Updated Race", "is_playable": False}

    response = client.patch(f"/races/{test_race.id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["is_playable"] == update_data["is_playable"]
    assert data["description"] == test_race.description


def test_update_race_patch_not_found(client):
    """Test partial update of a race that doesn't exist"""
    update_data = {"name": "Won't work"}

    response = client.patch("/races/999", json=update_data)

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["error"]["detail"]


def test_update_race_patch_duplicate_name(client, create_race):
    """Test partial update of a race with duplicate name"""
    race1 = create_race(name="Race 1")
    race2 = create_race(name="Race 2")

    update_data = {"name": race1.name}

    response = client.patch(f"/races/{race2.id}", json=update_data)

    assert response.status_code == 400
    data = response.json()
    assert "already exists" in data["error"]["detail"]


def test_toggle_race_playable_status_success(client, test_race):
    """Test toggling playable status of a race"""
    original_status = test_race.is_playable

    response = client.patch(f"/races/{test_race.id}/toggle-playable")

    assert response.status_code == 200
    data = response.json()
    assert data["is_playable"] != original_status


def test_toggle_race_playable_status_not_found(client):
    """Test toggling playable status of a race that doesn't exist"""
    response = client.patch("/races/999/toggle-playable")

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["error"]["detail"]


def test_delete_race_success(client, test_race):
    """Test deleting a race"""
    response = client.delete(f"/races/{test_race.id}")

    assert response.status_code == 204

    get_response = client.get(f"/races/{test_race.id}")
    assert get_response.status_code == 404


def test_delete_race_not_found(client):
    """Test deleting a race that doesn't exist"""
    response = client.delete("/races/999")

    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["error"]["detail"]


def test_get_races_by_rarity_invalid(client):
    """Test getting races by invalid rarity"""
    response = client.get("/races/by-rarity/invalid_rarity")

    assert response.status_code == 400
    data = response.json()
    detail = data["error"]["detail"]

    assert "The unacceptable value of rarity" in detail["message"]
    assert detail["received"] == "invalid_rarity"
    assert "очень редкая" in detail["allowed_values"]
    assert "редкая" in detail["examples"]
    assert data["error"]["type"] == "RaceRarityException"
