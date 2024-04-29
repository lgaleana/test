import requests
from bs4 import BeautifulSoup
import re


def extract_text_from_url(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()  # Ensure the response is successful
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()


def extract_images_from_url(url: str) -> list:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    images = [img['src'] for img in soup.find_all('img') if img.get('src')]
    # Extract images from CSS backgrounds
    styles = soup.find_all(style=True)
    background_images = [re.findall(r"url\('(.*)'\)", style['style'])[0] for style in styles if 'background-image' in style['style']]
    images.extend(background_images)
    return images

if __name__ == '__main__':
    url = input('Enter the URL to extract text and images from: ')
    print('Extracted Text:', extract_text_from_url(url))
    print('Extracted Images:', extract_images_from_url(url))
