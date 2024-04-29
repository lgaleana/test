import pytest
from unittest.mock import patch
from url_text_extractor import extract_text_from_url, extract_images_from_url


def test_extract_text_from_url():
    with patch('requests.get') as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.text = '<html><body>Hello World</body></html>'
        assert extract_text_from_url('http://example.com') == 'Hello World'

def test_extract_images_from_url():
    with patch('requests.get') as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.text = "<html><body><img src='image1.jpg'><div style='background-image:url(image2.jpg)'></div></body></html>"
        assert extract_images_from_url('http://example.com') == ['image1.jpg', 'image2.jpg']
