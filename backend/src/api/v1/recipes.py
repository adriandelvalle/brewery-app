from fastapi import APIRouter, HTTPException
from src.models.recipe import RecipeCreate, RecipeResponse
from src.core.mock_data import RECIPES, next_recipe_id
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=list[RecipeResponse])
def list_recipes():
    """Devuelve todas las recetas."""
    return list(RECIPES.values())


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int):
    """Devuelve una receta por ID."""
    if recipe_id not in RECIPES:
        raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} not found")
    return RECIPES[recipe_id]


@router.post("/", response_model=RecipeResponse, status_code=201)
def create_recipe(recipe: RecipeCreate):
    """Crea una nueva receta."""
    global next_recipe_id
    new_recipe = RecipeResponse(
        id=next_recipe_id,
        created_at=datetime.now().isoformat(),
        **recipe.model_dump()
    )
    RECIPES[next_recipe_id] = new_recipe
    next_recipe_id += 1
    return new_recipe
