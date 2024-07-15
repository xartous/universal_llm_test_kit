from abc import ABC, abstractmethod


class ModelInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response based on the given prompt.

        Args:
            prompt (str): The input prompt for the model.
            **kwargs: Additional keyword arguments that might be needed for specific model implementations.

        Returns:
            str: The generated response from the model.
        """
        pass
