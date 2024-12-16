from openai import OpenAI
import os
from typing import Dict

from scrapers.config import PERSONALITIES, TOPIC_COMMUNICATION
from storage.storage import JSONDataManager
from storage.config import RAW, CHATGPT_COMMUNICATION_PERSONALITIES_LOC

class ChatGPT:
    """
    A Python wrapper for interacting with the OpenAI ChatGPT API.
    """

    def __init__(self, api_key=None, model="gpt-4o-mini"):
        """
        Initialize the ChatGPT class with the API key and model.
        Args:
            api_key (str): Your OpenAI API key. If None, it will look for an environment variable.
            model (str): The OpenAI model to use (default: gpt-3.5-turbo).
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in the OPENAI_API_KEY environment variable.")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def send_prompt(self, prompt, system_message="You are a helpful assistant."):
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

class PersonalityInsights(ChatGPT):
    """
    Extends the ChatGPT class to generate prompts and retrieve insights about personality types.
    """
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        """
        Initialize the PersonalityInsights class with the API key and model.
        Args:
            api_key (str): Your OpenAI API key. If None, it will look for an environment variable.
            model (str): The OpenAI model to use (default: gpt-3.5-turbo).
        """
        super().__init__(api_key, model)
        self.personalities = PERSONALITIES
    
    def create_storage_manager(self, topic):
        storage_manager = None
        if topic == TOPIC_COMMUNICATION:
            storage_manager = JSONDataManager(RAW, CHATGPT_COMMUNICATION_PERSONALITIES_LOC)
        return storage_manager

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

    def inquire_all_personalities(self, topic: str) -> Dict[str, str]:
        """
        Iterates over all personalities and retrieves insights from ChatGPT for each.
        Returns:
            dict: A dictionary where keys are personality types and values are ChatGPT responses.
        """
        insights = {}
        for code, name in self.personalities.items():
            prompt = ''
            if topic == TOPIC_COMMUNICATION:
                prompt = self.create_communication_prompt(code, name)
            response = self.send_prompt(prompt)
            insights[code] = response
        return insights
    
    def reset_topic_storage(self, topic: str):
        storage_manager = self.create_storage_manager(topic)
        storage_manager.reset_storage()

    def save_insights_to_json(self, insights: Dict[str, str]) -> None:
        """
        Save the personality insights to JSON files.
        Args:
            insights (dict): The personality insights dictionary.
        """
        storage_manager = self.create_storage_manager(TOPIC_COMMUNICATION)
        for ptype, summary in insights.items():
            storage_manager.save_json(ptype, {TOPIC_COMMUNICATION:summary})

    def main(self, topic: str):
        insights = self.inquire_all_personalities(topic)
        self.save_insights_to_json(insights)
