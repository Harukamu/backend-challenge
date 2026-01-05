from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    UniqueConstraint,
    Index,
)
from sqlalchemy.sql import func

from app.db.session import Base


class ProcessorEvent(Base):
    __tablename__ = "processor_events"

    id = Column(Integer, primary_key=True)
    event_id = Column(String, nullable=False)
    restaurant_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    occurred_at = Column(DateTime(timezone=True), nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("event_id", name="uq_processor_events_event_id"),
        Index("ix_processor_events_restaurant_currency", "restaurant_id", "currency"),
    )
