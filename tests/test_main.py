from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Тест корня сайта"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server work"}

def test_health_check():
    """Тест health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "OK" 