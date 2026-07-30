# Agent Tooling Runtime
License: MIT [Python] [FastAPI] [PostgreSQL] [Redis] [Docker] [LLM] [SaaS]

**Production-ready LLM backend with SaaS billing, distributed rate limiting, SQL financial integrity, and OpenAI-compatible API.**

Author: João Felipe De Souza  
Year: 2026

---

## PROJECT OVERVIEW
Agent Tooling Runtime is a full-stack backend architecture designed for building scalable AI SaaS platforms.

It provides:
- **OpenAI-compatible Chat API**
- **Tool calling execution layer**
- **Async multi-step agent runtime**
- **Sliding-window Redis rate limiting**
- **SQL-based financial ledger with Decimal precision**
- **Monthly SaaS billing model**
- **Credit top-up system**
- **Stripe webhook simulation**
- **Prometheus metrics**
- **Admin dashboard**
- **Dockerized production deployment**

---

## ARCHITECTURE
```text
Client 
  | 
  v 
FastAPI (Gunicorn Workers) 
  | 
  +-- Redis (Distributed Rate Limiting) 
  | 
  +-- PostgreSQL (Billing + Transaction History) 
  | 
  +-- LLM Runtime (HuggingFace / Qwen2) 
  | 
  +-- Tool Execution Layer (Registry-based)
```

---

## CORE FEATURES

### LLM Runtime
- Async agent loop for non-blocking I/O
- Tool execution system with alias normalization
- Structured usage tracking per request

### Rate Limiting
- Redis sliding window (ZSET) implementation
- Multi-worker and multi-instance safe
- Rate limit headers returned to client (Limit, Remaining, Reset)

### Financial Layer
- PostgreSQL persistent ledger
- **Decimal financial precision** (no float rounding risks)
- Immutable usage and credit event logs
- Hard credit cap (HTTP 402) and soft warning thresholds

### SaaS Model
- Free and Pro plan support
- Monthly credit allocation logic
- Stripe webhook simulation for automated top-ups

### Observability
- Prometheus metrics endpoint (`/metrics`)
- Per-key usage and latency tracking
- Full per-step JSON tracing

---

## QUICK START (DOCKER)

**Build and run:**
```bash
docker compose up --build
```

**Endpoints:**
- API: `http://127.0.0.1:8000`
- Admin Dashboard: `http://127.0.0.1:8000/admin/dashboard`
- Metrics: `http://127.0.0.1:8000/metrics`

---

## DOCUMENTATION
- **Architecture & Decisions:** See [design.md](design.md)
- **Technical Metrics:** See [summary.txt](summary.txt)
- **License:** See [LICENSE](LICENSE)

---

## PRODUCTION READINESS
- PostgreSQL persistent storage
- Redis distributed rate limiting
- Gunicorn multi-worker setup
- Docker Compose orchestration
- Audit-ready financial records

---

## VISION
Agent Tooling Runtime is built as a foundation for AI-powered SaaS products. The system prioritizes financial correctness, production stability, and multi-tenant observability.

---

## Related Projects
- [fused-int4-gemm-sm75](https://github.com/JohnScheuer/fused-int4-gemm-sm75): Custom CUDA kernels.
- [distributed-inference-engine](https://github.com/JohnScheuer/distributed-inference-engine): Scale-out LLM parallelism.
- [rag-inference-stack](https://github.com/JohnScheuer/rag-inference-stack): Knowledge-augmented generation.

---
[MIT](LICENSE) - Joao Felipe De Souza, 2026
