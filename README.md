# brewery-app

> Brewery management application with AI assistance.
> **Status**: Phase 1 — Week 4 Complete | [View Learning Path](https://github.com/adriandelvalle/dev-ml-llm-ops)

---

## Purpose

This project serves as:

1. A practical vehicle for learning DevOps, MLOps, and LLMOps best practices.
2. A future operational tool for our artisanal brewery.

---

## Quick Start

### Full stack (Docker — recommended)

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

# 4. Cloudflare Tunnel (external access, free quick tunnel)
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
| Mock Data | ✅ Complete | In-memory data until PostgreSQL |
| pytest suite | ✅ Complete | 14 tests — recipes and batches |
| Docker (API) | ✅ Complete | Containerized + restart unless-stopped |
| Service Persistence | ✅ Complete | Auto-starts after server reboot |
| Docker Networks | ✅ Complete | brewery-network connecting all containers |
| Nginx Reverse Proxy | ✅ Complete | Routes /static and /api/* + /health |
| Static Files Serving | ✅ Complete | Tres Tigris content cards via volume mount |
| Cloudflare Tunnel | ✅ Complete | Quick tunnel — external HTTPS access, no port forwarding |
| AI Integration | ✅ Ready | OpenCode free tier (cloud-first, see ADR-0003) |
| Custom domain | ⏳ Deferred | Until real content justifies `trestigris.beer` purchase |
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
│   │   ├── api/v1/                 # recipes.py, batches.py
│   │   ├── models/                 # recipe.py, batch.py, fermentation.py
│   │   └── core/mock_data.py       # In-memory data (replaced by DB in Week 5)
│   ├── tests/                      # conftest.py, test_recipes.py, test_batches.py
│   ├── Dockerfile                  # Production image (python:3.12-slim)
│   ├── .dockerignore
│   ├── requirements.txt            # Production dependencies only
│   └── requirements-dev.txt        # Dev dependencies (-r requirements.txt + extras)
├── nginx/
│   ├── Dockerfile                  # nginx:alpine + custom config
│   └── nginx.conf                  # Reverse proxy + static serving rules
├── static/
│   └── tres_tigris_hojas_v2.html   # Instagram/WhatsApp content card (volume-mounted)
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
jotasrv
    └── brewery-cloudflared
            ↓ Docker network "brewery-network"
        brewery-nginx :80
            ├── /static/  → tres_tigris_hojas_v2.html (volume, read-only)
            └── /, /api/* → brewery-api:8000 (reverse proxy)
                    ↓
                FastAPI + Pydantic + mock data
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
| Reverse Proxy | Nginx (alpine) |
| External Access | Cloudflare Tunnel (quick tunnel) |
| AI / LLM | OpenCode CLI free cloud tier + Ollama (local, batch) |
| Database | PostgreSQL + SQLAlchemy 2 + Alembic (Week 5) |
| Secrets (pre-Vault) | python-dotenv + .env (Week 5) |
| CI/CD | GitHub Actions (Week 8) |
| Secrets | HashiCorp Vault (Week 7) |

---

## Backlog — Future Features

- **Member registration form** — legal/RGPD-compliant data capture, quota type
  (monthly/yearly), renewal date logic. Deferred to Week 5 (needs real DB persistence).
- **Admin panel with login** — JPG export tools, member management, batch status.
  Not user-database vs LDAP question — a simple `users` table with bcrypt-hashed
  passwords and role (`admin`/`socio`) is sufficient at this scale; LDAP is for
  corporate-scale SSO across many apps, not needed here.
- **Member area** — membership status, batch history, upcoming events.
- **Custom domain `trestigris.beer`** — when there's real content to justify it.

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
> Last updated: 2026-06-19
