import requests
from bs4 import BeautifulSoup

class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_page(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_article_text(self, soup):
        if not soup:
            return ""
        article = soup.find("article")
        if article:
            return article.get_text(separator="\n").strip()
        return ""
