import pytest
from unittest.mock import patch, Mock
from url_text_extractor import extract_text_from_url

@patch('requests.get')
def test_extract_text_from_url(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '<html><body><p>Hello, world!</p></body></html>'
    mock_get.return_value = mock_response

    expected_text = 'Hello, world!'
    assert extract_text_from_url('http://example.com') == expected_text
