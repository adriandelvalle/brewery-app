# brewery-app

> Brewery management application with AI assistance.
> **Status**: Phase 2 — Week 5 In Progress (PostgreSQL + Docker Compose + SQLAlchemy) | [View Learning Path](https://github.com/adriandelvalle/dev-ml-llm-ops)

---

## Purpose

This project serves as:

1. A practical vehicle for learning DevOps, MLOps, and LLMOps best practices.
2. A future operational tool for our artisanal brewery.

---

## Quick Start

### Full stack (Docker Compose — recommended)

```bash
cd ~/projects/brewery-app

# Copy .env.example and fill in your values
cp .env.example .env

# Start everything
docker compose up -d

# Apply database migrations
docker exec brewery-api alembic upgrade head

# Check status
docker compose ps
```

### [OLD] Full stack without Docker Compose (pre-Week 5 reference)

> This was the original method before Docker Compose was introduced.
> Kept here as reference to understand what Compose replaces.

```bash
# 1. Network
docker network create brewery-network

# 2. API
cd backend
docker build -t brewery-app:v0.1 .
docker run -d --name brewery-api --network brewery-network -p 8000:8000 --restart unless-stopped brewery-app:v0.1

# 3. Nginx (reverse proxy + static files)
cd ../nginx
docker build -t brewery-nginx:v0.2 .
docker run -d --name brewery-nginx --network brewery-network -p 80:80 \
  -v ~/projects/brewery-app/static:/usr/share/nginx/html/static:ro \
  --restart unless-stopped brewery-nginx:v0.2

# 4. Cloudflare Tunnel
docker run -d --name brewery-cloudflared --network brewery-network --restart unless-stopped \
  cloudflare/cloudflared:latest tunnel --no-autoupdate --url http://brewery-nginx:80
docker logs brewery-cloudflared   # shows the public URL
```

### Local development (no Docker)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Access:
- Local network: `http://192.168.0.21/health` (via Nginx, port 80)
- Static content: `http://192.168.0.21/static/tres_tigris_hojas_v2.html`
- External (temporary URL, changes on restart): see `docker logs brewery-cloudflared`

### Run tests

```bash
cd backend
source venv/bin/activate
pytest -v
```

### Access psql

```bash
psql-brew   # alias configured in ~/.bashrc
```

---

## Current Status

| Component | Status | Notes |
| --- | --- | --- |
| Project Structure | ✅ Complete | backend/, nginx/, static/, docs/, scripts/ |
| Security Audit | ✅ Complete | audit-permissions.sh implemented |
| Version Control | ✅ Complete | Git + Conventional Commits + pre-commit |
| pre-commit + commitizen | ✅ Complete | Enforced on every commit |
| Backend API | ✅ Complete | FastAPI + /health endpoint |
| Pydantic Models | ✅ Complete | Recipe, Batch, FermentationSample |
| API v1 Endpoints | ✅ Complete | GET/POST recipes and batches |
| Mock Data | ✅ Complete | In-memory data — pending replacement with PostgreSQL |
| pytest suite | ✅ Complete | 14 tests — recipes and batches |
| Docker | ✅ Complete | All services via Docker Compose |
| Service Persistence | ✅ Complete | Auto-starts after server reboot |
| Docker Networks | ✅ Complete | brewery-network connecting all containers |
| Nginx Reverse Proxy | ✅ Complete | Routes /static and /api/* + /health |
| Static Files Serving | ✅ Complete | Tres Tigris content cards via volume mount |
| Cloudflare Tunnel | ✅ Complete | Quick tunnel — external HTTPS access, no port forwarding |
| Docker Compose | ✅ Complete | Full stack declared in single file |
| PostgreSQL | ✅ Complete | Running in Docker with persistent named volume |
| SQLAlchemy models | ✅ Complete | Recipe, Batch defined with relationships |
| Alembic migrations | ✅ Complete | First migration applied — tables created |
| AI Integration | ✅ Ready | OpenCode free tier (cloud-first, see ADR-0003) |
| Connect API to PostgreSQL | ⏳ Pending | Replace mock_data with real DB queries |
| FermentationSample DB model | ⏳ Pending | SQLAlchemy model + migration |
| Socio model | ⏳ Pending | RGPD fields, quota type, renewal logic |
| pytest with real DB | ⏳ Pending | Replace mock_data fixtures |
| Custom domain | ⏳ Deferred | Until real content justifies `trestigris.com` purchase |
| MinIO | ⏳ Planned | Week 6 |
| HashiCorp Vault | ⏳ Planned | Week 7 |

---

## API Endpoints

| Method | Route | Description | Status |
| --- | --- | --- | --- |
| GET | `/health` | Service health check | ✅ |
| GET | `/api/v1/recipes/` | List all recipes | ✅ (mock) |
| GET | `/api/v1/recipes/{id}` | Get recipe by ID | ✅ (mock) |
| POST | `/api/v1/recipes/` | Create new recipe | ✅ (mock) |
| GET | `/api/v1/batches/` | List all batches | ✅ (mock) |
| GET | `/api/v1/batches/{id}` | Get batch by ID | ✅ (mock) |
| POST | `/api/v1/batches/` | Create new batch | ✅ (mock) |
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
│   │   ├── api/v1/                 # recipes.py, batches.py
│   │   ├── models/                 # Pydantic: recipe.py, batch.py, fermentation.py
│   │   ├── core/mock_data.py       # In-memory data (pending replacement with PostgreSQL)
│   │   └── db/
│   │       ├── base.py             # DeclarativeBase
│   │       ├── session.py          # AsyncSession + get_db dependency
│   │       └── models/
│   │           ├── recipe.py       # SQLAlchemy Recipe model
│   │           └── batch.py        # SQLAlchemy Batch model
│   ├── alembic/                    # migrations
│   │   └── versions/
│   │       └── 653336fca96a_create_recipes_and_batches_tables.py
│   ├── alembic.ini
│   ├── tests/                      # conftest.py, test_recipes.py, test_batches.py
│   ├── Dockerfile                  # Production image (python:3.12-slim)
│   ├── .dockerignore
│   ├── requirements.txt            # Production dependencies only
│   └── requirements-dev.txt        # Dev dependencies (-r requirements.txt + extras)
├── nginx/
│   ├── Dockerfile                  # nginx:alpine + custom config
│   └── nginx.conf                  # Reverse proxy + static serving rules + charset utf-8
├── static/
│   └── tres_tigris_hojas_v2.html   # Instagram/WhatsApp content card (volume-mounted)
├── .env                            # gitignored — real credentials
├── .env.example                    # committed — credentials template
├── docker-compose.yml              # full stack declaration
├── .pre-commit-config.yaml
├── .cz.toml
├── docs/decisions/
├── scripts/
└── README.md
```

---

## Infrastructure Stack

```
Internet (anywhere — verified via mobile data)
        ↓ HTTPS automatic
Cloudflare (edge — quic protocol)
        ↓ encrypted outbound tunnel — no inbound ports, no exposed home IP
jotasrv — Docker Compose
    ├── brewery-cloudflared
    ├── brewery-nginx :80
    │   ├── /static/  → tres_tigris_hojas_v2.html (volume, read-only)
    │   └── /, /api/* → brewery-api:8000 (reverse proxy)
    ├── brewery-api :8000
    │       └── FastAPI + Pydantic + SQLAlchemy → mock_data (pending DB)
    └── brewery-db :5432 (internal only)
            └── PostgreSQL 16 — tables: recipes, batches, alembic_version
```

**Why Cloudflare Tunnel over port forwarding**: the server only makes an
outbound connection — never receives inbound traffic directly. No exposed
home IP, no open router ports, Cloudflare absorbs attacks before they
reach the server.

**Current limitation**: using a free Quick Tunnel — the public subdomain
(`*.trycloudflare.com`) changes on every container restart. A named tunnel
with a fixed subdomain requires a domain registered in Cloudflare —
deferred until there's real content to justify it.

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

**Foreign key behavior**: `ON DELETE RESTRICT` (default) — deleting a recipe
with existing batches is blocked. Soft delete planned for future releases.

---

## Tech Stack

| Category | Technology |
| --- | --- |
| Language | Python 3.12+ |
| Framework | FastAPI (ASGI) + Uvicorn |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2 (async) |
| Migrations | Alembic |
| Database | PostgreSQL 16 |
| Testing | pytest + httpx + pytest-asyncio |
| Code Quality | pre-commit + commitizen |
| Containerization | Docker Compose |
| Reverse Proxy | Nginx (alpine) |
| External Access | Cloudflare Tunnel (quick tunnel) |
| AI / LLM | OpenCode CLI free cloud tier + Ollama (local, batch) |
| Secrets (pre-Vault) | python-dotenv + .env + .env.example |
| CI/CD | GitHub Actions (Week 8) |
| Secrets Mgmt | HashiCorp Vault (Week 7) |

---

## Backlog — Future Features

- **Connect API to PostgreSQL** — replace `mock_data.py` with real SQLAlchemy queries. Next session.
- **Member registration form** — legal/RGPD-compliant data capture, quota type
  (monthly/yearly), renewal date logic. Week 5 continuation.
- **Admin panel with login** — JPG export tools, member management, batch status.
  Simple `users` table with bcrypt-hashed passwords and role (`admin`/`socio`) —
  no LDAP needed at this scale.
- **Member area** — membership status, batch history, upcoming events.
- **KB Tres Tigris** — Syncthing + jotasrv + Obsidian. Post-domain purchase.
- **Custom domain `trestigris.com`** — when there's real content to justify it.

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
> Last updated: 2026-07-15
