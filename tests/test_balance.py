from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db.session import Base
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_balance_computation():
    restaurant_id = "res_test"
    currency = "PEN"

    unique_event_id = f"evt_balance_{uuid.uuid4()}"
    
    # primero crear un evento de charge
    event = {
        "event_id": "evt_balance",
        "event_type": "charge_succeeded",
        "occurred_at": "2025-12-20T16:00:00Z",
        "restaurant_id": restaurant_id,
        "currency": currency,
        "amount": 1000,
        "fee": 50,
        "metadata": {}
    }
    client.post("/v1/processor/events", json=event)

    # luego consultar balance
    r = client.get(f"/v1/restaurants/{restaurant_id}/balance?currency={currency}")
    assert r.status_code == 200
    data = r.json()
    assert data["available"] == 950  # 1000 - 50
