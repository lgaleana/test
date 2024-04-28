import pytest
from unittest.mock import patch
from url_text_scraper import extract_text_from_url

def test_extract_text_from_url():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html><body><p>Hello World</p></body></html>'
        assert extract_text_from_url('http://example.com') == 'Hello World'
