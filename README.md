# brewery-app

> Brewery management application with AI assistance.<br>
> **Status**: Phase 1 (Week 2 Complete) | [View Learning Path](https://github.com/adriandelvalle/dev-ml-llm-ops)

---

## Purpose
This project serves as:
1. A practical vehicle for learning DevOps, MLOps, and LLMOps best practices.
2. A future operational tool for our artisanal brewery.

## Quick Start
```bash
# 1. Setup environment
cd backend
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run server
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access: http://localhost:8000/health or http://localhost:8000/docs

---

## Current Status
| Component | Status | Notes |
| :--- | :--- | :--- |
Project Structure | ✅ Ready | Backend, docs, scripts organized
Security Audit | ✅ Ready | audit-permissions.sh implemented
Version Control | ✅ Ready | Git + Conventional Commits
Backend API | ✅ Implemented | FastAPI scaffold + /health endpoint
Database | ⏳ Planned | PostgreSQL + SQLAlchemy (Week 3)
AI Integration | ✅ Ready | OpenCode + Ollama (Qwen3:8b)

---

## Architecture

``` 
brewery-app/
├── backend/
│   ├── src/
│   │   ├── api/          # FastAPI endpoints
│   │   ├── core/         # Config, security, logging
│   │   └── models/       # SQLAlchemy models
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile        # Planned
├── docs/decisions/       # Architecture Decision Records
├── scripts/              # Automation tools
└── README.md
```

---

## Tech Stack
| Category | Technology |
| :--- | :--- |
| Language | Python 3.12+|
| Framework | FastAPI (ASGI) + Uvicorn |
| AI / LLM | OpenCode CLI + Ollama + Qwen3:8b|
| Database | PostgreSQL (Planned) |
| Infrastructure | 	Docker, Kubernetes (k3s) |
| CI/CD | GitHub Actions|

## Learning Context
This repository contains the application code.
For detailed learning notes, progress tracking, and cheatsheets, visit the [Main Portfolio Repository](https://github.com/adriandelvalle/dev-ml-llm-ops).

---
> Philosophy: Learning-first, users-later. 100% free stack. Depth > speed.<br>
> Last updated: 2026-04-06
