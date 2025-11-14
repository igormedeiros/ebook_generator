import unittest
from unittest.mock import patch, MagicMock

# Temporarily add src to path to allow imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# We need to import the __main__ to test the entry point
from src import __main__ as dunder_main

class TestIntegrationPipeline(unittest.TestCase):

    @patch('src.__main__.validate_book_input')
    @patch('src.__main__.run_ebook_pipeline')
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_api_key'})
    def test_pipeline_integration_with_mocks(self, mock_run_pipeline, mock_validate_input):
        """
        Test the integration of the main script with the pipeline, using mocks.
        This test simulates the behavior of the original integration test but without
        making real API calls.
        """
        # Mock the input validation to return a sample config
        mock_config = {
            "metadata": {
                "topic": "Mock Topic",
                "target_audience": "Mock Audience",
            },
            "parameters": {
                "word_count_target": 1000,
                "transformation_promise": "Mock Promise",
                "reading_level": "beginner",
            }
        }
        mock_validate_input.return_value = mock_config

        # Mock the pipeline result
        mock_run_pipeline.return_value = {"pipeline_status": "completed"}

        # Run the main function from __main__
        dunder_main.main()

        # Assert that the validation was called
        mock_validate_input.assert_called_once()

        # Assert that the pipeline was called with the correct parameters
        mock_run_pipeline.assert_called_once_with(
            topic="Mock Topic",
            target_audience="Mock Audience",
            word_count_target=1000,
            transformation_promise="Mock Promise",
            reading_level="beginner",
            run_all_stages=True
        )

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
