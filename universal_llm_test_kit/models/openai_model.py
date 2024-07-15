from openai import OpenAI
from .model_interface import ModelInterface
import json


class OpenAIModel(ModelInterface):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        try:
            # Ensure the prompt is a string, not a dictionary or any other type
            if isinstance(prompt, dict):
                prompt = json.dumps(prompt)
            elif not isinstance(prompt, str):
                prompt = str(prompt)

            # Generate a response using the OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating response from OpenAI: {str(e)}")
            return ""
