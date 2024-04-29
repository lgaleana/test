from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/extract-content")
def extract_content(url: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = []
    # Extract images from <img> tags
    for img in soup.find_all('img'):
        if img.get('src'):
            images.append(img.get('src'))
    # Extract images from any tag with a style attribute containing 'background-image'
    for tag in soup.find_all(style=True):
        style = tag['style']
        if 'background-image' in style:
            url_start = style.find('url(') + 4
            url_end = style.find(')', url_start)
            image_url = style[url_start:url_end].strip('"\'')
            images.append(image_url)
    text = soup.get_text()
    return {'images': images, 'text': text}
