from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests

app = FastAPI()

@app.get("/scrape-text")
def scrape_text(url: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    images = set()
    for img in soup.find_all('img'):
        if img.get('src'):
            images.add(img.get('src'))
    for tag in soup.find_all():
        if 'background-image' in str(tag):
            style = tag.get('style')
            if style:
                url_start = style.find('url(')
                if url_start != -1:
                    url_end = style.find(')', url_start)
                    if url_end != -1:
                        image_url = style[url_start+4:url_end].strip('"')
                        images.add(image_url)
    print(text)
    print(images)
    return {'text': text, 'images': list(images)}
