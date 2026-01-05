from pydantic import BaseModel
from typing import List, Optional

class PayoutItem(BaseModel):
    type: str
    amount: int

class PayoutCreate(BaseModel):
    currency: str
    min_amount: int

class PayoutResponse(BaseModel):
    payout_id: str
    restaurant_id: str
    currency: str
    amount: int
    status: str
    created_at: str
    items: Optional[List[PayoutItem]] = []
