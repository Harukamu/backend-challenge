from fastapi import APIRouter, HTTPException
from app.services.restaurants import get_balance  
from app.schemas.balance import BalanceResponse  

router = APIRouter()

@router.get("/v1/restaurants/{restaurant_id}/balance", response_model=BalanceResponse)
async def restaurant_balance(restaurant_id: str, currency: str):
    try:
        balance = await get_balance(restaurant_id, currency)
        return balance
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
