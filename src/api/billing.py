import os
import redis
from datetime import datetime
from decimal import Decimal

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

PRICE_PER_1K_TOKENS = Decimal("0.002")
WARNING_THRESHOLD_PERCENT = Decimal("0.10")


def current_cycle():
    now = datetime.utcnow()
    return now.strftime("%Y-%m")


def token_key(api_key: str):
    return f"billing:tokens:{api_key}:{current_cycle()}"


def credit_key(api_key: str):
    return f"billing:extra_credit:{api_key}:{current_cycle()}"


def add_usage(api_key: str, tokens: int):
    redis_client.incrby(token_key(api_key), tokens)


def get_usage(api_key: str):
    tokens = redis_client.get(token_key(api_key))
    return int(tokens) if tokens else 0


def add_credit(api_key: str, amount_usd: Decimal):
    redis_client.incrbyfloat(credit_key(api_key), float(amount_usd))


def get_extra_credit(api_key: str):
    value = redis_client.get(credit_key(api_key))
    return Decimal(str(value)) if value else Decimal("0.0")


def calculate_cost(tokens: int):
    tokens_decimal = Decimal(tokens)
    cost = (tokens_decimal / Decimal("1000")) * PRICE_PER_1K_TOKENS
    return cost.quantize(Decimal("0.000001"))


def calculate_total_credit(base_credit: Decimal, extra_credit: Decimal):
    return base_credit + extra_credit


def check_warning(tokens: int, total_credit: Decimal):

    cost = calculate_cost(tokens)
    remaining = total_credit - cost

    if remaining < Decimal("0"):
        remaining = Decimal("0")

    if total_credit == Decimal("0"):
        return False, remaining

    remaining_ratio = remaining / total_credit

    if remaining > Decimal("0") and remaining_ratio <= WARNING_THRESHOLD_PERCENT:
        return True, remaining.quantize(Decimal("0.000001"))

    return False, remaining.quantize(Decimal("0.000001"))
