from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    entry_type = Column(String, nullable=False)

    processor_event_id = Column(
        Integer,
        ForeignKey("processor_events.id", ondelete="RESTRICT"),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    processor_event = relationship("ProcessorEvent")

    __table_args__ = (
        Index("ix_ledger_restaurant_currency", "restaurant_id", "currency"),
    )