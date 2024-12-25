import re
from spellchecker import SpellChecker

from storage.storage import JSONDataManager
from storage.config import SIXTEEN_PERSONALITIES_LOC, CLEANSED, RAW, CHATGPT_PERSONALITIES_LOC, CHATGPT_TOPIC_DETAILS_LOC

class DataCleaner:
    def __init__(self, raw_loc:str, cleansed_loc:str, subpath:str):
        self.spellchecker = SpellChecker()
        self.raw_storage_manager = JSONDataManager(raw_loc, subpath)
        self.cleansed_storage_manager = JSONDataManager(cleansed_loc, subpath)

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
    
    def get_raw_storage_manager(self):
        return self.raw_storage_manager
    
    def get_cleansed_storage_manager(self):
        return self.cleansed_storage_manager
    
    def reset_cleansed_storage(self):
        self.cleansed_storage_manager.reset_storage()

class SixteenPersonalityDataCleaner(DataCleaner):
    def __init__(self):
        super().__init__(RAW, CLEANSED, SIXTEEN_PERSONALITIES_LOC)

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

class chatGPTPersonalityDataCleaner(DataCleaner):
    def __init__(self):
        super().__init__(RAW, CLEANSED, CHATGPT_PERSONALITIES_LOC)

    def process_personality_data(self):
        files = self.raw_storage_manager.get_files()
        for file in files:
            data = self.raw_storage_manager.load_json(file)

            # Cleansing process
            for key, value in data.items():
                value = self.clean_text(value)
                # Uncomment the following line if you want to include spell correction
                # value = self.correct_spelling(value)

                data[key] = value

            ptype = file.split('/')[-1].split('.')[0]
            self.cleansed_storage_manager.save_json(ptype, data)

class chatGPTTopicDataCleaner(DataCleaner):
    def __init__(self):
        super().__init__(RAW, CLEANSED, CHATGPT_TOPIC_DETAILS_LOC)

    def process_topic_details_data(self):
        files = self.raw_storage_manager.get_files()
        for file in files:
            data = self.raw_storage_manager.load_json(file)

             # Extract fields
            topic = data.get("topic", "")
            description = data.get("description", "")
            explanation = data.get("explanation", "")

            # Clean the text
            description = self.clean_text(description)
            explanation = self.clean_text(explanation)

            ptype = file.split('/')[-1].split('.')[0]
            self.cleansed_storage_manager.save_json(topic, {topic:explanation})
