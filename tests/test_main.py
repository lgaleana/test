import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

class MockTemplate:
    def render(self, context):
        return 'index.html'

@patch('fastapi.templating.Jinja2Templates.TemplateResponse')
def test_template_loading(mock_template_response):
    mock_template = MockTemplate()
    mock_template_response.return_value = mock_template.render({})
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert 'index.html' in response.text

@patch('fastapi.templating.Jinja2Templates.TemplateResponse')
@patch('requests.get')
@patch('openai.Completion.create')
def test_extract_content(mock_openai_create, mock_get, mock_template_response):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.content = b'<html><body><p>Example Domain</p><img src="https://example.com/image.png"><div style="background-image: url(\'https://example.com/bg.png\');"></div></body></html>'
    mock_openai_create.return_value = type('obj', (object,), {'choices': [type('obj', (object,), {'text': 'Mocked headline'})]})
    mock_template = MockTemplate()
    mock_template_response.return_value = mock_template.render({"request": {}, "images": [], "text": ""})
    client = TestClient(app)
    response = client.get("/extract-content", params={"url": "https://example.com"})
    assert response.status_code is 200
    assert 'index.html' in response.text
