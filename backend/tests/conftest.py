import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.db.base import Base
from src.db.session import get_db

# Base de datos SQLite en memoria — solo para tests
SQLITE_URL = "sqlite+aiosqlite://"

engine_test = create_async_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

AsyncSessionTest = sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False
)


async def override_get_db():
    """Sustituye get_db en tests — usa SQLite en memoria en lugar de PostgreSQL."""
    async with AsyncSessionTest() as session:
        yield session


@pytest.fixture(autouse=True)
async def setup_database():
    """Crea las tablas antes de cada test y las elimina después."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def client():
    """Cliente de test con get_db sobreescrito para usar SQLite."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
