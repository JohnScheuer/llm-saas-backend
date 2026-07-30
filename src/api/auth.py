from fastapi import Header, HTTPException
from decimal import Decimal

from .metrics import metrics_store
from .redis_rate_limit import check_rate_limit as redis_check_rate_limit
from .db import SessionLocal
from .sql_billing import (
    get_monthly_usage,
    get_monthly_credit
)

API_KEYS = {
    "dev-key-123": {
        "plan": "free",
        "rate_limit_per_minute": 100,
        "monthly_credit_usd": 0.001
    },
    "pro-key-456": {
        "plan": "pro",
        "rate_limit_per_minute": 200,
        "monthly_credit_usd": 1.0
    }
}


def verify_api_key(authorization: str = Header(None)):

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid API key")

    api_key = authorization.split(" ")[1]

    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return api_key


def check_credit_limit(api_key: str):

    db = SessionLocal()

    base_credit = Decimal(str(API_KEYS[api_key]["monthly_credit_usd"]))
    extra_credit = get_monthly_credit(db, api_key)
    total_usage = get_monthly_usage(db, api_key)

    total_credit = base_credit + extra_credit

    db.close()

    if total_usage >= total_credit:
        raise HTTPException(
            status_code=402,
            detail="Monthly credit limit exceeded"
        )


def check_rate_limit(api_key: str):

    limit = API_KEYS[api_key]["rate_limit_per_minute"]

    try:
        rate_data = redis_check_rate_limit(api_key, limit)
        return rate_data
    except HTTPException as e:
        if e.status_code == 429:
            metrics_store.record_rate_limited(api_key)
        raise e
