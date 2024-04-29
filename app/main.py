from fastapi import FastAPI, HTTPException
from typing import Optional
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/scrape/")
def scrape_url(url: Optional[str] = None) -> str:
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is missing.")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

    soup = BeautifulSoup(response.text, 'html.parser')
    text = ' '.join(soup.stripped_strings)
    return text
