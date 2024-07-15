from ..models.model_interface import ModelInterface
from .test_case import TestCase
from ..utils.prompt_templates import TEST_EVALUATOR_PROMPT
import json
import re


class TestEvaluator:
    def __init__(self, evaluator_model: ModelInterface):
        self.evaluator_model = evaluator_model

    def evaluate_test(self, test_case: TestCase, model_output: str) -> dict:
        # Format the prompt with test case details and model output
        prompt = TEST_EVALUATOR_PROMPT.format(
            test_type=test_case.test_type,
            input_data=test_case.input_data,
            expected_output=test_case.expected_output,
            model_output=model_output
        )
        # Generate evaluation using the evaluator model
        evaluation_result = self.evaluator_model.generate(prompt)
        return self.parse_evaluation_result(evaluation_result)

    def parse_evaluation_result(self, evaluation_result: str) -> dict:
        # Try to find JSON object in the response
        json_match = re.search(r'\{.*\}', evaluation_result, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON: {json_str[:100]}...")  # Print first 100 characters

        print(f"No valid JSON found in the response. Attempting to extract information.")
        # If no JSON is found, attempt to extract information from the text
        score_match = re.search(r'score:\s*(\d+(\.\d+)?)', evaluation_result, re.IGNORECASE)
        score = float(score_match.group(1)) if score_match else 0.0

        reasoning_match = re.search(r'reasoning:(.+?)(?=suggestions:|$)', evaluation_result, re.IGNORECASE | re.DOTALL)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "No reasoning provided"

        suggestions_match = re.search(r'suggestions:(.+)', evaluation_result, re.IGNORECASE | re.DOTALL)
        suggestions = suggestions_match.group(1).strip() if suggestions_match else "No suggestions provided"

        # Return extracted information as a dictionary
        return {
            "score": score,
            "reasoning": reasoning,
            "suggestions": suggestions
        }
