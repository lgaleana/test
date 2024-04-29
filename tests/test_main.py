import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

@patch('requests.get')
def test_scrape_url(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.text = '<html><body><p>Example Domain</p></body></html>'
    client = TestClient(app)
    response = client.get("/scrape/", params={"url": "https://example.com"})
    assert response.status_code == 200
    assert 'Example Domain' in response.text

def test_scrape_url_no_url():
    client = TestClient(app)
    response = client.get("/scrape/")
    assert response.status_code == 400
    assert 'URL parameter is missing.' in response.json()['detail']
