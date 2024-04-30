from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import requests

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/extract-content")
def extract_content(request: Request, url: str) -> HTMLResponse:
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
    return templates.TemplateResponse("results.html", {"request": request, "images": images, "text": text})
