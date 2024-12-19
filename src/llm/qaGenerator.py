from transformers import pipeline
import os
from typing import Dict, List
from storage.config import CLEANSED, SIXTEEN_PERSONALITIES_LOC, CHATGPT_PERSONALITIES_LOC, QA_PERSONALITIES_LOC
from storage.storage import JSONDataManager

class QAGenerator:
    def __init__(self, model_name="google/flan-t5-small", device:int = 0, max_questions:int = 3, max_answers:int = 3):
        """
        Initialize the QA generator with a local Hugging Face model.
        Args:
            model_name (str): The name of the Hugging Face model.
        """
        self.qa_generator = pipeline("text2text-generation", model=model_name, device=device)
        self.max_questions = max_questions
        self.max_answers = max_answers
        self.output_manager = JSONDataManager(CLEANSED, QA_PERSONALITIES_LOC)

    def generate_questions_answers(self, chunks:List) -> Dict[str, str]:
        """
        Generate question-answer pairs for given data.
        Args:
            data (Dict[str, str]): Dictionary with 'topic' as keys and 'chunk' as values.
            max_questions (int): Number of questions to generate per chunk.
        Returns:
            List[Dict[str, str]]: List of generated QA pairs.
        """
        qa_dict = {}

        for chunk in chunks:
            # Generate questions using the pipeline
            prompt = f"""Based on the following text, generate {self.max_questions} questions that cover the most important 
            ideas, descriptive details, and insights.
            Make sure the questions include:
            1. A mix of open-ended and short-answer types.
            2. Questions that require descriptive answers as well as some that can be answered concisely.
            Focus on:
            - Key themes, concepts, and facts in the text.
            - Asking meaningful questions that help someone understand the text more deeply.
            Text:{chunk}
            """
            questions = self.qa_generator(
                prompt, 
                max_length=128, 
                num_return_sequences=self.max_questions, 
                do_sample=True  # Enable sampling for diverse outputs
            )

            for q in questions:
                temp = q['generated_text'].strip()

                # Generate anwers using the pipeline
                prompt = f"""Based on the following text, provide specific and descriptive answers to the given question.
                Instructions:
                - Answers should be detailed and descriptive for open-ended questions.
                - For shorter questions, provide concise and to-the-point answers.
                - Make sure the answers are accurate and reflect the information in the text.
                Question:{temp}
                Text:{chunk}
                """
                answers = self.qa_generator(
                    prompt, 
                    max_length=128, 
                    num_return_sequences=self.max_answers, 
                    do_sample=True  # Enable sampling for diverse outputs
                )

                for a in answers:
                    qa_dict[temp] = a['generated_text'].strip()

        return qa_dict

    def process_and_save(self, storage_manager: JSONDataManager):
        """
        Generate QA dict for all files in cleansed data and save the results into cleansed data storage.
        Args:
            data_manager (JSONDataManager): Instance managing data files.
            max_questions (int): Number of questions to generate per chunk.
        """
        # Get list of files in the raw data location
        raw_files = storage_manager.get_files()

        for file in raw_files:
            data = storage_manager.load_json(file)

            # Generate QA dict for the loaded data
            qa_dict = self.generate_questions_answers(list(data.values()))

            # Save the generated QA dict in the cleansed storage
            filename = os.path.splitext(os.path.basename(file))[0]  # Extract filename without extension
            self.output_manager.save_json(filename, qa_dict)

    def reset_storage(self):
        self.output_manager.reset_storage()

    def process_all_sources(self):
        sixteen_storage_manager = JSONDataManager(datatype=CLEANSED, subpath=SIXTEEN_PERSONALITIES_LOC)
        self.process_and_save(sixteen_storage_manager)
        
        chatGPT_storage_manager = JSONDataManager(datatype=CLEANSED, subpath=CHATGPT_PERSONALITIES_LOC)
        self.process_and_save(chatGPT_storage_manager)
