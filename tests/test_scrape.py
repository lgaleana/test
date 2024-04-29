import pytest
from unittest.mock import patch, Mock
from app.scrape import extract_text_from_url, print_text_from_url


def test_extract_text_from_url():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.text = '<html><body>Hello World</body></html>'
        mock_get.return_value = mock_response

        result = extract_text_from_url('http://example.com')
        assert result == 'Hello World'


def test_print_text_from_url(capsys):
    with patch('app.scrape.extract_text_from_url', return_value='Hello World'):
        print_text_from_url('http://example.com')
        captured = capsys.readouterr()
        assert captured.out == 'Hello World\n'
