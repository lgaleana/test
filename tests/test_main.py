import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

class MockTemplate:
    def __init__(self, name):
        self.name = name

    def render(self, context):
        if self.name == "index.html":
            return 'index.html'
        elif self.name == "results.html":
            headlines = ' '.join([f'<p>{headline}</p>' for headline in context['headlines']])
            images = ' '.join([f'<img src="{image}" alt="Extracted Image">' for image in context['images']])
            return f'<!DOCTYPE html><html lang="en"><body>{headlines} {images}</body></html>'

@patch('fastapi.templating.Jinja2Templates.TemplateResponse')
def test_template_loading(mock_template_response):
    mock_template = MockTemplate("index.html")
    mock_template_response.return_value = mock_template.render({})
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert 'index.html' in response.text

@patch('fastapi.templating.Jinja2Templates.TemplateResponse')
@patch('app.main.get_openai_client')
@patch('requests.get')
def test_extract_content(mock_get, mock_openai_client, mock_template_response):
    mock_openai = MagicMock()
    mock_openai.chat.completions.create.return_value = type('obj', (object,), {'choices': [type('obj', (object,), {'message': {'content': 'Mocked headline'}})]})
    mock_openai_client.return_value = mock_openai

    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.content = b'<html><body><p>Example Domain</p><img src="https://example.com/image.png"><div style="background-image: url(\'https://example.com/bg.png\');"></div></body></html>'
    mock_template = MockTemplate("results.html")
    mock_template_response.return_value = mock_template.render({"request": {}, "images": ["https://example.com/image.png", "https://example.com/bg.png"], "headlines": ["Mocked headline", "Mocked headline"]})
    client = TestClient(app)
    response = client.get("/extract-content", params={"url": "https://example.com"})
    assert response.status_code == 200
    assert 'Mocked headline' in response.text
