import requests
from bs4 import BeautifulSoup


def extract_text_from_url(url: str) -> str:
    """Extracts all text from the specified URL using BeautifulSoup.

    Args:
        url (str): The URL to scrape.

    Returns:
        str: The extracted text.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return ' '.join(soup.stripped_strings)

if __name__ == '__main__':
    url_to_scrape = 'http://example.com'
    extracted_text = extract_text_from_url(url_to_scrape)
    print(extracted_text)
