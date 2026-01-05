from fastapi import APIRouter, HTTPException
from sqlalchemy import select, func
from app.db.session import async_session
from app.db.models.ledger_entry import LedgerEntry

router = APIRouter()

@router.get("/v1/restaurants/{restaurant_id}/balance")
async def get_balance(restaurant_id: str, currency: str):
    """
    Return the current balance for a restaurant in a given currency
    """
    async with async_session() as session:
        result = await session.execute(
            select(
                func.coalesce(func.sum(LedgerEntry.amount), 0)
            ).where(
                LedgerEntry.restaurant_id == restaurant_id,
                LedgerEntry.currency == currency
            )
        )
        total = result.scalar()
        return {"restaurant_id": restaurant_id, "currency": currency, "balance": total}