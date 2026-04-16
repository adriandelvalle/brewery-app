import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core import mock_data


@pytest.fixture(autouse=True)
def reset_mock_data():
    """
    Resetea los datos en memoria antes de cada test.
    Sin esto, un test que crea una receta afectaría al siguiente.
    """
    mock_data.RECIPES.clear()
    mock_data.RECIPES.update({
        1: mock_data.RECIPES_DEFAULT[1],
        2: mock_data.RECIPES_DEFAULT[2],
    })
    mock_data.BATCHES.clear()
    mock_data.BATCHES.update({
        1: mock_data.BATCHES_DEFAULT[1],
    })
    mock_data.next_recipe_id = 3
    mock_data.next_batch_id = 2


@pytest.fixture
def client():
    """Cliente HTTP de pruebas. No necesita el servidor corriendo."""
    return TestClient(app)
