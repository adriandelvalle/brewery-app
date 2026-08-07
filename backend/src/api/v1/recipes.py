from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.recipe import RecipeCreate, RecipeResponse
from src.db.session import get_db
from src.db.models.recipe import Recipe

router = APIRouter()


@router.get("/", response_model=list[RecipeResponse])
async def list_recipes(db: AsyncSession = Depends(get_db)):
    """Devuelve todas las recetas."""
    result = await db.execute(select(Recipe))
    return result.scalars().all()


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    """Devuelve una receta por ID."""
    result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise HTTPException(status_code=404, detail=f"Recipe {recipe_id} not found")
    return recipe


@router.post("/", response_model=RecipeResponse, status_code=201)
async def create_recipe(recipe: RecipeCreate, db: AsyncSession = Depends(get_db)):
    """Crea una nueva receta."""
    new_recipe = Recipe(**recipe.model_dump())
    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    return new_recipe
