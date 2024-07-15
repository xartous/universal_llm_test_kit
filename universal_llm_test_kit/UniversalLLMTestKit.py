from typing import List, Dict, Any
from universal_llm_test_kit.models.model_interface import ModelInterface
from universal_llm_test_kit.models.openai_model import OpenAIModel
from universal_llm_test_kit.models.anthropic_model import AnthropicModel
from universal_llm_test_kit.models.llama_lmstudio_model import LlamaLMStudioModel
from universal_llm_test_kit.core.test_generator import TestGenerator
from universal_llm_test_kit.core.test_evaluator import TestEvaluator
from universal_llm_test_kit.core.test_type_generator import TestTypeGenerator
from universal_llm_test_kit.utils import prompt_templates


class UniversalLLMTestKit:
    def __init__(self,
                 test_model: ModelInterface,
                 generator_model: ModelInterface,
                 evaluator_model: ModelInterface):
        # Initialize the test kit with different models for each task
        self.test_model = test_model
        self.test_generator = TestGenerator(generator_model)
        self.test_evaluator = TestEvaluator(evaluator_model)
        self.test_type_generator = TestTypeGenerator(generator_model)

    def generate_test_types(self, num_test_types: int) -> List[Dict[str, Any]]:
        # Generate a specified number of test types
        return self.test_type_generator.generate_test_types(num_test_types)

    def run_test_suite(self, test_configs: List[Dict[str, Any]], custom_instructions: str = "") -> List[Dict[str, Any]]:
        results = []
        for config in test_configs:
            try:
                # Generate test case
                test_case = self.test_generator.generate_test(config['test_type'], config['parameters'],
                                                              custom_instructions)

                # Run test using the test model
                model_output = self.test_model.generate(test_case.input_data)

                # Evaluate the test results
                evaluation = self.test_evaluator.evaluate_test(test_case, model_output)

                results.append({
                    'test_type': config['test_type'],
                    'parameters': config['parameters'],
                    'test_case': test_case,
                    'model_output': model_output,
                    'evaluation': evaluation
                })
            except Exception as e:
                print(f"Error in test case for {config['test_type']}: {str(e)}")
                results.append({
                    'test_type': config['test_type'],
                    'parameters': config['parameters'],
                    'error': str(e)
                })
        return results

    def set_custom_prompt_template(self, prompt_type: str, template: str):
        # Set a custom prompt template for a specific prompt type
        if hasattr(prompt_templates, prompt_type):
            setattr(prompt_templates, prompt_type, template)
        else:
            raise ValueError(f"Unknown prompt type: {prompt_type}")

    def add_custom_test_type(self, name: str, description: str, default_parameters: Dict[str, Any]):
        # This method could be used to add predefined test types
        # Implementation depends on how you want to store and use custom test types
        pass

    def set_model_for_task(self, task: str, model: ModelInterface):
        # Set a specific model for a given task
        if task == 'test':
            self.test_model = model
        elif task == 'generate':
            self.test_generator = TestGenerator(model)
            self.test_type_generator = TestTypeGenerator(model)
        elif task == 'evaluate':
            self.test_evaluator = TestEvaluator(model)
        else:
            raise ValueError(f"Unknown task: {task}")