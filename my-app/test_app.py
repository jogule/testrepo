import pytest
import json
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_sample_page(client):
    """Test the main page returns 200 and contains expected content"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'html' in response.data


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get('/healthcheck')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['health_status'] == 'OK'


def test_health_check_json_format(client):
    """Test health check returns proper JSON"""
    response = client.get('/healthcheck')
    assert response.content_type == 'application/json'


def test_nonexistent_route(client):
    """Test 404 for non-existent routes"""
    response = client.get('/nonexistent')
    assert response.status_code == 404