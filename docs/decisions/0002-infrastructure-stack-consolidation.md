# ADR-0002: Infrastructure Stack Consolidation

## Status
Accepted

## Context
We need a local, open-source infrastructure stack that:
1. Replicates cloud patterns (S3, secrets management, virtualization) without vendor lock-in.
2. Scales from learning labs to production-like environments.
3. Minimizes tool-switching overhead during the 12-15 month learning path.

## Decision
- **Object Storage**: MinIO (S3-compatible API). Enables seamless migration to AWS S3, GCS, or Azure Blob later.
- **Secrets Management**: HashiCorp Vault (not Vaultwarden for app secrets). Industry standard, supports dynamic secrets, audit logs, and K8s integration.
- **Virtualization**: Proxmox VE (not OpenStack). Sufficient for local clusters, K8s labs, and migration testing. Lower learning curve.
- **Orchestration**: Docker Compose → Kubernetes (k3s). Progressive complexity.

## Consequences
- ✅ Single learning curve: tools chosen now remain valid in later phases.
- ✅ Portfolio demonstrates production-grade patterns, not just tutorials.
- ✅ Local hardware (32GB RAM) can run full stack via containers.
- ⚠️ Vault has initial setup complexity (unseal, storage backend). Mitigated by Docker Compose templates.
- ⚠️ Proxmox requires bare-metal install. Mitigated by dedicating ACEMAGIC as lab server.