from dataclasses import dataclass
from typing import Any

@dataclass
class TestCase:
    """
    Represents a single test case for language model evaluation.
    """
    input_data: Any  # The input data for the test
    expected_output: Any  # The expected output or behavior
    test_type: str  # The type or category of the test

    def __post_init__(self):
        """
        Perform basic validation after initialization.
        """
        if not isinstance(self.test_type, str) or not self.test_type:
            raise ValueError("test_type must be a non-empty string")