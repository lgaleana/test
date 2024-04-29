import requests
from bs4 import BeautifulSoup


def extract_images_from_html(soup: BeautifulSoup) -> list:
    images = []
    # Extract from <img> tags
    for img in soup.find_all('img'):
        if img.get('src'):
            images.append(img.get('src'))
    # Extract from any tag with a style attribute containing 'background-image'
    for tag in soup.find_all(style=True):
        style = tag['style']
        if 'background-image' in style:
            url_start = style.find('url(') + 4
            url_end = style.find(')', url_start)
            image_url = style[url_start:url_end].strip('"\'')
            images.append(image_url)
    return images

def extract_text_and_images_from_url(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()  # Ensure the response is successful
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    images = extract_images_from_html(soup)
    return {'text': text, 'images': images}

if __name__ == '__main__':
    url = input('Enter the URL to extract text and images from: ')
    result = extract_text_and_images_from_url(url)
    print('Extracted Text:', result['text'])
    print('Extracted Images:', result['images'])
