from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.payout import PayoutCreate, PayoutResponse, PayoutItem
from app.services.payouts import generate_payouts, get_payout, mark_payout_paid
from datetime import datetime

router = APIRouter()


@router.post("/v1/payouts/run", response_model=List[PayoutResponse])
async def run_payouts(body: PayoutCreate):
    """
    Generate payouts for all restaurants with available balance >= min_amount.
    Returns the list of created payouts.
    """
    try:
        payouts = await generate_payouts(body.currency, body.min_amount)
        response_list = []

        for payout in payouts:
            response_list.append(
                PayoutResponse(
                    payout_id=payout.payout_id,
                    restaurant_id=payout.restaurant_id,
                    currency=payout.currency,
                    amount=payout.amount,
                    status=payout.status,
                    created_at=payout.created_at.isoformat(),
                    items=[]  # opcional: se pueden rellenar con detalles si implementas payout_items
                )
            )

        return response_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/v1/payouts/{payout_id}", response_model=PayoutResponse)
async def read_payout(payout_id: str):
    """
    Retrieve a payout by its ID.
    """
    try:
        payout = await get_payout(payout_id)
        return PayoutResponse(
            payout_id=payout.payout_id,
            restaurant_id=payout.restaurant_id,
            currency=payout.currency,
            amount=payout.amount,
            status=payout.status,
            created_at=payout.created_at.isoformat(),
            items=[]  # opcional: si tienes payout_items, mapéalos aquí
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/v1/payouts/{payout_id}/paid", response_model=PayoutResponse)
async def payout_paid(payout_id: str):
    """
    Mark a payout as paid (can be triggered by a processor_paid event)
    """
    try:
        payout = await mark_payout_paid(payout_id)
        return PayoutResponse(
            payout_id=payout.payout_id,
            restaurant_id=payout.restaurant_id,
            currency=payout.currency,
            amount=payout.amount,
            status=payout.status,
            created_at=payout.created_at.isoformat(),
            items=[]  # opcional
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
