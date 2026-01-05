from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_payout_generation():
    restaurant_id = "res_test"
    currency = "PEN"

    # crear evento que genere balance suficiente
    event = {
        "event_id": "evt_payout",
        "event_type": "charge_succeeded",
        "occurred_at": "2025-12-21T10:00:00Z",
        "restaurant_id": restaurant_id,
        "currency": currency,
        "amount": 6000,
        "fee": 100,
        "metadata": {}
    }
    client.post("/v1/processor/events", json=event)

    # ejecutar payout
    body = {"currency": currency, "min_amount": 5000}
    r = client.post("/v1/payouts/run", json=body)
    assert r.status_code == 200
    payouts = r.json()
    assert len(payouts) > 0
    assert payouts[0]["status"] == "created"

    # marcar payout como pagado
    payout_id = payouts[0]["payout_id"]
    r_paid = client.post(f"/v1/payouts/{payout_id}/paid")
    assert r_paid.status_code == 200
    assert r_paid.json()["status"] == "paid"
