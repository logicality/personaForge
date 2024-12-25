import os
import json
import re
from typing import Dict

from openai import OpenAI
from scrapers.config import PERSONALITIES, TOPIC_COMMUNICATION
from storage.storage import JSONDataManager
from storage.config import RAW, CHATGPT_PERSONALITIES_LOC, CHATGPT_TOPICS_LOC, CHATGPT_TOPIC_DETAILS_LOC

class ChatGPT:
    """
    A Python wrapper for interacting with the OpenAI ChatGPT API.
    """

    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant."

    def __init__(self, api_key=None, model=DEFAULT_MODEL):
        """
        Initialize the ChatGPT class with the API key and model.
        
        Args:
            api_key (str): Your OpenAI API key. If None, it will look for an environment variable.
            model (str): The OpenAI model to use (default: gpt-4o-mini).
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in the OPENAI_API_KEY environment variable.")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def send_prompt(self, prompt, system_message=DEFAULT_SYSTEM_MESSAGE):
        """
        Sends a prompt to the ChatGPT API and retrieves the response.
        
        Args:
            prompt (str): The user input or prompt.
            system_message (str): The system message to set the assistant's behavior.
        
        Returns:
            str: The response from the ChatGPT API.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"

class TopicExtraction(ChatGPT):
    """
    Extends the ChatGPT class to extract additional subtopics for a given topic,
    excluding any that are already collected.
    """

    PROMPT_TOPIC_EXTRACTION = """System/Developer Instruction
        You are an advanced research assistant capable of leveraging both your internal knowledge base and external sources (web scraping, if possible).

        Task:
        You are given two inputs:
        A primary topic, s: {topic}
        A list of already-collected sub-topics, c: {exclusionList} (these must be excluded from further suggestions).

        Identify a comprehensive set of new relevant subtopics or sub-subjects, s′, that expand on s. Exclude any sub-topics appearing in .

        For each newly identified sub-topic s′, produce a prompt (stored in a "value" field) that can later be used to gather up-to-date, in-depth information.

        Output:
        Return a Python dictionary in this format:
        {{
            "topic": "<the main topic s>",
            "subtopics":
                {{
                    "<new sub-topic s′>": "<prompt to gather more info on s′>"
                }}
        }}

        Constraints/Clarifications:
        Ensure the total output remains concise enough to fit within response size limits.
        Generate sufficient subtopics (5–10 or more if necessary) to cover the key dimensions of s—excluding those found in c.
        Each "value" prompt should be brief yet clear, guiding future queries for deeper knowledge.
        Incorporate any newly discovered, relevant data from external lookups if helpful, but do not include the responses to the prompts—only the prompts themselves.
        """

    PROMPT_TOPIC_EXPLORATION = """
        System/Developer Instruction
        You are an advanced research assistant capable of using both your internal knowledge and external sources (web scraping, if possible).

        Task:
        You have been given a specific subtopic:short-description to explore in detail: topic:{topic} and description:{description}.
        Provide a thorough, in-depth explanation of this subtopic. Cover its background, key concepts, relevant examples, current trends, and any notable future directions or debates. Use any authoritative, up-to-date data or references that can be reliably retrieved.

        Constraints:
        1. Aim for maximum completeness without exceeding the allowed response size (token limit).
        2. Present the information in a clear, structured manner, using headings or bullet points where beneficial.
        3. Cite external sources or data when referencing specific statistics, studies, or major developments.
        4. Summarize or omit excessively detailed data if it would exceed the response size limit, but include as much relevant detail as possible.
        5. Avoid purely speculative or unverified information unless clearly labeled as such.

        Objective:
        Deliver the best possible answer on this subtopic, combining depth, clarity, and practical insights for the user.

        Now, please provide your comprehensive answer.
        """

    def __init__(self, api_key=None, model="gpt-4o-mini"):
        super().__init__(api_key, model)
        self.topics_storage_manager = JSONDataManager(RAW, CHATGPT_TOPICS_LOC)
        self.description_store_manager = JSONDataManager(RAW, CHATGPT_TOPIC_DETAILS_LOC)

    def reset_storage(self):
        """
        Reset storage for topics and descriptions.
        """
        self.topics_storage_manager.reset_storage()
        self.description_store_manager.reset_storage()

    def get_extracted_topics(self) -> list:
        """
        Get a list of extracted topics from the storage.

        Returns:
            list: A list of extracted topics.
        """
        filenames = self.topics_storage_manager.get_files()
        extracted_topics = []

        for file in filenames:
            extracted_topics.extend(list(self.topics_storage_manager.load_json(file).keys()))

        return extracted_topics
    
    def get_extracted_data(self) -> dict:
        """
        Get aggregated data from all extracted topics.

        Returns:
            dict: Aggregated data from all extracted topics.
        """
        filenames = self.topics_storage_manager.get_files()
        aggregated_data = {}

        for file in filenames:
            data = self.topics_storage_manager.load_json(file)
            
            if isinstance(data, dict):
                aggregated_data.update(data)

        return aggregated_data

    def extract_topics(self, topic: str, exclusion_list: list) -> dict:
        """
        Extract subtopics for a given topic, excluding any that are already collected.

        Args:
            topic (str): The primary topic for which we want subtopics.
            exclusion_list (list): Sub-topics to exclude from suggestions.

        Returns:
            dict: A dictionary with the keys 'topic' and 'subtopics'.
        """
        prompt = self.PROMPT_TOPIC_EXTRACTION.format(topic=topic, exclusionList=exclusion_list)
        response = self.send_prompt(prompt)

        pattern = re.compile(r"```python\s*(.*?)\s*```", re.DOTALL)
        match = pattern.search(response)

        if not match:
            parsed_data = {"topic": topic, "subtopics": []}
        else:
            code_block = match.group(1)
            try:
                parsed_data = json.loads(code_block)
            except json.JSONDecodeError:
                parsed_data = {"topic": topic, "subtopics": []}

        self.topics_storage_manager.save_json(topic, parsed_data['subtopics'])
        return parsed_data
    
    def explore_subtopic(self, topic: str, description: str) -> dict:
        """
        Explore a subtopic in detail.

        Args:
            topic (str): The subtopic name (or short descriptor).
            description (str): Additional context or details about the subtopic.

        Returns:
            dict: A dictionary with 'topic', 'description', and 'explanation' fields.
        """
        prompt = self.PROMPT_TOPIC_EXPLORATION.format(topic=topic, description=description)
        response = self.send_prompt(prompt)

        parsed_data = {
            "topic": topic,
            "description": description,
            "explanation": response
        }

        filename = f"{topic}".replace(" ", "_")
        self.description_store_manager.save_json(filename, parsed_data)

        return parsed_data

class PersonalityInsights(ChatGPT):
    """
    Extends the ChatGPT class to generate prompts and retrieve insights about personality types.
    """

    def __init__(self, api_key=None, model="gpt-4o-mini"):
        """
        Initialize the PersonalityInsights class with the API key and model.
        
        Args:
            api_key (str): Your OpenAI API key. If None, it will look for an environment variable.
            model (str): The OpenAI model to use (default: gpt-4o-mini).
        """
        super().__init__(api_key, model)
        self.personalities = PERSONALITIES
        self.storage_manager = JSONDataManager(RAW, CHATGPT_PERSONALITIES_LOC)

    def reset_storage(self):
        """
        Reset storage for personality insights.
        """
        self.storage_manager.reset_storage()

    def create_communication_prompt(self, personality_type: str, personality_name: str) -> str:
        """
        Create a detailed prompt for querying ChatGPT about a specific personality type.
        
        Args:
            personality_type (str): The MBTI code of the personality type.
            personality_name (str): The descriptive name of the personality type.
        
        Returns:
            str: The generated prompt.
        """
        return f"""
        Provide a thorough and holistic summary of the personality type {personality_type.upper()} ({personality_name}). 
        with a singular focus on their communication traits. Include the following aspects in detail::
        1. **Overall Communication Style:** Describe how this personality type generally 
        communicates, including their tone, approach, and preferences in conversations.
        2. **Key Strengths:** Highlight the main advantages of their communication style, 
        such as clarity, empathy, persuasion, or other unique traits.
        3. **Key Challenges:** Discuss potential drawbacks, such as tendencies that might 
        lead to misunderstandings, conflicts, or other communication hurdles.
        4. **Adaptability in Contexts:**
        - How this personality communicates in professional settings (e.g., teamwork, leadership, conflict resolution).
        - How they interact in personal relationships (e.g., family, friends, romantic partners).
        - How they behave in social settings (e.g., parties, casual gatherings).
        5. **Emotional and Logical Balance:** Analyze how they balance emotional expression and 
        logical reasoning in their communication.
        6. **Conflict Management:** Explore how this personality handles disagreements or 
        difficult conversations, and how their style influences conflict resolution outcomes.
        7. **Strengthening Communication:** Provide actionable tips or strategies for this 
        personality type to improve their communication and connect effectively with others.
        8. **Advice for Others:** Offer practical advice for individuals interacting with this 
        personality type to foster mutual understanding and effective communication.
        Ensure the response is detailed, balanced, and organized into clear sections, with no 
        strict word limit. Aim for the most comprehensive explanation possible within the 
        response size limit of the model. Use examples or scenarios if necessary to illustrate key points.
        """

    def inquire_all_personalities(self, topics: list) -> Dict[str, str]:
        """
        Iterates over all personalities and retrieves insights from ChatGPT for each.
        
        Args:
            topics (list): List of topics to inquire about.
        
        Returns:
            dict: A dictionary where keys are personality types and values are ChatGPT responses.
        """
        for code, name in self.personalities.items():
            insights = {}
            for topic in topics:
                if topic == TOPIC_COMMUNICATION:
                    prompt = self.create_communication_prompt(code, name)
                response = self.send_prompt(prompt)
                insights[topic] = response

            self.storage_manager.save_json(code, insights)
