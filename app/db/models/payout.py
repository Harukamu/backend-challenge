from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Index,
)
from sqlalchemy.sql import func

from app.db.session import Base


class Payout(Base):
    __tablename__ = "payouts"

    id = Column(Integer, primary_key=True)
    payout_id = Column(String, nullable=False, unique=True)

    restaurant_id = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

    as_of = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_payouts_restaurant_currency", "restaurant_id", "currency"),
    )