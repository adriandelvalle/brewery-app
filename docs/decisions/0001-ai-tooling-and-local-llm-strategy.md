# ADR-0001: AI Tooling & Local LLM Strategy

## Status
Superseded by ADR-0003

## Context
We need an AI coding assistant that runs 100% locally on our ACEMAGIC hardware (AMD APU, 32GB RAM), costs nothing, and respects privacy. We evaluated OpenCode, Aider, and various LLM models (Qwen2.5 vs Qwen3).

## Decision
1. **Tool**: OpenCode CLI. Chosen for its native TUI, automatic Ollama detection, and flexible provider support.
2. **Model**: `qwen3:8b` via Ollama. Qwen3 supports stable tool calling for file creation/editing, which Qwen2.5-Coder lacked in our initial tests. 8B size balances performance (~5.2GB RAM) with capability.
3. **Environment**: Python `venv` is mandatory due to Ubuntu 24.04+ PEP 668 restrictions on system-wide pip installs.

## Consequences
- ✅ Fully offline workflow; no API keys or subscription costs.
- ✅ Reliable file generation via tool calling.
- ⚠️ RAM is shared between OS and GPU; models >14B cause swapping.
- ⚠️ Qwen3 has less coding-specific documentation than Qwen2.5; mitigated by explicit prompt engineering.
