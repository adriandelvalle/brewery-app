from sqlalchemy import String, Numeric, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from src.db.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    style: Mapped[str] = mapped_column(String(20), nullable=False)
    batch_size_liters: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    target_og: Mapped[float] = mapped_column(Numeric(5, 3), nullable=False)
    target_fg: Mapped[float] = mapped_column(Numeric(5, 3), nullable=False)
    target_ibu: Mapped[int | None] = mapped_column(Integer, nullable=True)
    target_abv: Mapped[float | None] = mapped_column(Numeric(4, 2), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    batches: Mapped[list["Batch"]] = relationship("Batch", back_populates="recipe")
