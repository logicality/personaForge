import json
import os
import shutil
import logging
from typing import List, Dict, Any

from storage.config import RAW_DATA_LOC, CLEANSED_DATA_LOC

class JSONDataManager:
    """
    A class to manage JSON file operations for raw and cleansed data, including subfolder structures.
    """

    def __init__(self, datatype: str, subpath: str):
        self.data_locations = {
            'raw': RAW_DATA_LOC,
            'cleansed': CLEANSED_DATA_LOC,
        }
        self.datatype = datatype
        self.subpath = subpath

    def _get_data_location(self) -> str:
        """
        Get the directory path for the given datatype and subpath.
        """
        if self.datatype not in self.data_locations:
            raise ValueError(f"Invalid datatype '{self.datatype}'. Valid options are: {list(self.data_locations.keys())}")

        base_path = self.data_locations[self.datatype]
        full_path = os.path.join(base_path, self.subpath)

        # Ensure the directory exists
        os.makedirs(full_path, exist_ok=True)
        return full_path

    def save_json(self, filename: str, data: Dict[str, Any]) -> None:
        """
        Save data to a JSON file in the specified datatype and subpath directory.
        """
        data_loc = self._get_data_location()
        file_path = os.path.join(data_loc, f"{filename}.json")

        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)

                if isinstance(existing_data, dict):
                    existing_data.update(data)
                else:
                    existing_data = data

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=2, ensure_ascii=False)
            else:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logging.error(f"Error saving JSON file: {e}")

    def get_files(self) -> List[str]:
        """
        Get a list of JSON file paths in the specified datatype and subpath directory.
        """
        data_loc = self._get_data_location()

        try:
            return [
                os.path.join(data_loc, f) 
                for f in os.listdir(data_loc) 
                if f.endswith('.json')
            ]
        except FileNotFoundError as e:
            logging.error(f"Error accessing directory: {e}")
            return []

    def load_json(self, filepath: str) -> Dict[str, Any]:
        """
        Load JSON data from the specified file.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"Error loading JSON file: {e}")
            return {}

    def reset_storage(self) -> None:
        """
        Reset storage by removing all files in the specified datatype and subpath directory.
        """
        data_loc = self._get_data_location()

        shutil.rmtree(data_loc, ignore_errors=True)
        os.makedirs(data_loc, exist_ok=True)
