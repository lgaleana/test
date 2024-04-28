import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    soup = BeautifulSoup(response.text, 'html.parser')
    return ' '.join(soup.stripped_strings)

def main():
    url = input('Enter the URL to scrape: ')
    try:
        text = extract_text_from_url(url)
        print(text)
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
