import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app({"SECRET_KEY": "test-secret"})
    app.testing = True
    with app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"


def test_login_and_balance_and_transfer(client):
    # login alice
    r = client.post("/login", json={"username": "alice", "password": "password1"})
    assert r.status_code == 200
    token = r.get_json()["token"]

    # check balance
    r = client.get("/balance", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["user"] == "alice"

    # transfer to bob
    r = client.post("/transfer", json={"to": "bob", "amount": 10}, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "success"
