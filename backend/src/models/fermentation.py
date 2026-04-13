from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FermentationSampleBase(BaseModel):
    """Una medición tomada durante la fermentación."""
    batch_id: int
    gravity: float = Field(..., description="Densidad medida (ej: 1.020)")
    temperature_celsius: float = Field(..., ge=0, le=40)
    ph: Optional[float] = Field(None, ge=0, le=14)
    notes: Optional[str] = Field(None, max_length=500)


class FermentationSampleCreate(FermentationSampleBase):
    """Lo que recibe la API al registrar una muestra."""
    pass


class FermentationSampleResponse(FermentationSampleBase):
    """Lo que devuelve la API."""
    id: int
    sampled_at: datetime
