from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.batch import BatchCreate, BatchResponse, BatchStatus
from src.db.session import get_db
from src.db.models.batch import Batch

router = APIRouter()


@router.get("/", response_model=list[BatchResponse])
async def list_batches(db: AsyncSession = Depends(get_db)):
    """Devuelve todos los lotes."""
    result = await db.execute(select(Batch))
    return result.scalars().all()


@router.get("/{batch_id}", response_model=BatchResponse)
async def get_batch(batch_id: int, db: AsyncSession = Depends(get_db)):
    """Devuelve un lote por ID."""
    result = await db.execute(select(Batch).where(Batch.id == batch_id))
    batch = result.scalar_one_or_none()
    if not batch:
        raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found")
    return batch


@router.post("/", response_model=BatchResponse, status_code=201)
async def create_batch(batch: BatchCreate, db: AsyncSession = Depends(get_db)):
    """Crea un nuevo lote."""
    new_batch = Batch(
        **batch.model_dump(),
        status=BatchStatus.PLANNED
    )
    db.add(new_batch)
    await db.commit()
    await db.refresh(new_batch)
    return new_batch
