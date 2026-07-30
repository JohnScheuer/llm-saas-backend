# Agent Tooling Runtime

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)]
[![FastAPI](https://img.shields.io/badge/FastAPI-Production%20Ready-009688.svg)]
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)]
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)]
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)]
[![LLM](https://img.shields.io/badge/OpenAI-Compatible-orange.svg)]
[![SaaS](https://img.shields.io/badge/SaaS-Billing%20Enabled-purple.svg)]

Production-ready LLM backend with SaaS billing, distributed rate limiting, SQL financial integrity, and OpenAI-compatible API.

Author: João Felipe De Souza  
Year: 2026  

========================================
PROJECT OVERVIEW
========================================

Agent Tooling Runtime is a full-stack backend architecture designed for building scalable AI SaaS platforms.

It provides:

- OpenAI-compatible Chat API
- Tool calling execution layer
- Async multi-step agent runtime
- Sliding-window Redis rate limiting
- SQL-based financial ledger with Decimal precision
- Monthly SaaS billing model
- Credit top-up system
- Stripe webhook simulation
- Prometheus metrics
- Admin dashboard
- Dockerized production deployment

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
  +-- PostgreSQL (Billing + History)
  |
  +-- LLM Runtime (HuggingFace)
  |
  +-- Tool Execution Layer

========================================
CORE FEATURES
========================================

LLM Runtime
- Async agent loop
- Tool execution system
- Structured usage tracking

Rate Limiting
- Redis sliding window
- Multi-worker safe
- Per-key configuration
- Rate limit headers

Financial Layer
- PostgreSQL persistent ledger
- Decimal financial precision
- Immutable usage events
- Immutable credit events
- Monthly billing cycle
- Hard credit cap (HTTP 402)
- Soft credit warning threshold

SaaS Model
- Free and Pro plans
- Monthly credit allocation
- Extra credit top-up
- Stripe webhook simulation
- Admin credit management

Observability
- Prometheus metrics endpoint
- Per-key usage tracking
- Latency metrics

Admin Tools
- HTML Dashboard
- Billing history endpoint
- Secure admin endpoint

========================================
DOCUMENTATION
========================================

Design Document  
See design.md  

Project Summary  
See summary.txt  

License  
See LICENSE  

========================================
QUICK START (DOCKER)
========================================

Build and run:

docker compose up --build

API available at:

http://127.0.0.1:8000

Admin Dashboard:

http://127.0.0.1:8000/admin/dashboard

========================================
PRODUCTION READINESS
========================================

- PostgreSQL persistent storage
- Redis distributed rate limiting
- Gunicorn multi-worker
- Docker Compose orchestration
- Audit-ready financial records
- Extensible SaaS architecture

========================================
ROADMAP
========================================

Planned Enhancements:

- Stripe signature verification
- Invoice generation
- Export CSV financial reports
- Multi-tier plans
- Alembic migrations
- PostgreSQL clustering
- Kubernetes deployment
- Enterprise monitoring stack

========================================
VISION
========================================

Agent Tooling Runtime is built as a foundation for AI-powered SaaS products.

The system prioritizes:

- Financial correctness
- Production stability
- Multi-tenant architecture
- Observability
- Extensibility
- Secure-by-design implementation

========================================
END
========================================

