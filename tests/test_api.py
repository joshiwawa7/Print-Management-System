from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # drop/create tables to ensure test isolation
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_and_get_order():
    payload = {"customer_name": "Alice", "pages": 3, "print_type": "bw"}
    r = client.post("/orders", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["customer_name"] == "Alice"
    assert data["unit_price"] == 2.0
    assert data["total_price"] == 6.0

    order_id = data["id"]
    r2 = client.get(f"/orders/{order_id}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["id"] == order_id
