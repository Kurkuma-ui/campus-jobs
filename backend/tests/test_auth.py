def test_register_and_login_happy_path(client):
    payload = {"email": "u1@example.com", "full_name": "User One", "password": "secret123"}
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 201
    token = r.json()["access_token"]
    assert token

    r2 = client.post("/auth/login", json={"email": payload["email"], "password": payload["password"]})
    assert r2.status_code == 200
    assert r2.json()["access_token"]

def test_register_duplicate_email(client):
    p = {"email": "dup@example.com", "full_name": "Dup", "password": "secret123"}
    assert client.post("/auth/register", json=p).status_code == 201
    r = client.post("/auth/register", json=p)
    assert r.status_code == 400
    assert "Email" in r.json()["detail"]

def test_login_wrong_password(client):
    p = {"email": "bad@example.com", "full_name": "Bad", "password": "secret123"}
    client.post("/auth/register", json=p)
    r = client.post("/auth/login", json={"email": p["email"], "password": "wrong"})
    assert r.status_code == 401
