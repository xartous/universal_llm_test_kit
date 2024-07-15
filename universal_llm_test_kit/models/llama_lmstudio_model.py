from openai import OpenAI
from .model_interface import ModelInterface


class LlamaLMStudioModel(ModelInterface):
    def __init__(self, api_key: str = "lm-studio", model: str = "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
                 base_url: str = "http://localhost:1234/v1"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        try:
            # Generate a response using the LLaMA model through LM Studio
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return ""
