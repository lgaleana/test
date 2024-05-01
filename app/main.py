from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import requests
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/extract-content")
def extract_content(request: Request, url: str) -> HTMLResponse:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    images = []
    headlines = []
    for img in soup.find_all('img'):
        if img.get('src'):
            images.append(img.get('src'))
            text = soup.get_text().strip().replace('\n', ' ')
            prompt = f"Generate a catchy headline for an image with the following description: {text}"
            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
                temperature=0
            )
            headlines.append(openai_response.choices[0].message['content'].strip())
    for tag in soup.find_all(style=True):
        style = tag['style']
        if 'background-image' in style:
            url_start = style.find('url(') + 4
            url_end = style.find(')', url_start)
            image_url = style[url_start:url_end].strip('"\'')
            images.append(image_url)
            text = soup.get_text().strip().replace('\n', ' ')
            prompt = f"Generate a catchy headline for an image with the following description: {text}"
            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
                temperature=0
            )
            headlines.append(openai_response.choices[0].message['content'].strip())
    return templates.TemplateResponse("results.html", {"request": request, "images": images, "headlines": headlines})
