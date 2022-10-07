from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_links():
    response = client.post(
        "/visited_links",
        headers={"X-Token": "coneofsilence"},
        json={"links": ["https://ya.ru", "https://ya.ru?q=123", "funbox.ru", 
        "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"]},
    )
    assert response.status_code == 201
    assert response.json() == {
        "status": "ok"
    }


def test_get_domains():
    cur_time = int(datetime.now().timestamp())
    response = client.get(
        f"/visited_domains?from={cur_time-1}&to={cur_time+1}",
        headers={"X-Token": "coneofsilence"}
    )
    domains = ["ya.ru", "funbox.ru", "stackoverflow.com"]
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "stackoverflow.com" and "funbox.ru" and "ya.ru" in response.json()["domains"]
