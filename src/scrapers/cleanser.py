import re
from spellchecker import SpellChecker

from storage.storage import JSONDataManager
from storage.config import SIXTEEN_PERSONALITIES_LOC, CLEANSED, RAW

class PersonalityDataCleaner:
    def __init__(self):
        self.spellchecker = SpellChecker()
        self.raw_storage_manager = JSONDataManager(RAW, SIXTEEN_PERSONALITIES_LOC)
        self.cleansed_storage_manager = JSONDataManager(CLEANSED, SIXTEEN_PERSONALITIES_LOC)

    def remove_content_level(self, data):
        """
        Removes the 'content' level from the JSON where it exists.
        Args:
            data (dict): The JSON object to process.
        Returns:
            dict: The processed JSON object with 'content' removed where applicable.
        """
        updated_data = {}
        for key, value in data.items():
            if isinstance(value, dict) and 'content' in value:
                # Replace the 'content' level with its value
                updated_data[key] = value['content']
            else:
                # Keep the key-value pair as is
                updated_data[key] = value
        return updated_data

    def clean_text(self, raw_text):
        """
        Perform text cleaning and normalization.
        Args:
            raw_text (str): The input text to clean.
        Returns:
            str: The cleaned and normalized text.
        """
        # Step 1: Remove special symbols
        cleaned_text = re.sub(r"[^\w\s.,!?]", "", raw_text)  # Remove non-alphanumeric and non-punctuation characters

        # Step 2: Normalize case and whitespace
        cleaned_text = cleaned_text.lower()  # Convert to lowercase
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()  # Normalize whitespace

        return cleaned_text

    def correct_spelling(self, text):
        """
        Perform basic spell correction on text.
        Args:
            text (str): The input text to correct.
        Returns:
            str: The text with corrected spelling.
        """
        words = text.split()
        corrected_words = [
            self.spellchecker.correction(word) if self.spellchecker.correction(word) else word for word in words
        ]
        return " ".join(corrected_words)

    def reset_cleansed_storage(self):
        self.cleansed_storage_manager.reset_storage()

    def process_personality_data(self):
        files = self.raw_storage_manager.get_files()
        for file in files:
            data = self.raw_storage_manager.load_json(file)
            data = self.remove_content_level(data)

            # Cleansing process
            for key, value in data.items():
                if key == 'ptype':
                    continue
                value = self.clean_text(value)
                # Uncomment the following line if you want to include spell correction
                # value = self.correct_spelling(value)

                data[key] = value

            self.cleansed_storage_manager.save_json(data['ptype'], data)
