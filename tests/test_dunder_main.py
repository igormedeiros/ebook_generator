import unittest
from unittest.mock import patch, MagicMock

# Temporarily add src to path to allow imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# The module to test
from src import __main__ as dunder_main

class TestDunderMain(unittest.TestCase):

    @patch('src.__main__.validate_book_input')
    @patch('src.__main__.run_ebook_pipeline')
    def test_main_success_flow(self, mock_run_pipeline, mock_validate_input):
        """Test the successful execution flow of the main script."""
        mock_config = {
            "metadata": {
                "topic": "Test Topic",
                "target_audience": "Test Audience",
            },
            "parameters": {
                "word_count_target": 5000,
                "transformation_promise": "Test Promise",
                "reading_level": "beginner",
            }
        }
        mock_validate_input.return_value = mock_config
        mock_run_pipeline.return_value = {"pipeline_status": "completed"}

        dunder_main.main()

        mock_validate_input.assert_called_once()
        mock_run_pipeline.assert_called_once_with(
            topic="Test Topic",
            target_audience="Test Audience",
            word_count_target=5000,
            transformation_promise="Test Promise",
            reading_level="beginner",
            run_all_stages=True
        )

    @patch('src.__main__.validate_book_input', side_effect=Exception("Validation Failed"))
    @patch('src.__main__.print_error_panel')
    @patch('sys.exit')
    def test_main_exception_handling(self, mock_exit, mock_print_error, mock_validate_input):
        """Test the exception handling in the main script."""
        dunder_main.main()

        mock_print_error.assert_called_once_with("Erro na Execução", "Validation Failed")
        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
