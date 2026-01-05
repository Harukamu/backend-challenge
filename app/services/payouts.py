from app.db.session import async_session
from app.db.models.payout import Payout
from app.db.models.ledger_entry import LedgerEntry
from app.services.restaurants import get_balance
from datetime import datetime
import uuid

async def generate_payouts(currency: str, min_amount: int):
    """
    Check balances of all restaurants, create payouts if available >= min_amount,
    and reserve funds in ledger (-payout_reserve)
    """
    async with async_session() as session:
        # 1️⃣ Get distinct restaurants with ledger entries
        result = await session.execute(
            select(LedgerEntry.restaurant_id).where(LedgerEntry.currency == currency).distinct()
        )
        restaurants = [r[0] for r in result.all()]

        payouts_created = []
        for restaurant_id in restaurants:
            balance = await get_balance(restaurant_id, currency)
            if balance.available >= min_amount:
                payout_id = str(uuid.uuid4())
                payout = Payout(
                    payout_id=payout_id,
                    restaurant_id=restaurant_id,
                    currency=currency,
                    amount=balance.available,
                    status="created",
                    created_at=datetime.utcnow()
                )
                session.add(payout)

                # 2️⃣ Ledger entry - reserve funds
                ledger = LedgerEntry(
                    restaurant_id=restaurant_id,
                    currency=currency,
                    amount=-balance.available,
                    type="payout_reserve"
                )
                session.add(ledger)
                payouts_created.append(payout)

        await session.commit()
        return payouts_created

async def get_payout(payout_id: str) -> Payout:
    async with async_session() as session:
        payout = await session.get(Payout, payout_id)
        if not payout:
            raise ValueError(f"Payout {payout_id} not found")
        return payout

async def mark_payout_paid(payout_id: str) -> Payout:
    async with async_session() as session:
        payout = await session.get(Payout, payout_id)
        if not payout:
            raise ValueError(f"Payout {payout_id} not found")
        payout.status = "paid"
        await session.commit()
        return payout
