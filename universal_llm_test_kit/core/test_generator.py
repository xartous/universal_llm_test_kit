from ..models.model_interface import ModelInterface
from .test_case import TestCase
from ..utils.prompt_templates import TEST_GENERATOR_PROMPT
import json


class TestGenerator:
    def __init__(self, generator_model: ModelInterface):
        self.generator_model = generator_model

    def generate_test(self, test_type: str, parameters: dict, custom_instructions: str = "") -> TestCase:
        # Format the prompt with test type, parameters, and custom instructions
        prompt = TEST_GENERATOR_PROMPT.format(
            test_type=test_type,
            parameters=json.dumps(parameters, indent=2),
            custom_instructions=custom_instructions
        )
        # Generate test data using the generator model
        generated_data = self.generator_model.generate(prompt)
        return self.parse_generated_data(generated_data, test_type)

    def parse_generated_data(self, generated_data: str, test_type: str) -> TestCase:
        try:
            # Attempt to parse the generated data as JSON
            data = json.loads(generated_data)

            # Create and return a TestCase object
            return TestCase(
                input_data=data.get('input_data', "Error: Missing input_data"),
                expected_output=data.get('expected_output', "Error: Missing expected_output"),
                test_type=test_type
            )
        except json.JSONDecodeError as e:
            # Handle JSON parsing errors
            print(f"Failed to parse JSON: {str(e)}")
            print(f"Raw data (first 100 characters): {generated_data[:100]}...")

            # Return a TestCase with error information
            return TestCase(
                input_data=f"Error: Invalid JSON format. Raw data: {generated_data[:100]}...",
                expected_output="Error: Could not parse generated data",
                test_type=test_type
            )
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error while parsing generated data: {str(e)}")
            return TestCase(
                input_data="Error: Unexpected error occurred",
                expected_output=f"Error: {str(e)}",
                test_type=test_type
            )