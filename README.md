# LLM SaaS Backend

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)]
[![FastAPI](https://img.shields.io/badge/FastAPI-Production%20Ready-009688.svg)]
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)]
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)]
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)]
[![LLM](https://img.shields.io/badge/OpenAI-Compatible-orange.svg)]
[![SaaS](https://img.shields.io/badge/SaaS-Billing%20Enabled-purple.svg)]

Complete LLM-as-a-Service backend.  
Sell AI access with tool calling, billing, and enterprise-grade infrastructure.

Everything needed to launch an AI SaaS product:
- OpenAI-compatible API
- Tool calling execution
- Credit-based billing
- Stripe webhook integration
- Distributed rate limiting
- Financial audit ledger
- Admin dashboard

This is not just a tool-calling framework.  
This is production-ready LLM SaaS infrastructure.

========================================
STACK
========================================

Backend:
- FastAPI + Gunicorn (production async server)
- HuggingFace model runtime
- Async multi-step agent execution

Infrastructure:
- Redis (distributed sliding-window rate limiting)
- PostgreSQL (transactional billing + audit log)
- Docker Compose (single-command deployment)
- Prometheus (observability)

========================================
PRODUCT FEATURES
========================================

For End Users:
- OpenAI-compatible /v1/chat/completions API
- Tool calling support (register any Python function)
- Multi-step agent workflows
- Streaming responses

For SaaS Operators:
- Credit-based billing with monthly renewal
- Free tier + Pro tier model
- Hard limit enforcement (HTTP 402)
- Soft warnings at usage thresholds
- Stripe webhook integration for top-ups
- Admin dashboard for user management
- Full transaction ledger (audit-ready SQL)

For Reliability:
- Distributed rate limiting (multi-worker safe)
- Decimal precision for financial operations (no float errors)
- Immutable event logs
- Prometheus metrics endpoint
- Containerized deployment

========================================
ARCHITECTURE
========================================

Client
  |
  v
FastAPI (Gunicorn Workers)
  |
  +-- Redis (Rate Limiting)
  |
  +-- PostgreSQL (Billing Ledger)
  |
  +-- LLM Runtime (Tool Calling Agent)

Docker Network:
- api
- postgres
- redis

========================================
QUICK START
========================================

Run everything with:

docker compose up --build

Endpoints:
- API: http://127.0.0.1:8000
- Admin Dashboard: http://127.0.0.1:8000/admin/dashboard
- Metrics: http://127.0.0.1:8000/metrics

========================================
WHY THIS EXISTS
========================================

Most LLM tutorials show how to call an API.

This project shows how to sell it.

It implements all the infrastructure that separates a demo from a real AI business:
- Billing
- Rate limits
- Financial integrity
- Credit enforcement
- SaaS model
- Admin tooling
- Audit trail

========================================
DOCUMENTATION
========================================

System Architecture:
See design.md

Executive Overview:
See summary.txt

License:
See LICENSE

========================================
STATUS
========================================

Production-ready backend architecture.
Prepared for:
- Stripe production integration
- PostgreSQL scaling
- Kubernetes deployment
- Enterprise SaaS use

========================================
AUTHOR
========================================

João Felipe De Souza
2026

