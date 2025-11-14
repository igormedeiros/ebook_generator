import unittest
from unittest.mock import patch, MagicMock

# Temporarily add src to path to allow imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.config import (
    print_panel,
    print_table,
    print_stage_header,
    print_pipeline_start,
    print_error_panel,
)

class TestTUIOutput(unittest.TestCase):

    @patch('src.config.console')
    def test_print_panel(self, mock_console):
        """Test the print_panel function."""
        print_panel("Test Title", "Test Content")
        mock_console.print.assert_called_once()
        # Check that the first argument to print is a Panel
        from rich.panel import Panel
        self.assertIsInstance(mock_console.print.call_args[0][0], Panel)

    @patch('src.config.console')
    def test_print_table(self, mock_console):
        """Test the print_table function."""
        print_table("Test Table", ["Header1"], [["Row1"]])
        mock_console.print.assert_called_once()
        # Check that the first argument to print is a Table
        from rich.table import Table
        self.assertIsInstance(mock_console.print.call_args[0][0], Table)

    @patch('src.config.console')
    def test_print_stage_header(self, mock_console):
        """Test the print_stage_header function."""
        print_stage_header(1, "Test Stage", "Test Description")
        mock_console.print.assert_called_once()
        from rich.panel import Panel
        self.assertIsInstance(mock_console.print.call_args[0][0], Panel)

    @patch('src.config.console')
    def test_print_pipeline_start(self, mock_console):
        """Test the print_pipeline_start function."""
        print_pipeline_start("Test Topic", "Test Audience", 1000)
        # It prints a panel and then a newline
        self.assertEqual(mock_console.print.call_count, 2)
        from rich.panel import Panel
        self.assertIsInstance(mock_console.print.call_args_list[0][0][0], Panel)

    @patch('src.config.console')
    def test_print_error_panel(self, mock_console):
        """Test the print_error_panel function."""
        print_error_panel("Test Error", "Error Message")
        mock_console.print.assert_called_once()
        from rich.panel import Panel
        self.assertIsInstance(mock_console.print.call_args[0][0], Panel)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
