# brewery-app

> Brewery management application with AI assistance.
> **Status**: Phase 1 — Week 4 In Progress (Docker complete) | [View Learning Path](https://github.com/adriandelvalle/dev-ml-llm-ops)

---

## Purpose

This project serves as:

1. A practical vehicle for learning DevOps, MLOps, and LLMOps best practices.
2. A future operational tool for our artisanal brewery.

---

## Quick Start

### Local development

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker (recommended)

```bash
cd backend
docker build -t brewery-app:v0.1 .
docker run -d --name brewery-api -p 8000:8000 --restart unless-stopped brewery-app:v0.1
```

Access:
- Health check: `http://localhost:8000/health`
- Swagger UI: `http://localhost:8000/docs`
- Local network: `http://192.168.0.21:8000/docs`

### Run tests

```bash
cd backend
source venv/bin/activate
pytest -v
```

---

## Current Status

| Component | Status | Notes |
| --- | --- | --- |
| Project Structure | ✅ Complete | backend/, docs/, scripts/ organized |
| Security Audit | ✅ Complete | audit-permissions.sh implemented |
| Version Control | ✅ Complete | Git + Conventional Commits + pre-commit |
| pre-commit + commitizen | ✅ Complete | Enforced on every commit |
| Backend API | ✅ Complete | FastAPI + /health endpoint |
| Pydantic Models | ✅ Complete | Recipe, Batch, FermentationSample |
| API v1 Endpoints | ✅ Complete | GET/POST recipes and batches |
| Mock Data | ✅ Complete | In-memory data until PostgreSQL |
| pytest suite | ✅ Complete | 14 tests — recipes and batches |
| Docker | ✅ Complete | Containerized + restart unless-stopped |
| Service Persistence | ✅ Complete | Auto-starts after server reboot |
| AI Integration | ✅ Ready | OpenCode free tier (cloud-first, see ADR-0003) |
| Nginx + Cloudflare Tunnel | ⏳ Pending | Week 4 continuation |
| Static files (Tres Tigris) | ⏳ Pending | Week 4 continuation |
| Database | ⏳ Planned | PostgreSQL + SQLAlchemy + Alembic (Week 5) |

---

## API Endpoints

| Method | Route | Description | Status |
| --- | --- | --- | --- |
| GET | `/health` | Service health check | ✅ |
| GET | `/api/v1/recipes/` | List all recipes | ✅ |
| GET | `/api/v1/recipes/{id}` | Get recipe by ID | ✅ |
| POST | `/api/v1/recipes/` | Create new recipe | ✅ |
| GET | `/api/v1/batches/` | List all batches | ✅ |
| GET | `/api/v1/batches/{id}` | Get batch by ID | ✅ |
| POST | `/api/v1/batches/` | Create new batch | ✅ |
| GET | `/api/v1/batches/{id}/fermentation` | List fermentation samples | ⏳ |
| POST | `/api/v1/batches/{id}/fermentation` | Add fermentation sample | ⏳ |
| PATCH | `/api/v1/batches/{id}/measurements` | Update batch measurements | ⏳ |

---

## Architecture

```
brewery-app/
├── backend/
│   ├── src/
│   │   ├── main.py                 # App entry point — registers routers only
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── recipes.py      # Recipe endpoints
│   │   │       └── batches.py      # Batch endpoints
│   │   ├── models/
│   │   │   ├── recipe.py           # RecipeBase, RecipeCreate, RecipeResponse, BeerStyle
│   │   │   ├── batch.py            # BatchBase, BatchCreate, BatchResponse, BatchMeasurements
│   │   │   └── fermentation.py     # FermentationSample models
│   │   └── core/
│   │       └── mock_data.py        # In-memory data (replaced by DB in Week 5)
│   ├── tests/
│   │   ├── conftest.py             # TestClient fixture + autouse mock data reset
│   │   ├── test_recipes.py         # 7 tests for recipe endpoints
│   │   └── test_batches.py         # 7 tests for batch endpoints
│   ├── Dockerfile                  # Production image definition
│   ├── .dockerignore               # Excludes venv, tests, etc from image
│   ├── pytest.ini
│   ├── requirements.txt            # Production dependencies only
│   └── requirements-dev.txt        # Dev dependencies (-r requirements.txt + extras)
├── .pre-commit-config.yaml
├── .cz.toml
├── docs/decisions/
├── scripts/
└── README.md
```

---

## Docker Stack

```
jotasrv (Ubuntu 24.04)
└── Docker Engine 29.5.2
    └── brewery-api (brewery-app:v0.1)
        ├── restart: unless-stopped
        ├── port: 0.0.0.0:8000 → :8000
        └── uvicorn → FastAPI → Pydantic
```

**Planned (Week 4 continuation):**
```
jotasrv
└── Docker Engine
    ├── brewery-nginx    ← Nginx reverse proxy + HTTPS
    │   └── :80/:443 → brewery-api:8000
    └── brewery-api      ← FastAPI
```

---

## Domain Model

```
Recipe (1) ──── (N) Batch (1) ──── (N) FermentationSample
```

**Recipe** — the blueprint. Defines style, ingredients, targets (OG, FG, IBU, ABV).

**Batch** — a concrete execution of a recipe on a given date. Holds real process
measurements: pre/post boil gravity and pH, fermentor volume, final gravity.

**FermentationSample** — daily gravity/temperature/pH readings taken during
fermentation until gravity stabilizes (typically 5–7 days).

---

## Tech Stack

| Category | Technology |
| --- | --- |
| Language | Python 3.12+ |
| Framework | FastAPI (ASGI) + Uvicorn |
| Validation | Pydantic v2 |
| Testing | pytest + httpx + pytest-asyncio |
| Code Quality | pre-commit + commitizen |
| Containerization | Docker 29.5.2 |
| AI / LLM | OpenCode CLI free cloud tier + Ollama (local, batch) |
| Database | PostgreSQL + SQLAlchemy 2 + Alembic (Week 5) |
| Secrets (pre-Vault) | python-dotenv + .env (Week 5) |
| Reverse Proxy | Nginx (Week 4 continuation) |
| External Access | Cloudflare Tunnel (Week 4 continuation) |
| CI/CD | GitHub Actions (Week 8) |
| Secrets | HashiCorp Vault (Week 7) |

---

## Architecture Decision Records

| ADR | Title | Status |
| --- | --- | --- |
| [ADR-0001](docs/decisions/0001-ai-tooling-and-local-llm-strategy.md) | AI Tooling & Local LLM Strategy | Superseded by ADR-0003 |
| [ADR-0002](docs/decisions/0002-infrastructure-stack-consolidation.md) | Infrastructure Stack Consolidation | Accepted |
| [ADR-0003](docs/decisions/0003-ai-strategy.md) | AI Strategy (Hybrid Cloud-First) | Accepted |
| [ADR-0004](docs/decisions/0004-database-orm-migrations.md) | Database, ORM & Migrations | Accepted |

---

## Learning Context

This repository contains the application code.
For detailed learning notes, progress tracking, and cheatsheets, visit the
[Main Portfolio Repository](https://github.com/adriandelvalle/dev-ml-llm-ops).

---

> Philosophy: Learning-first, users-later. 100% free stack. Depth > speed.
> Last updated: 2026-05-27
