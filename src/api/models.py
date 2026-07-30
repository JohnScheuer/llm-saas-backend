from sqlalchemy import Column, Integer, String, DateTime, Numeric
from datetime import datetime
from decimal import Decimal

from .db import Base


class UsageEvent(Base):
    __tablename__ = "usage_events"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, index=True)
    tokens = Column(Integer)
    cost_usd = Column(Numeric(18, 6))  # ✅ Decimal
    created_at = Column(DateTime, default=datetime.utcnow)


class CreditEvent(Base):
    __tablename__ = "credit_events"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, index=True)
    amount_usd = Column(Numeric(18, 6))  # ✅ Decimal
    created_at = Column(DateTime, default=datetime.utcnow)
