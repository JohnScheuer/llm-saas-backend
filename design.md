# Agent Tooling Runtime
Design Document
Author: João Felipe De Souza
Year: 2026

========================================
1. OVERVIEW
========================================

Agent Tooling Runtime is a production-ready backend system designed to:

- Serve LLM responses through an OpenAI-compatible API
- Execute tool/function calls
- Enforce SaaS-grade billing
- Apply distributed rate limiting
- Provide financial integrity with Decimal arithmetic
- Support multi-tenant API keys
- Run in a containerized production environment

The system is built for real-world SaaS deployment and is structured for scalability and financial correctness.

========================================
2. HIGH-LEVEL ARCHITECTURE
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
  +-- HuggingFace LLM Runtime
  |
  +-- Tool Execution Layer

All services run inside Docker Compose:

- billing-api
- billing-postgres
- billing-redis

========================================
3. CORE COMPONENTS
========================================

3.1 API Layer

- OpenAI-compatible endpoint: /v1/chat/completions
- Streaming support
- Structured usage reporting
- Rate limit headers
- Admin endpoints
- Billing endpoints
- Metrics endpoint (Prometheus format)

3.2 LLM Runtime

- HuggingFace integration
- Async agent loop
- Multi-step reasoning
- Tool execution
- Structured usage tracking

3.3 Tool Execution Layer

- Registry-based tool system
- Async and sync execution
- Argument validation
- Alias normalization
- Structured error handling

========================================
4. RATE LIMITING DESIGN
========================================

Technology: Redis
Strategy: Sliding Window via Sorted Set (ZSET)

For each API key:
- A Redis key stores timestamps of recent requests
- Old timestamps are removed (window expiration)
- Cardinality is checked against limit
- Request rejected if over limit

Headers returned:
- X-RateLimit-Limit
- X-RateLimit-Remaining
- X-RateLimit-Reset

Properties:
- Multi-worker safe
- Multi-container safe
- Atomic operations via Redis pipeline

========================================
5. BILLING ARCHITECTURE
========================================

Technology: PostgreSQL
Precision: Decimal (Numeric(18,6))

Tables:

usage_events
- id
- api_key
- tokens
- cost_usd (Decimal)
- created_at

credit_events
- id
- api_key
- amount_usd (Decimal)
- created_at

Design Principles:
- Immutable financial records
- Event-based accounting
- Monthly billing cycle
- Credit top-ups stored as separate events
- Audit-friendly structure

========================================
6. BILLING MODEL
========================================

Each API key has:

- plan
- monthly_credit_usd
- rate_limit_per_minute

Billing cycle:
- Monthly
- Computed via SQL aggregation using created_at

Hard Cap:
If total_usage >= total_credit:
    Return HTTP 402

Soft Warning:
If remaining_credit <= 10%:
    Return header:
        X-Credit-Warning: true
        X-Remaining-Credit: <value>

Credit Extension:
Admin endpoint allows adding extra credit per billing cycle.

========================================
7. STRIPE WEBHOOK SIMULATION
========================================

Endpoint:
POST /webhook/stripe

Simulated event:
type: invoice.paid

Payload includes:
- amount_paid (in cents)
- metadata.api_key

Behavior:
- Convert cents to USD
- Insert CreditEvent into database
- Credit becomes immediately available

Prepared for future:
- Stripe signature verification
- Real webhook validation
- Subscription model

========================================
8. ADMIN DASHBOARD
========================================

Endpoint:
GET /admin/dashboard

Features:
- Lists API keys
- Shows plan
- Shows usage (USD)
- Shows total credit
- Shows remaining balance

Access:
Protected via X-Admin-Secret header

========================================
9. OBSERVABILITY
========================================

Prometheus endpoint:
GET /metrics

Metrics exposed:
- successful_requests_total
- rate_limited_requests_total
- total_tokens
- avg_latency_ms

Per-key metrics supported.

========================================
10. SECURITY MODEL
========================================

Authentication:
- API key via Authorization: Bearer header

Admin Access:
- X-Admin-Secret header

Rate limiting:
- Redis-based
- Prevents abuse

Financial Integrity:
- Decimal arithmetic
- SQL-based immutable event storage

========================================
11. CONTAINERIZATION
========================================

Docker Compose services:

- billing-api (Gunicorn + FastAPI)
- billing-postgres
- billing-redis

Characteristics:
- Multi-worker support
- Persistent volume for PostgreSQL
- Isolated Docker network
- Production-ready configuration

========================================
12. SCALABILITY
========================================

Horizontally scalable:
- Multiple API containers
- Shared Redis
- Shared PostgreSQL

Stateless API layer:
- All state externalized (Redis + Postgres)

========================================
13. EXTENSIBILITY
========================================

Prepared for:

- Stripe real integration
- Invoice generation
- Multi-plan tiers
- Enterprise features
- Kubernetes deployment
- PostgreSQL clustering
- Multi-model routing
- Advanced analytics

========================================
14. DESIGN PRINCIPLES
========================================

- Separation of concerns
- Financial correctness first
- Production-ready from day one
- Observability built-in
- Multi-tenant by design
- Extensible architecture
- Docker-native
- SaaS-first mindset

========================================
END OF DOCUMENT
========================================

