from app.db.session import async_session
from app.db.models.ledger_entry import LedgerEntry
from app.schemas.balance import BalanceResponse
from sqlalchemy import select, func

async def get_balance(restaurant_id: str, currency: str) -> BalanceResponse:
    """
    Return the current balance of a restaurant
    """
    async with async_session() as session:
        result = await session.execute(
            select(func.sum(LedgerEntry.amount), func.max(LedgerEntry.created_at))
            .where(LedgerEntry.restaurant_id == restaurant_id)
            .where(LedgerEntry.currency == currency)
        )
        total, last_event_at = result.one()
        return BalanceResponse(
            restaurant_id=restaurant_id,
            currency=currency,
            available=total or 0,
            pending=0,  # si implementas ventana de madurez, cámbialo
            last_event_at=last_event_at.isoformat() if last_event_at else None
        )
