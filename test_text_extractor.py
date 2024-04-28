import pytest
from unittest.mock import patch
from text_extractor import extract_text_from_url


def test_extract_text_from_url():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html><body><p>Hello World!</p></body></html>'

        expected_text = 'Hello World!'
        assert extract_text_from_url('http://example.com') == expected_text
