from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


class BatchStatus(str, Enum):
    PLANNED = "planned"
    BREWING = "brewing"
    FERMENTING = "fermenting"
    CONDITIONING = "conditioning"
    BOTTLED = "bottled"
    READY = "ready"


class BatchBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recipe_id: int
    brew_date: date
    brewer: str = Field(..., min_length=2, max_length=50)
    water_volume_liters: float = Field(..., gt=0, le=100)
    notes: Optional[str] = Field(None, max_length=1000)


class BatchCreate(BatchBase):
    pass


class BatchMeasurements(BaseModel):
    """Mantenido por compatibilidad — usado en mock_data y tests existentes."""
    pre_boil_og: Optional[float] = Field(None)
    pre_boil_ph: Optional[float] = Field(None, ge=0, le=14)
    post_boil_og: Optional[float] = Field(None)
    post_boil_ph: Optional[float] = Field(None, ge=0, le=14)
    fermentor_volume_liters: Optional[float] = Field(None, gt=0, le=60)
    final_og: Optional[float] = Field(None)
    final_fg: Optional[float] = Field(None)
    actual_abv: Optional[float] = Field(None, ge=0, le=20)


class BatchResponse(BatchBase):
    id: int
    status: BatchStatus
    pre_boil_og: Optional[float] = None
    pre_boil_ph: Optional[float] = None
    post_boil_og: Optional[float] = None
    post_boil_ph: Optional[float] = None
    fermentor_volume_liters: Optional[float] = None
    final_og: Optional[float] = None
    final_fg: Optional[float] = None
    actual_abv: Optional[float] = None
    created_at: datetime
