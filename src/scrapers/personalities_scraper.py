from scrapers.config import PERSONALITIES, PERSONALITIES_ENDPOINTS, PERSONALITIES_URL, RAW_DATA_LOC
from scrapers.base_scraper import BaseScraper
from scrapers.storage import saveJSON
import random
import time
import shutil
import os

class PersonalitiesScraper(BaseScraper):
    def __init__(self):
        # Initialize the base URL and any other required state
        super().__init__(PERSONALITIES_URL)

    def scrape_personality(self, ptype):
        data = {}
        for section_name, endpoint in PERSONALITIES_ENDPOINTS.items():
            # add randomness to scrapping
            timeout = random.uniform(1,5)
            time.sleep(timeout)

            url = self.base_url + ptype + endpoint
            soup = self.fetch_page(url)
            content = self.extract_article_text(soup)
            data[section_name] = {"content": content}
        return data
    
    def reset_raw(self):
        """Reset cleasend directory."""
        shutil.rmtree(RAW_DATA_LOC, ignore_errors=True)
        os.makedirs(RAW_DATA_LOC, exist_ok=True)
    
    def main(self):
        for ptype, pname in PERSONALITIES.items():  # pylint: disable=unused-variable
            data = self.scrape_personality(ptype)
            data['ptype'] = ptype

            saveJSON(ptype, 'raw', data)
