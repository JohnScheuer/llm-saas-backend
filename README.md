# LLM SaaS Backend

![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7+-DC382D?style=flat-square&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=flat-square)

**Complete LLM-as-a-Service backend.** Sell AI access with tool calling, billing, and enterprise-grade infrastructure.

Everything needed to launch an AI SaaS product: OpenAI-compatible API, tool calling execution, credit-based billing, Stripe integration, distributed rate limiting, financial audit trail, and Prometheus observability.

> This is not just a tool-calling framework. This is production-ready LLM SaaS infrastructure.

---

## Why This Exists

Most LLM tutorials show you how to **call** an API.

This project shows how to **sell** it.

It implements all the infrastructure that separates a demo from a real AI business:

- Billing accuracy (Decimal precision, no float errors)
- Distributed rate limits (multi-worker safe)
- Financial integrity (transactional audit log)
- Credit enforcement (fail-closed with HTTP 402)
- SaaS tier model (Free + Pro with monthly renewal)
- Admin tooling (dashboard + user management)
- Audit trail (immutable event logs)

---

## Stack

### Backend
- **FastAPI + Gunicorn** — production async server with multi-worker support
- **HuggingFace Transformers** — LLM runtime (Qwen2 compatible)
- **Async agent loop** — multi-step tool calling with non-blocking I/O

### Infrastructure
- **Redis** — distributed sliding-window rate limiting (ZSET-based)
- **PostgreSQL** — transactional billing ledger + audit log
- **Docker Compose** — single-command deployment
- **Prometheus** — observability endpoint

---

## Architecture

Request flow:

- Client sends HTTP request
- FastAPI (Gunicorn Workers) receives it
- Redis validates rate limit
- PostgreSQL validates credits and logs transaction
- LLM Runtime (HuggingFace / Qwen2) processes the request
- Tool Execution Layer runs any registered Python functions

**Docker Network Components:**
- api — FastAPI application container
- postgres — PostgreSQL 15 with financial schema
- redis — Redis 7 for rate limiting cache

---

## Product Features

### For End Users
- OpenAI-compatible /v1/chat/completions API
- Tool calling support (register any Python function via @tool decorator)
- Multi-step agent workflows
- Streaming responses (SSE)

### For SaaS Operators
- Credit-based billing with monthly renewal
- Free tier and Pro tier model
- Hard limit enforcement (HTTP 402 Payment Required)
- Soft warnings at configurable usage thresholds
- Stripe webhook integration for automated top-ups
- Admin dashboard for user management
- Full transaction ledger (audit-ready SQL)

### For Reliability
- Distributed rate limiting (multi-worker safe via Redis)
- Decimal precision for financial operations (no float rounding errors)
- Immutable event logs (append-only)
- Prometheus metrics endpoint
- Containerized deployment (works locally and in production)

---

## Quick Start

Requirements: Docker and Docker Compose installed.

Run everything with a single command:

    docker compose up --build

Available endpoints:

| Endpoint | URL |
|----------|-----|
| API | http://127.0.0.1:8000 |
| Admin Dashboard | http://127.0.0.1:8000/admin/dashboard |
| Metrics | http://127.0.0.1:8000/metrics |
| API Docs | http://127.0.0.1:8000/docs |

---

## Design Highlights

### Financial Precision
All monetary values use Python Decimal (never float). This prevents rounding errors that compound over millions of transactions.

### Distributed Rate Limiting
Uses Redis ZSET (sorted set) for sliding-window algorithm. Multi-worker safe: multiple Gunicorn workers or multiple API instances share the same rate limit state without race conditions.

### Fail-Closed Enforcement
When credits run out, the API returns HTTP 402 Payment Required. No silent failures, no accidental usage without payment.

### Audit-Ready Ledger
Every LLM call is logged with:
- Input tokens, output tokens, total cost
- Model used, tool calls executed
- Timestamp, request ID, user ID
- Result status (success, error, rate-limited)

This satisfies audit requirements for financial regulations.

### Rate Limit Headers
Standard headers returned to clients:
- X-RateLimit-Limit: max requests in window
- X-RateLimit-Remaining: requests left
- X-RateLimit-Reset: seconds until window resets

---

## Related Projects

- **fused-int4-gemm-sm75:** Custom INT4 CUDA kernels with Qwen2 integration
- **distributed-inference-engine:** Multi-GPU LLM scaling (TP + PP)
- **rag-inference-stack:** Knowledge-augmented generation pipeline
- **custom-llm-serving-engine:** OpenAI-compatible serving runtime

---

## Documentation

- **System Architecture:** See design.md
- **Executive Overview:** See summary.txt
- **License:** See LICENSE

---

## Roadmap

Prepared for:
- Stripe production integration (currently uses webhook simulation)
- PostgreSQL horizontal scaling (read replicas)
- Kubernetes deployment (Helm chart)
- Enterprise SaaS use cases (multi-tenancy, SSO)

---

## License

MIT — João Felipe De Souza, 2026
