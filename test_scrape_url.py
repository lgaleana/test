import pytest
from scrape_url import scrape_text_from_url
from unittest.mock import patch, Mock

@patch('requests.get')
@patch('builtins.print')
def test_scrape_text_from_url(mock_print, mock_get):
    mock_resp = Mock()
    mock_resp.text = '<html><body><p>Hello, World!</p></body></html>'
    mock_get.return_value = mock_resp
    scrape_text_from_url('http://example.com')
    mock_print.assert_called_once_with('Hello, World!')