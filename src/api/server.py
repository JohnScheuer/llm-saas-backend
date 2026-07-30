import uuid
import time
from decimal import Decimal

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse

from ..agent_async import AsyncAgent
from ..clients.huggingface_client import HuggingFaceClient

from .metrics import metrics_store
from .auth import verify_api_key, check_rate_limit, check_credit_limit, API_KEYS
from .admin_auth import verify_admin
from .schemas import ChatCompletionRequest

from .db import Base, engine, SessionLocal
from .sql_billing import (
    record_usage,
    add_credit,
    get_monthly_usage,
    get_monthly_credit,
    get_monthly_history
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

llm = HuggingFaceClient(
    model_name="Qwen/Qwen2-0.5B-Instruct",
    temperature=0.0,
)

def calculator(expression: str):
    return eval(expression)


# =============================
# CHAT ENDPOINT
# =============================
@app.post("/v1/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    api_key: str = Depends(verify_api_key)
):

    check_credit_limit(api_key)
    rate_info = check_rate_limit(api_key)

    start_time = time.time()

    user_message = request.messages[-1].content

    agent = AsyncAgent(
        llm=llm,
        tools=[calculator],
        max_steps=5,
        enable_tracing=True
    )

    result, trace, usage = await agent.run(user_input=user_message)

    latency = time.time() - start_time

    metrics_store.record_success(api_key, latency, usage, trace)

    db = SessionLocal()
    record_usage(db, api_key, usage["total_tokens"])

    base_credit = Decimal(str(API_KEYS[api_key]["monthly_credit_usd"]))
    extra_credit = get_monthly_credit(db, api_key)

    total_credit = base_credit + extra_credit
    total_usage = get_monthly_usage(db, api_key)

    remaining = total_credit - total_usage

    db.close()

    if remaining < Decimal("0"):
        return JSONResponse(
            status_code=402,
            content={"detail": "Monthly credit limit exceeded"}
        )

    response = JSONResponse(content={
        "id": str(uuid.uuid4()),
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result
                },
                "finish_reason": "stop"
            }
        ],
        "usage": usage
    })

    response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
    response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])
    response.headers["X-RateLimit-Reset"] = str(rate_info["reset"])

    return response


# =============================
# BILLING API
# =============================
@app.get("/billing")
async def billing(api_key: str = Depends(verify_api_key)):

    db = SessionLocal()

    base_credit = Decimal(str(API_KEYS[api_key]["monthly_credit_usd"]))
    extra_credit = get_monthly_credit(db, api_key)

    total_credit = base_credit + extra_credit
    total_usage = get_monthly_usage(db, api_key)

    remaining = total_credit - total_usage
    if remaining < Decimal("0"):
        remaining = Decimal("0")

    response = {
        "api_key": api_key,
        "plan": API_KEYS[api_key]["plan"],
        "monthly_credit_usd": float(base_credit),
        "extra_credit_usd": float(extra_credit),
        "total_credit_usd": float(total_credit),
        "total_usage_usd_this_month": float(total_usage),
        "remaining_credit_usd": float(remaining)
    }

    db.close()
    return response


@app.get("/billing/history")
async def billing_history(api_key: str = Depends(verify_api_key)):

    db = SessionLocal()
    history = get_monthly_history(db, api_key)
    db.close()

    return {
        "api_key": api_key,
        "history": history
    }


# =============================
# ADMIN CREDIT
# =============================
@app.post("/admin/add-credit")
async def admin_add_credit(
    api_key: str,
    amount_usd: float,
    admin: bool = Depends(verify_admin)
):

    db = SessionLocal()
    add_credit(db, api_key, Decimal(str(amount_usd)))
    db.close()

    return {
        "message": "Credit added",
        "api_key": api_key,
        "added_amount_usd": amount_usd
    }


# =============================
# ADMIN DASHBOARD
# =============================
@app.get("/admin/dashboard")
async def admin_dashboard(admin: bool = Depends(verify_admin)):

    db = SessionLocal()

    html = "<h1>Admin Dashboard</h1>"
    html += "<table border='1' cellpadding='6'>"
    html += "<tr><th>API Key</th><th>Plan</th><th>Usage (USD)</th><th>Credit (USD)</th><th>Remaining (USD)</th></tr>"

    for key, config in API_KEYS.items():

        base_credit = Decimal(str(config["monthly_credit_usd"]))
        extra_credit = get_monthly_credit(db, key)
        total_credit = base_credit + extra_credit

        total_usage = get_monthly_usage(db, key)
        remaining = total_credit - total_usage
        if remaining < Decimal("0"):
            remaining = Decimal("0")

        html += f"<tr>"
        html += f"<td>{key}</td>"
        html += f"<td>{config['plan']}</td>"
        html += f"<td>{float(total_usage):.6f}</td>"
        html += f"<td>{float(total_credit):.6f}</td>"
        html += f"<td>{float(remaining):.6f}</td>"
        html += f"</tr>"

    html += "</table>"

    db.close()

    return HTMLResponse(content=html)


# =============================
# METRICS
# =============================
@app.get("/metrics")
async def prometheus_metrics():

    snapshot = metrics_store.snapshot()
    lines = []

    global_stats = snapshot["global"]

    lines.append("# TYPE llm_successful_requests_total counter")
    lines.append(f"llm_successful_requests_total {global_stats['successful_requests']}")

    lines.append("# TYPE llm_rate_limited_requests_total counter")
    lines.append(f"llm_rate_limited_requests_total {global_stats['rate_limited_requests']}")

    lines.append("# TYPE llm_total_tokens counter")
    lines.append(f"llm_total_tokens {global_stats['total_tokens']}")

    lines.append("# TYPE llm_avg_latency_ms gauge")
    lines.append(f"llm_avg_latency_ms {global_stats['avg_latency_ms']}")

    return PlainTextResponse("\n".join(lines))
