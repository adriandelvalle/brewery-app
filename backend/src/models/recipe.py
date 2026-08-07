from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime


class BeerStyle(str, Enum):
    IPA = "IPA"
    LAGER = "LAGER"
    NEIPA = "NEIPA"
    APA = "APA"
    STOUT = "STOUT"
    PORTER = "PORTER"
    WHEAT = "WHEAT"


class RecipeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=2, max_length=100)
    style: BeerStyle
    batch_size_liters: float = Field(..., gt=0, le=100)
    target_og: float = Field(..., description="Original Gravity objetivo (ej: 1.052)")
    target_fg: float = Field(..., description="Final Gravity objetivo (ej: 1.010)")
    target_ibu: Optional[int] = Field(None, ge=0, le=120, description="Amargor en IBUs")
    target_abv: Optional[float] = Field(None, ge=0, le=20, description="Alcohol estimado %")
    notes: Optional[str] = Field(None, max_length=1000)


class RecipeCreate(RecipeBase):
    pass


class RecipeResponse(RecipeBase):
    id: int
    created_at: datetime
