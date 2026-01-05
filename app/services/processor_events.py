from app.db.session import async_session
from app.db.models.processor_event import ProcessorEvent
from app.db.models.ledger_entry import LedgerEntry
from app.schemas.processor_event import ProcessorEventResponse, ProcessorEventCreate
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

async def process_event(event: ProcessorEventCreate) -> ProcessorEventResponse:
    """
    Process a payment processor event (idempotent)
    """
    async with async_session() as session:
        # --- Check idempotency by event_id ---
        result = await session.execute(
            select(ProcessorEvent).where(ProcessorEvent.event_id == event.event_id)
        )
        existing = result.scalars().first()
        if existing:
            return ProcessorEventResponse(
                event_id=existing.event_id,
                event_type=existing.event_type,
                restaurant_id=existing.restaurant_id,
                currency=existing.currency,
                amount=existing.amount,
                fee=getattr(existing, "fee", 0),
                processed_at=datetime.utcnow(),
                status="already_processed"
            )

        # --- Create ProcessorEvent entry ---
        new_event = ProcessorEvent(
            event_id=event.event_id,
            event_type=event.event_type,
            occurred_at=event.occurred_at,
            restaurant_id=event.restaurant_id,
            currency=event.currency,
            payload=event.dict(),  # store full event JSON
        )
        # Optional: store amount & fee in ProcessorEvent for convenience
        new_event.amount = getattr(event, "amount", None)
        new_event.fee = getattr(event, "fee", None)

        session.add(new_event)
        await session.flush()  # ⚡ flush to get new_event.id

        # --- Create LedgerEntry depending on event_type ---
        if event.event_type == "charge_succeeded":
            ledger = LedgerEntry(
                restaurant_id=event.restaurant_id,
                currency=event.currency,
                amount=(event.amount or 0) - (event.fee or 0),
                entry_type="net",
                processor_event_id=new_event.id
            )
            session.add(ledger)
        elif event.event_type == "refund_succeeded":
            ledger = LedgerEntry(
                restaurant_id=event.restaurant_id,
                currency=event.currency,
                amount=-(event.amount or 0),
                entry_type="refund",
                processor_event_id=new_event.id
            )
            session.add(ledger)
        elif event.event_type == "payout_paid":
            # payout handled elsewhere
            pass
        else:
            raise ValueError(f"Unsupported event_type: {event.event_type}")

        # --- Commit transaction ---
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise ValueError("Event already processed (DB constraint)")

        # --- Return response ---
        return ProcessorEventResponse(
            event_id=new_event.event_id,
            event_type=new_event.event_type,
            restaurant_id=new_event.restaurant_id,
            currency=new_event.currency,
            amount=new_event.amount,
            fee=new_event.fee,
            processed_at=datetime.utcnow(),
            status="created"
        )
