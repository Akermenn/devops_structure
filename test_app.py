import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Проверка, что главная страница отвечает кодом 200"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Hello from Backend" in rv.data