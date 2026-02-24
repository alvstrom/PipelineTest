from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_read_root():
    """Tests health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    
def test_get_weather_helsinki():
    response = client.get("/weather/helsinki")
    assert response.status_code == 200
    
    data = response.json()
    assert "location" in data
    assert "temperature_celsius" in data
    assert data["location"] == "Helsinki, Finland"