def test_list_batches_returns_one_batch(client):
    """El mock tiene 1 lote por defecto."""
    response = client.get("/api/v1/batches/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_batch_by_id(client):
    """Debe devolver el lote con id=1 en estado fermenting."""
    response = client.get("/api/v1/batches/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "fermenting"
    assert data["brewer"] == "jota"


def test_get_batch_not_found(client):
    """Un id que no existe debe devolver 404."""
    response = client.get("/api/v1/batches/999")
    assert response.status_code == 404


def test_batch_has_measurements(client):
    """El lote debe incluir mediciones anidadas."""
    response = client.get("/api/v1/batches/1")
    data = response.json()
    assert "measurements" in data
    assert data["measurements"]["pre_boil_og"] == 1.048
    assert data["measurements"]["final_fg"] is None


def test_create_batch_success(client):
    """Un lote válido debe crearse con status=planned y measurements vacías."""
    payload = {
        "recipe_id": 1,
        "brew_date": "2026-04-20",
        "brewer": "jota",
        "water_volume_liters": 50
    }
    response = client.post("/api/v1/batches/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 2
    assert data["status"] == "planned"
    assert data["measurements"]["pre_boil_og"] is None


def test_create_batch_missing_fields(client):
    """Campos obligatorios ausentes deben devolver 422."""
    response = client.post("/api/v1/batches/", json={"brewer": "jota"})
    assert response.status_code == 422

def test_post_if_planned(client):
    payload = {
        "recipe_id": 1,
        "brew_date": "2026-04-20",
        "brewer": "jota",
        "water_volume_liters": 50
    }
    response = client.post("/api/v1/batches/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "planned"
    assert data["recipe_id"] == 1
    assert data["brew_date"] == "2026-04-20"
    assert data["brewer"] == "jota"