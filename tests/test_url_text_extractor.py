import pytest
from unittest.mock import patch
from url_text_extractor import extract_text_and_images_from_url


def test_extract_text_and_images_from_url():
    with patch('requests.get') as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.text = "<html><body>Hello World<img src='example.jpg' style='background-image: url(example-bg.jpg);'></body></html>"
        result = extract_text_and_images_from_url('http://example.com')
        assert result['text'] == 'Hello World'
        assert 'example.jpg' in result['images']
        assert 'example-bg.jpg' in result['images']
