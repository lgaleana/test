import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

@patch('requests.get')
def test_scrape_text(mock_get):
    mock_get.return_value.content = b'<html><body><p>Example Domain</p></body></html>'
    client = TestClient(app)
    response = client.get("/scrape-text", params={"url": "https://example.com"})
    assert response.status_code == 200
    assert 'Example Domain' in response.text
