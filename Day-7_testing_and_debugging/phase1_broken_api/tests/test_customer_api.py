from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_existing_active_customer():
    response = client.get("/customers/101")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == 101
    assert data["status"] == "active"
    assert data["name"] == "Alice"

def test_existing_inactive_customer():
    response = client.get("/customers/102")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == 102
    assert data["status"] == "inactive"

def test_missing_customer_returns_404():
    response = client.get("/customers/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Customer Not Found"
