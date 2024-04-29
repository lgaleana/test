import requests
from bs4 import BeautifulSoup


def extract_images_from_url(url: str) -> list:
    response = requests.get(url)
    response.raise_for_status()  # Ensure the response is successful
    soup = BeautifulSoup(response.text, 'html.parser')
    images = []
    # Extract images from <img> tags
    for img in soup.find_all('img'):
        if img.get('src'):
            images.append(img.get('src'))
    # Extract images from any tag with a background-image
    for tag in soup.find_all(style=True):
        style = tag['style']
        if 'background-image' in style:
            url_start = style.find('url(') + 4
            url_end = style.find(')', url_start)
            images.append(style[url_start:url_end])
    return images

if __name__ == '__main__':
    url = input('Enter the URL to extract images from: ')
    images = extract_images_from_url(url)
    print('Extracted images:', images)
