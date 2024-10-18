from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_cpu(monkeypatch):
    monkeypatch.setattr("psutil.cpu_percent", lambda: 100)

    response = client.get("/cpu/")
    assert response.status_code == 200
    assert response.json() == {"cpu": 100}

    monkeypatch.setattr("psutil.cpu_percent", lambda percpu: 100)
    response = client.get("/cpu/?cpu_id=0")
    assert response.status_code == 200
    assert response.json() == {"cpu1": 100}

    response = client.get("/cpu/?cpu_id=7")
    assert response.status_code == 200
    assert response.json() == {"cpu8": 100}

    response = client.get("/cpu/?cpu_id=-1")
    assert response.status_code == 404
    assert response.json() == {"detail": "CPU not found. cpu_id must be between 0 and 7, but got -1"}

    response = client.get("/cpu/?cpu_id=121")
    assert response.status_code == 404
    assert response.json() == {"detail": "CPU not found. cpu_id must be between 0 and 7, but got 121"}