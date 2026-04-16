def test_list_recipes_returns_two_recipes(client):
    """El mock tiene 2 recetas por defecto."""
    response = client.get("/api/v1/recipes/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_recipe_by_id(client):
    """Debe devolver la receta con id=1."""
    response = client.get("/api/v1/recipes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Asturian Pale Ale"
    assert data["style"] == "APA"


def test_get_recipe_not_found(client):
    """Un id que no existe debe devolver 404."""
    response = client.get("/api/v1/recipes/999")
    assert response.status_code == 404


def test_create_recipe_success(client):
    """Una receta válida debe crearse con id=3 y created_at generado."""
    payload = {
        "name": "Gijon Stout",
        "style": "STOUT",
        "batch_size_liters": 50,
        "target_og": 1.060,
        "target_fg": 1.014,
        "target_ibu": 40,
        "target_abv": 6.0,
        "notes": "Stout de invierno"
    }
    response = client.post("/api/v1/recipes/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 3
    assert data["name"] == "Gijon Stout"
    assert "created_at" in data


def test_create_recipe_invalid_style(client):
    """Un estilo que no existe en el Enum debe devolver 422."""
    payload = {
        "name": "Test",
        "style": "INVENTADA",
        "batch_size_liters": 50,
        "target_og": 1.050,
        "target_fg": 1.010
    }
    response = client.post("/api/v1/recipes/", json=payload)
    assert response.status_code == 422


def test_create_recipe_missing_fields(client):
    """Campos obligatorios ausentes deben devolver 422."""
    response = client.post("/api/v1/recipes/", json={"name": "Solo nombre"})
    assert response.status_code == 422


def test_create_recipe_increments_id(client):
    """Crear dos recetas debe generar ids correlativos."""
    payload = {
        "name": "Primera",
        "style": "IPA",
        "batch_size_liters": 50,
        "target_og": 1.055,
        "target_fg": 1.011
    }
    r1 = client.post("/api/v1/recipes/", json=payload)
    payload["name"] = "Segunda"
    r2 = client.post("/api/v1/recipes/", json=payload)
    assert r1.json()["id"] == 3
    assert r2.json()["id"] == 4
