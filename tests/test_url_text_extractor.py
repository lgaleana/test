import pytest
from unittest.mock import patch
from url_text_extractor import extract_text_from_url


def test_extract_text_from_url():
    with patch('requests.get') as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.text = '<html><body>Hello World</body></html>'
        assert extract_text_from_url('http://example.com') == 'Hello World'
