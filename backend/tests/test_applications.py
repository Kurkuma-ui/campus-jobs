def _register_and_login(client, email="student@example.com"):
    reg = {"email": email, "full_name": "Student", "password": "secret123"}
    client.post("/auth/register", json=reg)
    r = client.post("/auth/login", json={"email": email, "password": "secret123"})
    assert r.status_code == 200
    return r.json()["access_token"]

def test_create_application_needs_auth(client, make_vacancy):
    vid = make_vacancy()
    r = client.post("/applications", json={"vacancy_id": vid, "cover_letter": "Hi"})
    assert r.status_code in (401, 403)  # без токена нельзя

def test_create_application_and_me(client, make_vacancy):
    vid = make_vacancy()
    token = _register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post("/applications", headers=headers, json={"vacancy_id": vid, "cover_letter": "I am ready"})
    assert r.status_code == 201
    app = r.json()
    assert app["vacancy_id"] == vid
    assert app["status"] == "submitted"

    r2 = client.get("/applications/me", headers=headers)
    assert r2.status_code == 200
    items = r2.json()
    assert len(items) == 1
    assert items[0]["id"] == app["id"]
