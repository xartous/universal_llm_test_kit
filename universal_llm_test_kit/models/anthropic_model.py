from anthropic import Anthropic
from .model_interface import ModelInterface

class AnthropicModel(ModelInterface):
    def __init__(self, api_key: str, model: str = "claude-2"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        # Generate a response using the Anthropic API
        response = self.client.completions.create(
            model=self.model,
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            max_tokens_to_sample=1000,
            **kwargs
        )
        return response.completion