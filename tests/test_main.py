import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

@patch('requests.get')
def test_extract_content(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.content = b'<html><body><p>Example Domain</p><img src="https://example.com/image.png"><div style="background-image: url(\'https://example.com/bg.png\');"></div></body></html>'
    client = TestClient(app)
    response = client.get("/extract-content", params={"url": "https://example.com"})
    assert response.status_code == 200
    assert 'https://example.com/image.png' in response.json()['images']
    assert 'https://example.com/bg.png' in response.json()['images']
    assert 'Example Domain' in response.json()['text']
