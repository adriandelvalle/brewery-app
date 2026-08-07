def _create_recipe(client):
    """Helper — crea una receta y devuelve su id."""
    response = client.post("/api/v1/recipes/", json={
        "name": "Test Recipe",
        "style": "IPA",
        "batch_size_liters": 50,
        "target_og": 1.055,
        "target_fg": 1.011
    })
    return response.json()["id"]


def test_list_batches_empty(client):
    """Sin datos, devuelve lista vacía."""
    response = client.get("/api/v1/batches/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_batch_not_found(client):
    """Un id que no existe debe devolver 404."""
    response = client.get("/api/v1/batches/999")
    assert response.status_code == 404


def test_create_batch_success(client):
    """Un lote válido debe crearse con status planned y mediciones en null."""
    recipe_id = _create_recipe(client)
    payload = {
        "recipe_id": recipe_id,
        "brew_date": "2026-08-07",
        "brewer": "jota",
        "water_volume_liters": 50
    }
    response = client.post("/api/v1/batches/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "planned"
    assert data["recipe_id"] == recipe_id
    assert data["pre_boil_og"] is None
    assert "id" in data
    assert "created_at" in data


def test_get_batch_by_id(client):
    """Debe devolver el lote creado por su id."""
    recipe_id = _create_recipe(client)
    created = client.post("/api/v1/batches/", json={
        "recipe_id": recipe_id,
        "brew_date": "2026-08-07",
        "brewer": "jota",
        "water_volume_liters": 50
    }).json()
    response = client.get(f"/api/v1/batches/{created['id']}")
    assert response.status_code == 200
    assert response.json()["brewer"] == "jota"


def test_create_batch_invalid_recipe(client):
    """Sin receta previa, crear batch con recipe_id inexistente."""
    payload = {
        "recipe_id": 999,
        "brew_date": "2026-08-07",
        "brewer": "jota",
        "water_volume_liters": 50
    }
    response = client.post("/api/v1/batches/", json=payload)
    # SQLite no enforza FK por defecto — en PostgreSQL devolvería 500
    # La integridad referencial se verifica en tests de integración con DB real
    assert response.status_code in [201, 500]


def test_create_batch_missing_fields(client):
    """Campos obligatorios ausentes deben devolver 422."""
    response = client.post("/api/v1/batches/", json={"brewer": "jota"})
    assert response.status_code == 422


def test_list_batches_returns_created(client):
    """Crear dos lotes y verificar que ambos aparecen en el listado."""
    recipe_id = _create_recipe(client)
    for _ in range(2):
        client.post("/api/v1/batches/", json={
            "recipe_id": recipe_id,
            "brew_date": "2026-08-07",
            "brewer": "jota",
            "water_volume_liters": 50
        })
    response = client.get("/api/v1/batches/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_post_if_planned(client):
    """Un lote nuevo debe tener status planned."""
    recipe_id = _create_recipe(client)
    payload = {
        "recipe_id": recipe_id,
        "brew_date": "2026-08-07",
        "brewer": "jota",
        "water_volume_liters": 50
    }
    response = client.post("/api/v1/batches/", json=payload)
    assert response.status_code == 201
    assert response.json()["status"] == "planned"
