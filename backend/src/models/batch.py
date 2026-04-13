from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class BatchStatus(str, Enum):
    PLANNED = "planned"
    BREWING = "brewing"
    FERMENTING = "fermenting"
    CONDITIONING = "conditioning"
    BOTTLED = "bottled"
    READY = "ready"


class BatchBase(BaseModel):
    """Campos comunes a todos los modelos de Batch."""
    recipe_id: int
    brew_date: date
    brewer: str = Field(..., min_length=2, max_length=50)
    water_volume_liters: float = Field(..., gt=0, le=100)
    notes: Optional[str] = Field(None, max_length=1000)


class BatchCreate(BatchBase):
    """Lo que recibe la API al crear un lote."""
    pass


class BatchMeasurements(BaseModel):
    """Mediciones tomadas durante el proceso. Opcionales porque se añaden en fases."""
    pre_boil_og: Optional[float] = Field(None, description="Densidad pre-hervido")
    pre_boil_ph: Optional[float] = Field(None, ge=0, le=14)
    post_boil_og: Optional[float] = Field(None, description="Densidad post-hervido")
    post_boil_ph: Optional[float] = Field(None, ge=0, le=14)
    fermentor_volume_liters: Optional[float] = Field(None, gt=0, le=60)
    final_og: Optional[float] = Field(None, description="Densidad original al entrar fermentador")
    final_fg: Optional[float] = Field(None, description="Densidad final tras fermentacion")
    actual_abv: Optional[float] = Field(None, ge=0, le=20)


class BatchResponse(BatchBase):
    """Lo que devuelve la API."""
    id: int
    status: BatchStatus
    measurements: BatchMeasurements
    created_at: str
