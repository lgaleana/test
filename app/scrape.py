import requests
from bs4 import BeautifulSoup


def extract_text_from_url(url: str) -> str:
    """Extracts all text from the specified URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        str: The extracted text.
    """
    response = requests.get(url)
    response.raise_for_status()  # Ensure the response is successful

    soup = BeautifulSoup(response.text, 'html.parser')
    return ' '.join(soup.stripped_strings)


def print_text_from_url(url: str):
    """Prints the extracted text from the specified URL.

    Args:
        url (str): The URL to scrape.

    """
    text = extract_text_from_url(url)
    print(text)
