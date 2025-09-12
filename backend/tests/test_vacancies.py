def test_list_vacancies_empty(client):
    r = client.get("/vacancies")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 0
    assert body["items"] == []

def test_list_and_get_vacancy(client, make_vacancy):
    vid = make_vacancy()

    r = client.get("/vacancies")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == vid

    r2 = client.get(f"/vacancies/{vid}")
    assert r2.status_code == 200
    got = r2.json()
    assert got["id"] == vid
    assert got["title"] == "Junior Developer"
