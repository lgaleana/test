from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

n_images = int(os.getenv('N_IMAGES', '10'))

def generate_headline(description: str, image_url: str) -> str:
    client = get_openai_client()
    prompt = f"Generate a catchy headline for an image with the following description and URL: {description}, {image_url}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message['content'].strip()

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
    text = soup.get_text().strip().replace('\n', ' ')
    image_elements = soup.find_all('img') + [tag for tag in soup.find_all(style=True) if 'background-image' in tag['style']]
    image_elements = image_elements[:n_images]
    images = []
    headlines = []
    def process_image(img):
        image_url = img.get('src') if img.name == 'img' else img['style'].split('url(')[1].split(')')[0].strip('"\'')
        headline = generate_headline(text, image_url)
        return (image_url, headline)
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(process_image, image_elements)
    for image_url, headline in results:
        images.append(image_url)
        headlines.append(headline)
    return templates.TemplateResponse("results.html", {"request": request, "images": images, "headlines": headlines})
