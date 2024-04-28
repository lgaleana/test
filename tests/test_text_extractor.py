import pytest
from unittest.mock import patch, Mock
from text_extractor import extract_text_from_url


def test_extract_text_from_url_success():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.text = '<html><body>Hello World</body></html>'
        mock_get.return_value = mock_response

        result = extract_text_from_url('http://example.com')
        assert result == 'Hello World'


def test_extract_text_from_url_failure():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception('Failed to connect')

        with pytest.raises(Exception) as exc_info:
            extract_text_from_url('http://example.com')
        assert str(exc_info.value) == 'Failed to connect'
