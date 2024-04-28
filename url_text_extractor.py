import requests
from bs4 import BeautifulSoup


def extract_text_from_url(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()  # Ensure the response is successful

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator='\n')
    return text


def main():
    url = input("Enter the URL to extract text from: ")
    try:
        text = extract_text_from_url(url)
        print(text)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
