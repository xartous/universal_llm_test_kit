# run_tests.py
from universal_llm_test_kit.UniversalLLMTestKit import UniversalLLMTestKit
from universal_llm_test_kit.models.openai_model import OpenAIModel
from universal_llm_test_kit.models.anthropic_model import AnthropicModel
from universal_llm_test_kit.models.llama_lmstudio_model import LlamaLMStudioModel
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    try:
        # Setup models (replace with your actual API keys)
        openai_model = OpenAIModel(api_key="your_openai_api_key")
        anthropic_model = AnthropicModel(api_key="your_anthropic_api_key")
        llama_model = LlamaLMStudioModel() # runs locally for tests

        # Initialize the test kit
        test_kit = UniversalLLMTestKit(llama_model, openai_model, anthropic_model)

        # Generate test types
        test_types = test_kit.generate_test_types(num_test_types=2)
        logger.info("Generated Test Types:")
        for test_type in test_types:
            logger.info(f"Name: {test_type['name']}")
            logger.info(f"Description: {test_type['description']}")
            logger.info(f"Parameters: {test_type['parameters']}")
            logger.info("---")

        # Define test configurations
        test_configs = [
            {
                'test_type': 'controlled_fake_detection',
                'parameters': {
                    'subtlety': 'high',
                    'content_type': 'social_media_post',
                    'target_group': 'random',
                    'length': 200
                }
            },
            {
                'test_type': 'logical_reasoning',
                'parameters': {
                    'difficulty': 'medium',
                    'domain': 'scientific_analysis'
                }
            }
        ]

        # Add custom instructions
        custom_instructions = """
        Generate challenging but ethically neutral test cases. Focus on testing the model's ability to understand context, 
        provide accurate information, summarize content, and generate creative responses.
        """

        # Run tests
        results = test_kit.run_test_suite(test_configs, custom_instructions)

        # Process and analyze results
        for result in results:
            logger.info(f"Test Type: {result['test_type']}")
            logger.info(f"Parameters: {result['parameters']}")
            if 'error' in result:
                logger.error(f"Error: {result['error']}")
            else:
                logger.info(f"Test Case Input: {result['test_case'].input_data}")
                logger.info(f"Model Output: {result['model_output']}")
                logger.info(f"Evaluation: {result['evaluation']}")
            logger.info("---")

        # Example of setting a custom prompt template
        test_kit.set_custom_prompt_template('TEST_GENERATOR_PROMPT',
                                            "Your custom prompt here: {test_type}, {parameters}, {custom_instructions}")

        # Example of setting a different model for a specific task
        test_kit.set_model_for_task('evaluate', anthropic_model)

    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
