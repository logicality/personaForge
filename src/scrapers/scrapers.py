import random
import time
import requests
from bs4 import BeautifulSoup

from scrapers.config import PERSONALITIES, PERSONALITIES_ENDPOINTS, PERSONALITIES_URL, SIXTEEN_PERSONALITIES_LOC, RAW
from scrapers.storage import JSONDataManager

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

class PersonalitiesScraper(BaseScraper):
    def __init__(self):
        # Initialize the base URL and any other required state
        super().__init__(PERSONALITIES_URL)

        self.datatype = RAW
        self.subpath = SIXTEEN_PERSONALITIES_LOC
        self.personalities_endpoints = PERSONALITIES_ENDPOINTS
        self.personalities = PERSONALITIES

        # creating a raw storage manager
        self.json_manager = JSONDataManager(self.datatype, self.subpath)

    def scrape_personality(self, ptype):
        data = {}
        for section_name, endpoint in self.personalities_endpoints.items():
            # add randomness to scrapping
            timeout = random.uniform(1,5)
            time.sleep(timeout)

            url = self.base_url + ptype + endpoint
            soup = self.fetch_page(url)
            content = self.extract_article_text(soup)
            data[section_name] = {"content": content}
        return data

    def reset_storage(self):
        self.json_manager.reset_storage()

    def main(self):
        for ptype, pname in self.personalities.items():  # pylint: disable=unused-variable
            data = self.scrape_personality(ptype)
            data['ptype'] = ptype

            self.json_manager.save_json(ptype, data)
