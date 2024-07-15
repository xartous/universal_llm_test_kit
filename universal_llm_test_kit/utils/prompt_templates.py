# Template for generating test types
TEST_TYPE_GENERATOR_PROMPT = """
Generate {num_test_types} unique test types for evaluating language models. Each test type should focus on a different aspect of model performance or potential issues.

For each test type, provide:
1. A name for the test type
2. A brief description of what the test evaluates
3. Key parameters that can be adjusted for this test type

IMPORTANT: Provide the output ONLY as a JSON array, with no additional text before or after. The format should be exactly as follows:
[
  {{
    "name": "test_type_name",
    "description": "Brief description of the test",
    "parameters": {{
      "param1": "description of param1",
      "param2": "description of param2"
    }}
  }},
  ...
]
"""

# Template for generating test cases
TEST_GENERATOR_PROMPT = """
You are an AI model tasked with generating test cases for evaluating language models. Your role is to create challenging and diverse tests that focus on linguistic abilities, knowledge, and reasoning skills. 

Generate a test case for the following test type and parameters:

Test Type: {test_type}
Parameters: {parameters}

Additional instructions:
{custom_instructions}

IMPORTANT: Your response must be ONLY a valid JSON object with the following structure, with no additional text before or after:
{{
    "input_data": <input data for the test, focusing on neutral but challenging content>,
    "expected_output": <expected output or behavior>
}}

Ensure that the test cases are challenging but do not involve sensitive, controversial, or potentially harmful content. Focus on testing language understanding, knowledge application, and reasoning abilities.
"""

# Template for evaluating test results
TEST_EVALUATOR_PROMPT = """
Evaluate the model's output for the following test case:

Test Type: {test_type}
Input Data: {input_data}
Expected Output: {expected_output}
Model Output: {model_output}

IMPORTANT: Your response must be ONLY a valid JSON object with the following structure, with no additional text before or after:
{{
    "score": <numeric score between 0 and 1>,
    "reasoning": <explanation for the score>,
    "suggestions": <suggestions for improvement>
}}
"""