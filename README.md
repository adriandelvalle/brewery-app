# brewery-app

> Brewery management application with AI assistance.
> **Status**: Phase 1 (Scaffold) | [View Learning Path](../portfolio)

---

## Purpose
This project serves as:
1. A practical vehicle for learning DevOps, MLOps, and LLMOps best practices.
2. A future operational tool for our artisanal brewery.

## Current Status
- Project Structure: Ready (Backend, docs, scripts organized)
- Security Audit: Ready (audit-permissions.sh implemented)
- Version Control: Ready (Git with Conventional Commits)
- Backend API: Planned (FastAPI, coming Week 2)
- Database: Planned (PostgreSQL, coming Week 2)
- AI Integration: Planned (Local LLMs via Ollama, coming Phase 4/5)

## Architecture
brewery-app/
├── backend/
│   ├── src/
│   │   ├── api/          # FastAPI endpoints
│   │   ├── core/         # Config, security, logging
│   │   └── models/       # SQLAlchemy models
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── docs/decisions/       # Architecture Decision Records
├── scripts/              # Automation tools
└── README.md

## Tech Stack
- Language: Python 3.11+
- Framework: FastAPI (ASGI)
- AI / LLM: Ollama + Qwen2.5-Coder (Local, 100% Free)
- Database: PostgreSQL
- Infrastructure: Docker, Kubernetes (k3s)
- CI/CD: GitHub Actions
- Monitoring: Prometheus + Grafana (Planned)

## Learning Context
This repository contains the application code.
For detailed learning notes, progress tracking, and cheatsheets, visit the [Main Portfolio Repository](../portfolio).

---
> Philosophy: Learning-first, users-later. 100% free stack. Depth > speed.
> Last updated: 2026-04-06
