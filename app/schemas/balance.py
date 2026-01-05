from pydantic import BaseModel

class BalanceResponse(BaseModel):
    restaurant_id: str
    currency: str
    available: int
    pending: int
    last_event_at: str
