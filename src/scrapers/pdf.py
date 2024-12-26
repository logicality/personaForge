import os
import time
import logging
import random
from typing import List, Dict, Optional
import pdfplumber

from storage.config import RAW
from storage.storage import JSONDataManager

# Configure logging
logging.basicConfig(
    filename='pdf_scraper.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class BasePDFScraper:
    """
    A base class for PDF scrapers.
    """

    def __init__(self, subpath: str):
        """
        Initialize the BasePDFScraper with the path to the raw PDF folder.

        Args:
            raw_folder (str): The directory containing raw PDF files.
            storage_subpath (str): Subdirectory path for storage within the storage base directory.
        """
        self.storage_manager = JSONDataManager(RAW, subpath)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            str: The extracted text content.
        """
        if not os.path.exists(pdf_path):
            logging.error("Raw folder does not exist: %s", pdf_path)
            return ""

        extracted_text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
                    else:
                        logging.warning("No text found on page %s of %s.", page_num, pdf_path)
        except Exception as e:
            logging.error("Error reading PDF %s: %s", pdf_path, e)

        if extracted_text:
            logging.info("Extracted text from %s.", pdf_path)
        return extracted_text

    def clean_text(self, text: str) -> str:
        """
        Clean the extracted text.

        Args:
            text (str): The raw text extracted from the PDF.

        Returns:
            str: The cleaned text.
        """
        # Example cleaning steps:
        # - Remove excessive whitespace
        # - Normalize encoding
        # - Remove unwanted characters or patterns
        cleaned = ' '.join(text.split())
        return cleaned

    def parse_sections(self, text: str) -> Dict[str, str]:
        """
        Parse the cleaned text to extract relevant sections.

        Args:
            text (str): The cleaned text from the PDF.

        Returns:
            Dict[str, str]: A dictionary with section names as keys and their content as values.
        """
        # Implement parsing logic based on PDF structure
        # This is a placeholder example
        sections = {}

        # Example: Split text based on headings using simple keyword detection
        # Adjust the markers based on actual PDF content
        # You can enhance this using regex or NLP techniques for better accuracy
        if "Description" in text and "Explanation" in text:
            parts = text.split("Description")
            if len(parts) > 1:
                description_part = parts[1].split("Explanation")[0].strip()
                explanation_part = parts[1].split("Explanation")[1].strip()
                sections["description"] = description_part
                sections["explanation"] = explanation_part
        elif "Introduction" in text and "Details" in text:
            parts = text.split("Introduction")
            if len(parts) > 1:
                introduction_part = parts[1].split("Details")[0].strip()
                details_part = parts[1].split("Details")[1].strip()
                sections["introduction"] = introduction_part
                sections["details"] = details_part
        else:
            # Fallback: Assign all text to a generic section
            sections["content"] = text

        return sections

    def reset_storage(self):
        self.storage_manager.reset_storage()

# scrapers/pdf_scraper.py (continued)

# class GenericPDFScraper(BasePDFScraper):
#     """
#     A generic scraper for extracting information from PDF documents.
#     """

#     def __init__(self, raw_folder: str, storage_subpath: str = JSON_STORAGE_SUBPATH):
#         """
#         Initialize the GenericPDFScraper with the required configuration.

#         Args:
#             raw_folder (str): The directory containing raw PDF files.
#             storage_subpath (str): Subdirectory path for storage within the storage base directory.
#         """
#         super().__init__(raw_folder, storage_subpath)

#     def get_pdf_files(self) -> List[str]:
#         """
#         Retrieve a list of PDF file paths from the raw folder.

#         Returns:
#             List[str]: List of PDF file paths.
#         """
#         if not os.path.isdir(self.raw_folder):
#             logging.error(f"Raw folder does not exist: {self.raw_folder}")
#             return []

#         pdf_files = [
#             os.path.join(self.raw_folder, file)
#             for file in os.listdir(self.raw_folder)
#             if file.lower().endswith('.pdf')
#         ]
#         logging.info(f"Found {len(pdf_files)} PDF files in {self.raw_folder}.")
#         return pdf_files

#     def scrape_pdf(self, pdf_path: str) -> Dict[str, Dict[str, str]]:
#         """
#         Scrape information from a specific PDF file.

#         Args:
#             pdf_path (str): The path to the PDF file.

#         Returns:
#             Dict[str, Dict[str, str]]: The scraped data structured by sections.
#         """
#         data = {}
#         extracted_text = self.extract_text_from_pdf(pdf_path)
#         if not extracted_text:
#             logging.error(f"No text extracted from {pdf_path}.")
#             return data

#         cleaned_text = self.clean_text(extracted_text)
#         sections = self.parse_sections(cleaned_text)

#         # Assign sections to data
#         for section, content in sections.items():
#             data[section] = {"content": content}

#         return data

#     def get_topic_from_filename(self, filename: str) -> Optional[str]:
#         """
#         Extract the topic from the PDF filename.

#         Args:
#             filename (str): The name of the PDF file.

#         Returns:
#             Optional[str]: The extracted topic or None if not found.
#         """
#         base_name = os.path.basename(filename)
#         name_part = os.path.splitext(base_name)[0]

#         # Example: "Data_Science_Overview.pdf" -> "Data Science Overview"
#         topic = name_part.replace('_', ' ').strip()
#         if topic:
#             return topic
#         return None

#     def scrape_all_pdfs(self):
#         """
#         Scrape all PDF files in the raw folder and save the extracted data.
#         """
#         pdf_files = self.get_pdf_files()
#         if not pdf_files:
#             logging.warning("No PDF files found to scrape.")
#             return

#         for pdf_file in pdf_files:
#             topic = self.get_topic_from_filename(pdf_file)
#             if not topic:
#                 logging.warning(f"Topic not found in filename: {pdf_file}")
#                 continue

#             data = self.scrape_pdf(pdf_file)
#             if not data:
#                 logging.warning(f"No data scraped from {pdf_file}.")
#                 continue

#             data['topic'] = topic

#             # Save the data using JSONDataManager
#             self.json_manager.save_json(topic, data)

#             # Respectful delay to avoid overwhelming the system
#             time.sleep(random.uniform(1, 3))

#     def main(self):
#         """
#         Main method to scrape all PDFs and save the data.
#         """
#         logging.info("Starting PDF scraping process.")
#         self.reset_storage()
#         self.scrape_all_pdfs()
#         logging.info("PDF scraping process completed.")
