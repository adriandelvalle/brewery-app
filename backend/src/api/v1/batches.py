from fastapi import APIRouter, HTTPException
from src.models.batch import BatchCreate, BatchResponse, BatchStatus, BatchMeasurements
from src.core import mock_data
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=list[BatchResponse])
def list_batches():
    """Devuelve todos los lotes."""
    return list(mock_data.BATCHES.values())


@router.get("/{batch_id}", response_model=BatchResponse)
def get_batch(batch_id: int):
    """Devuelve un lote por ID."""
    if batch_id not in mock_data.BATCHES:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found")
    return mock_data.BATCHES[batch_id]


@router.post("/", response_model=BatchResponse, status_code=201)
def create_batch(batch: BatchCreate):
    """Crea un nuevo lote."""
    new_batch = BatchResponse(
        id=mock_data.next_batch_id,
        status=BatchStatus.PLANNED,
        measurements=BatchMeasurements(),
        created_at=datetime.now().isoformat(),
        **batch.model_dump()
    )
    mock_data.BATCHES[mock_data.next_batch_id] = new_batch
    mock_data.next_batch_id += 1
    return new_batch
