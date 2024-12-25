import random
import time
import requests
from bs4 import BeautifulSoup
from typing import Dict

from scrapers.config import PERSONALITIES, PERSONALITIES_ENDPOINTS, PERSONALITIES_URL
from storage.config import SIXTEEN_PERSONALITIES_LOC, RAW
from storage.storage import JSONDataManager

class BaseScraper:
    """
    A base class for web scrapers.
    """

    def __init__(self, base_url: str):
        """
        Initialize the BaseScraper with a base URL.
        
        Args:
            base_url (str): The base URL for the scraper.
        """
        self.base_url = base_url

    def fetch_page(self, url: str) -> BeautifulSoup:
        """
        Fetch a web page and return its parsed content.
        
        Args:
            url (str): The URL of the web page to fetch.
        
        Returns:
            BeautifulSoup: The parsed content of the web page.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_article_text(self, soup: BeautifulSoup) -> str:
        """
        Extract text content from an article element in the parsed HTML.
        
        Args:
            soup (BeautifulSoup): The parsed HTML content.
        
        Returns:
            str: The extracted text content.
        """
        if not soup:
            return ""
        article = soup.find("article")
        if article:
            return article.get_text(separator="\n").strip()
        return ""

class PersonalitiesScraper(BaseScraper):
    """
    A scraper for extracting personality information from a website.
    """

    def __init__(self):
        """
        Initialize the PersonalitiesScraper with the required configuration.
        """
        super().__init__(PERSONALITIES_URL)
        self.datatype = RAW
        self.subpath = SIXTEEN_PERSONALITIES_LOC
        self.personalities_endpoints = PERSONALITIES_ENDPOINTS
        self.personalities = PERSONALITIES
        self.json_manager = JSONDataManager(self.datatype, self.subpath)

    def scrape_personality(self, ptype: str) -> Dict[str, Dict[str, str]]:
        """
        Scrape information for a specific personality type.
        
        Args:
            ptype (str): The personality type to scrape.
        
        Returns:
            Dict[str, Dict[str, str]]: The scraped data.
        """
        data = {}
        for section_name, endpoint in self.personalities_endpoints.items():
            time.sleep(random.uniform(1, 5))  # Add randomness to scraping
            url = f"{self.base_url}{ptype}{endpoint}"
            soup = self.fetch_page(url)
            content = self.extract_article_text(soup)
            data[section_name] = {"content": content}
        return data

    def reset_storage(self):
        """
        Reset the storage for scraped data.
        """
        self.json_manager.reset_storage()

    def main(self):
        """
        Main method to scrape all personalities and save the data.
        """
        for ptype in self.personalities:
            data = self.scrape_personality(ptype)
            data['ptype'] = ptype
            self.json_manager.save_json(ptype, data)
