import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.main import app

# Для старых версий Starlette используем app=, для новых — позиционный
try:
    client = TestClient(app=app)  # Старая версия
except TypeError:
    client = TestClient(app)      # Новая версия

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}