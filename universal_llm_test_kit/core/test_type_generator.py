import json
import re
from ..models.model_interface import ModelInterface
from ..utils.prompt_templates import TEST_TYPE_GENERATOR_PROMPT


class TestTypeGenerator:
    def __init__(self, generator_model: ModelInterface):
        self.generator_model = generator_model

    def generate_test_types(self, num_test_types: int) -> list:
        # Format the prompt with the number of test types to generate
        prompt = TEST_TYPE_GENERATOR_PROMPT.format(num_test_types=num_test_types)
        # Generate test types using the generator model
        generated_data = self.generator_model.generate(prompt)
        return self.parse_generated_data(generated_data)

    def parse_generated_data(self, generated_data: str) -> list:
        # Try to find JSON array in the response
        json_match = re.search(r'\[.*\]', generated_data, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                # Attempt to parse the JSON string
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
                print(f"Problematic JSON string: {json_str[:100]}...")  # Print first 100 characters
        else:
            print("No JSON array found in the generated data.")

        # If no valid JSON is found or parsing fails, log the issue and return an empty list
        print(f"Raw generated data (first 100 characters): {generated_data[:100]}...")
        return []
