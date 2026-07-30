from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from .models import UsageEvent, CreditEvent

PRICE_PER_1K = Decimal("0.002")


def calculate_cost(tokens: int) -> Decimal:
    tokens_decimal = Decimal(tokens)
    cost = (tokens_decimal / Decimal("1000")) * PRICE_PER_1K
    return cost.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def record_usage(db: Session, api_key: str, tokens: int):
    cost = calculate_cost(tokens)

    event = UsageEvent(
        api_key=api_key,
        tokens=tokens,
        cost_usd=cost
    )

    db.add(event)
    db.commit()

    return cost


def add_credit(db: Session, api_key: str, amount: Decimal):

    event = CreditEvent(
        api_key=api_key,
        amount_usd=amount
    )

    db.add(event)
    db.commit()


def get_monthly_usage(db: Session, api_key: str):

    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)

    total = db.query(
        func.coalesce(func.sum(UsageEvent.cost_usd), 0)
    ).filter(
        UsageEvent.api_key == api_key,
        UsageEvent.created_at >= month_start
    ).scalar()

    return Decimal(total)


def get_monthly_credit(db: Session, api_key: str):

    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0)

    total = db.query(
        func.coalesce(func.sum(CreditEvent.amount_usd), 0)
    ).filter(
        CreditEvent.api_key == api_key,
        CreditEvent.created_at >= month_start
    ).scalar()

    return Decimal(total)


# ✅ ✅ ✅ NOVO: Histórico mensal completo
def get_monthly_history(db: Session, api_key: str):

    usage = db.query(
        func.strftime("%Y-%m", UsageEvent.created_at).label("month"),
        func.coalesce(func.sum(UsageEvent.cost_usd), 0)
    ).filter(
        UsageEvent.api_key == api_key
    ).group_by("month").all()

    credit = db.query(
        func.strftime("%Y-%m", CreditEvent.created_at).label("month"),
        func.coalesce(func.sum(CreditEvent.amount_usd), 0)
    ).filter(
        CreditEvent.api_key == api_key
    ).group_by("month").all()

    usage_dict = {row[0]: Decimal(row[1]) for row in usage}
    credit_dict = {row[0]: Decimal(row[1]) for row in credit}

    months = set(usage_dict.keys()).union(set(credit_dict.keys()))

    history = []

    for month in sorted(months):
        total_usage = usage_dict.get(month, Decimal("0"))
        total_credit = credit_dict.get(month, Decimal("0"))

        history.append({
            "month": month,
            "usage_usd": float(total_usage),
            "credit_usd": float(total_credit),
            "net_usd": float(total_credit - total_usage)
        })

    return history
