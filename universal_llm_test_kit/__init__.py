from .models.model_interface import ModelInterface
from .models.openai_model import OpenAIModel
from .models.anthropic_model import AnthropicModel
from .core.test_case import TestCase
from .core.test_generator import TestGenerator
from .core.test_evaluator import TestEvaluator
from .core.test_type_generator import TestTypeGenerator

# File: universal_llm_test_kit/models/model_interface.py
from abc import ABC, abstractmethod

class ModelInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass