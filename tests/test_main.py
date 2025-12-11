import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.main import app

try:
    client = TestClient(app=app)  
except TypeError:
    client = TestClient(app)     
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}