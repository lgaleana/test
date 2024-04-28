import requests
from bs4 import BeautifulSoup


def extract_text_from_url(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()  # Ensure the response is successful
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

if __name__ == '__main__':
    url = input('Enter the URL to extract text from: ')
    print(extract_text_from_url(url))
