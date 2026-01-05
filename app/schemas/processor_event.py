from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime

class ProcessorEventCreate(BaseModel):
    event_id: str
    event_type: str  # charge_succeeded, refund_succeeded, payout_paid
    occurred_at: datetime
    restaurant_id: str
    currency: str
    amount: int
    fee: Optional[int] = 0
    metadata: Optional[Dict[str, str]] = {}

class ProcessorEventResponse(BaseModel):
    event_id: str
    event_type: str
    restaurant_id: str
    currency: str
    amount: int
    fee: Optional[int] = 0
    processed_at: datetime
    status: str  # "created" o "already_processed"
