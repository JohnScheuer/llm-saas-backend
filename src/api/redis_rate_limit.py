import os
import time
import redis
from fastapi import HTTPException

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

WINDOW_SECONDS = 60  # 1 minuto


def rate_limit_key(api_key: str):
    return f"rate_limit:{api_key}"


def check_rate_limit(api_key: str, limit: int):
    """
    Sliding window rate limiting using Redis.
    """

    key = rate_limit_key(api_key)
    now = int(time.time())

    pipe = redis_client.pipeline()

    # ✅ Remove registros antigos
    pipe.zremrangebyscore(key, 0, now - WINDOW_SECONDS)

    # ✅ Conta quantos restam
    pipe.zcard(key)

    # ✅ Adiciona novo request
    pipe.zadd(key, {str(now): now})

    # ✅ Define expiração automática
    pipe.expire(key, WINDOW_SECONDS)

    results = pipe.execute()

    current_count = results[1]

    if current_count >= limit:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

    remaining = limit - current_count - 1

    reset_time = now + WINDOW_SECONDS

    return {
        "limit": limit,
        "remaining": max(remaining, 0),
        "reset": reset_time
    }
