from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class BeerStyle(str, Enum):
    IPA = "IPA"
    LAGER = "LAGER"
    NEIPA = "NEIPA"
    APA = "APA"
    STOUT = "STOUT"
    PORTER = "PORTER"
    WHEAT = "WHEAT"


class RecipeBase(BaseModel):
    """Campos comunes a todos los modelos de Recipe."""
    name: str = Field(..., min_length=2, max_length=100)
    style: BeerStyle
    batch_size_liters: float = Field(..., gt=0, le=100)
    target_og: float = Field(..., description="Original Gravity objetivo (ej: 1.052)")
    target_fg: float = Field(..., description="Final Gravity objetivo (ej: 1.010)")
    target_ibu: Optional[int] = Field(None, ge=0, le=120, description="Amargor en IBUs")
    target_abv: Optional[float] = Field(None, ge=0, le=20, description="Alcohol estimado %")
    notes: Optional[str] = Field(None, max_length=1000)


class RecipeCreate(RecipeBase):
    """Lo que recibe la API al crear una receta. Hereda todo de RecipeBase."""
    pass


class RecipeResponse(RecipeBase):
    """Lo que devuelve la API. Añade campos generados por el sistema."""
    id: int
    created_at: str
