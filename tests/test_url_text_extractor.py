import pytest
from unittest.mock import patch
from url_text_extractor import extract_images_from_url


def test_extract_images_from_url():
    with patch('requests.get') as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.text = '<html><body><img src="http://example.com/image.jpg"><div style="background-image: url(http://example.com/bg.jpg)"></div></body></html>'
        assert extract_images_from_url('http://example.com') == ['http://example.com/image.jpg', 'http://example.com/bg.jpg']
