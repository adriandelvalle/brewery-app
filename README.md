# brewery-app

> Brewery management application with AI assistance.
> **Status**: Phase 1 — Week 3 Complete | [View Learning Path](https://github.com/adriandelvalle/dev-ml-llm-ops)

---

## Purpose

This project serves as:

1. A practical vehicle for learning DevOps, MLOps, and LLMOps best practices.
2. A future operational tool for our artisanal brewery.

---

## Quick Start

```bash
# 1. Setup environment
cd backend
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run server — always from backend/, not from project root
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
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
| AI Integration | ✅ Ready | OpenCode free tier (cloud-first, see ADR-0003) |
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
│   │   ├── main.py           # App entry point — registers routers only
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
│   ├── pytest.ini
│   ├── requirements.txt
│   └── Dockerfile                  # Planned Week 4
├── .pre-commit-config.yaml         # pre-commit hooks configuration
├── .cz.toml                        # commitizen configuration
├── docs/decisions/                 # Architecture Decision Records
├── scripts/                        # Automation tools
└── README.md
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

## Pydantic Patterns Used

**Create / Response separation** — the model that receives data is never the same
as the one that returns it. System-generated fields (`id`, `status`, `created_at`)
only appear in Response models.

**Model composition** — `BatchMeasurements` is a nested model inside `BatchResponse`
because measurements accumulate across different phases of the brewing process,
not all at creation time.

**Enums for domain vocabulary** — `BeerStyle` and `BatchStatus` ensure only valid
domain values are accepted. Invalid values are rejected automatically with a clear
error message listing accepted options.

---

## Testing Approach

**14 tests** covering:
- List endpoints return expected number of items
- GET by ID returns correct data
- GET by non-existent ID returns 404
- POST with valid data returns 201 with system-generated fields
- POST with invalid data returns 422
- State isolation between tests via `conftest.py` autouse fixture

Tests run without the server — `TestClient` talks directly to the FastAPI app in memory.

---

## Tech Stack

| Category | Technology |
| --- | --- |
| Language | Python 3.12+ |
| Framework | FastAPI (ASGI) + Uvicorn |
| Validation | Pydantic v2 |
| Testing | pytest + httpx + pytest-asyncio |
| Code Quality | pre-commit + commitizen |
| AI / LLM | OpenCode CLI free cloud tier + Ollama (local, batch) |
| Database | PostgreSQL + SQLAlchemy 2 + Alembic (Week 5) |
| Secrets (pre-Vault) | python-dotenv + .env (Week 5) |
| Infrastructure | Docker (Week 4), Kubernetes k3s (Phase 3) |
| CI/CD | GitHub Actions (Week 8) |
| Secrets | HashiCorp Vault (Week 7) |

---

## AI Strategy (Hybrid)

| Use Case | Infrastructure | Model |
| --- | --- | --- |
| Interactive development | Cloud (OpenCode) | free tier |
| Nightly automations / batch | Local (Ollama) | phi3:mini, llama3.2:3b |
| MLOps/LLMOps experiments | Local (Ollama) | Any experimental model |
| Production with sensitive data | Local + dedicated GPU* | Quantized model |

*Future: RTX 3060 12GB or similar.
Local inference tested with qwen2.5-coder:7b — 2–4 tok/s, 30–50s latency, not viable
for interactive development. See ADR-0001 (superseded) and ADR-0003.

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
> Last updated: 2026-04-17
