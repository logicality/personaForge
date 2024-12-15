from openai import OpenAI
import os

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
