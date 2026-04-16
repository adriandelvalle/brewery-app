from fastapi import APIRouter, HTTPException
from src.models.recipe import RecipeCreate, RecipeResponse
from src.core import mock_data
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=list[RecipeResponse])
def list_recipes():
    """Devuelve todas las recetas."""
    return list(mock_data.RECIPES.values())


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int):
    """Devuelve una receta por ID."""
    if recipe_id not in mock_data.RECIPES:
        raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} not found")
    return mock_data.RECIPES[recipe_id]


@router.post("/", response_model=RecipeResponse, status_code=201)
def create_recipe(recipe: RecipeCreate):
    """Crea una nueva receta."""
    new_recipe = RecipeResponse(
        id=mock_data.next_recipe_id,
        created_at=datetime.now().isoformat(),
        **recipe.model_dump()
    )
    mock_data.RECIPES[mock_data.next_recipe_id] = new_recipe
    mock_data.next_recipe_id += 1
    return new_recipe
