import requests
from bs4 import BeautifulSoup


def extract_images_from_html(html_content: str) -> list:
    soup = BeautifulSoup(html_content, 'html.parser')
    images = []
    # Extract from <img> tags
    for img_tag in soup.find_all('img'):
        if img_tag.get('src'):
            images.append(img_tag.get('src'))
    # Extract from any tag with a style attribute containing a background image
    for tag in soup.find_all(style=True):
        style = tag['style']
        if 'background-image' in style:
            url_start = style.find('url(') + 4
            url_end = style.find(')', url_start)
            images.append(style[url_start:url_end])
    return images

def extract_text_and_images_from_url(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()  # Ensure the response is successful
    text = BeautifulSoup(response.text, 'html.parser').get_text()
    images = extract_images_from_html(response.text)
    return {'text': text, 'images': images}

if __name__ == '__main__':
    url = input('Enter the URL to extract text and images from: ')
    result = extract_text_and_images_from_url(url)
    print('Extracted Text:', result['text'])
    print('Extracted Images:', result['images'])
