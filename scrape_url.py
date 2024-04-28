import requests
from bs4 import BeautifulSoup

def scrape_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.get_text())

if __name__ == '__main__':
    url = input('Enter the URL: ')
    scrape_text_from_url(url)