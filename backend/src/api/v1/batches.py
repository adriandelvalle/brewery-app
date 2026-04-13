from fastapi import APIRouter, HTTPException
from src.models.batch import BatchCreate, BatchResponse, BatchStatus, BatchMeasurements
from src.core.mock_data import BATCHES, next_batch_id
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=list[BatchResponse])
def list_batches():
    """Devuelve todos los lotes."""
    return list(BATCHES.values())


@router.get("/{batch_id}", response_model=BatchResponse)
def get_batch(batch_id: int):
    """Devuelve un lote por ID."""
    if batch_id not in BATCHES:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found")
    return BATCHES[batch_id]


@router.post("/", response_model=BatchResponse, status_code=201)
def create_batch(batch: BatchCreate):
    """Crea un nuevo lote."""
    global next_batch_id
    new_batch = BatchResponse(
        id=next_batch_id,
        status=BatchStatus.PLANNED,
        measurements=BatchMeasurements(),
        created_at=datetime.now().isoformat(),
        **batch.model_dump()
    )
    BATCHES[next_batch_id] = new_batch
    next_batch_id += 1
    return new_batch
