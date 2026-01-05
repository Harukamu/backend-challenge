from sqlalchemy import Column, Integer, String, DateTime, Float, func
from app.db.session import Base
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_event_idempotency_sync():
    event = {
        "event_id": "evt_test",
        "event_type": "charge_succeeded",
        "occurred_at": "2025-12-20T15:10:00Z",
        "restaurant_id": "res_test",
        "currency": "PEN",
        "amount": 1000,
        "fee": 50,
        "metadata": {}
    }
    r1 = client.post("/v1/processor/events", json=event)
    r2 = client.post("/v1/processor/events", json=event)
    assert r1.status_code == 201
    assert r2.status_code == 200
