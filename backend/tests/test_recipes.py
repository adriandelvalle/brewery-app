def test_list_recipes_empty(client):
    """Sin datos, devuelve lista vacía."""
    response = client.get("/api/v1/recipes/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_recipe_not_found(client):
    """Un id que no existe debe devolver 404."""
    response = client.get("/api/v1/recipes/999")
    assert response.status_code == 404


def test_create_recipe_success(client):
    """Una receta válida debe crearse con id generado y created_at."""
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
    assert data["name"] == "Gijon Stout"
    assert data["style"] == "STOUT"
    assert "id" in data
    assert "created_at" in data


def test_get_recipe_by_id(client):
    """Debe devolver la receta creada por su id."""
    payload = {
        "name": "Asturian Pale Ale",
        "style": "APA",
        "batch_size_liters": 50,
        "target_og": 1.052,
        "target_fg": 1.010
    }
    created = client.post("/api/v1/recipes/", json=payload).json()
    response = client.get(f"/api/v1/recipes/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Asturian Pale Ale"


def test_list_recipes_returns_created(client):
    """Crear dos recetas y verificar que ambas aparecen en el listado."""
    for name in ["Receta A", "Receta B"]:
        client.post("/api/v1/recipes/", json={
            "name": name,
            "style": "IPA",
            "batch_size_liters": 50,
            "target_og": 1.055,
            "target_fg": 1.011
        })
    response = client.get("/api/v1/recipes/")
    assert response.status_code == 200
    assert len(response.json()) == 2


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
