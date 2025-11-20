import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import tempfile
from pathlib import Path

from src.pipeline import generate_ebook, save_ebook


class TestPipeline(unittest.TestCase):
    """Tests for the main ebook generation pipeline."""

    def setUp(self):
        """Set up test environment."""
        os.environ['GOOGLE_API_KEY'] = 'test-api-key'
        
    def tearDown(self):
        """Clean up test environment."""
        if 'GOOGLE_API_KEY' in os.environ:
            del os.environ['GOOGLE_API_KEY']

    @patch('src.pipeline.load_brd')
    @patch('src.pipeline.generate_chapter_structure')
    @patch('src.pipeline.generate_introduction')
    @patch('src.pipeline.generate_chapter_research')
    @patch('src.pipeline.generate_chapter_content')
    @patch('src.pipeline.initialize_ebook_file')
    @patch('src.pipeline.append_chapter_to_ebook')
    @patch('src.pipeline.get_confirmation')
    @patch('src.pipeline.print_header')
    @patch('src.pipeline.print_info')
    @patch('src.pipeline.print_separator')
    @patch('src.pipeline.print_ebook_info')
    @patch('src.pipeline.print_chapters_preview')
    @patch('src.pipeline.print_phase_header')
    @patch('src.pipeline.print_success_message')
    @patch('src.pipeline.print_error_message')
    def test_generate_ebook_test_mode(self, *mocks):
        """Test ebook generation in test mode."""
        # Mock BRD
        mock_load_brd = mocks[-1]
        mock_load_brd.return_value = {
            'project': {
                'name': 'Test Ebook',
                'description': 'Test Description',
                'target_audience': 'Test Audience',
                'word_count_target': 1000,
                'number_chapters': 2
            },
            'content_structure': {},
            'writing_style': {}
        }
        
        # Mock confirmations to always return True
        mock_get_confirmation = mocks[8]
        mock_get_confirmation.return_value = True
        
        # Mock introduction
        mock_generate_introduction = mocks[-3]
        mock_generate_introduction.return_value = "Test introduction content"
        
        # Mock file operations
        mock_initialize = mocks[10]
        mock_append = mocks[9]
        
        # Run in test mode
        result = generate_ebook(test_mode=True)
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertIn('title', result)
        self.assertIn('chapters', result)
        self.assertEqual(result['title'], 'Test Ebook')
        
        # Verify mocks were called
        mock_load_brd.assert_called_once()
        mock_initialize.assert_called_once()

    @patch('src.pipeline.load_brd')
    @patch('src.pipeline.generate_chapter_structure')
    @patch('src.pipeline.print_header')
    @patch('src.pipeline.print_info')
    @patch('src.pipeline.print_separator')
    @patch('src.pipeline.print_error_message')
    def test_generate_ebook_empty_chapters(self, *mocks):
        """Test ebook generation when chapter structure generation fails."""
        # Mock BRD
        mock_load_brd = mocks[-1]
        mock_load_brd.return_value = {
            'project': {
                'name': 'Test Ebook',
                'description': 'Test Description',
                'target_audience': 'Test Audience',
                'word_count_target': 1000
            },
            'content_structure': {},
            'writing_style': {}
        }
        
        # Mock empty chapter structure
        mock_generate_structure = mocks[-2]
        mock_generate_structure.return_value = []
        
        # Run pipeline
        result = generate_ebook(test_mode=False)
        
        # Should return None when chapters fail to generate
        self.assertIsNone(result)

    @patch('src.pipeline.load_brd')
    @patch('src.pipeline.generate_conclusion')
    @patch('src.pipeline.generate_glossary')
    @patch('src.pipeline.generate_bibliography')
    @patch('builtins.open', new_callable=mock_open, read_data='# Test\n[Palavras Finais]\n[Glossário]\n[Referências Bibliográficas]')
    @patch('src.pipeline.print_info')
    @patch('src.pipeline.print_success_message')
    def test_save_ebook(self, mock_success, mock_info, mock_file, mock_biblio, mock_glossary, mock_conclusion, mock_load_brd):
        """Test saving ebook with all sections."""
        # Mock BRD
        mock_load_brd.return_value = {
            'project': {
                'name': 'Test Ebook',
                'description': 'Test Description'
            }
        }
        
        # Mock ebook data
        ebook = {
            'title': 'Test Ebook',
            'description': 'Test Description',
            'chapters': [
                {'name': 'Chapter 1', 'content': 'Content 1'},
                {'name': 'Chapter 2', 'content': 'Content 2'}
            ]
        }
        
        # Mock content generators
        mock_conclusion.return_value = "Test conclusion"
        mock_glossary.return_value = "Test glossary"
        mock_biblio.return_value = "Test bibliography"
        
        # Save ebook
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_ebook.md"
            result = save_ebook(ebook, output_file=str(output_file), test_mode=True)
        
        # Verify generators were called
        mock_conclusion.assert_called_once()
        mock_glossary.assert_called_once()
        mock_biblio.assert_called_once()

    @patch('src.pipeline.load_brd')
    @patch('src.pipeline.generate_chapter_structure')
    @patch('src.pipeline.get_confirmation')
    @patch('src.pipeline.print_header')
    @patch('src.pipeline.print_info')
    @patch('src.pipeline.print_separator')
    @patch('src.pipeline.print_ebook_info')
    @patch('src.pipeline.print_chapters_preview')
    def test_generate_ebook_user_cancellation(self, *mocks):
        """Test ebook generation when user cancels."""
        # Mock BRD
        mock_load_brd = mocks[-1]
        mock_load_brd.return_value = {
            'project': {
                'name': 'Test Ebook',
                'description': 'Test Description',
                'target_audience': 'Test Audience',
                'word_count_target': 1000
            },
            'content_structure': {},
            'writing_style': {}
        }
        
        # Mock chapter structure
        mock_generate_structure = mocks[-2]
        mock_generate_structure.return_value = [
            {'name': 'Chapter 1', 'purpose': 'Test', 'elements': []}
        ]
        
        # Mock user cancellation
        mock_get_confirmation = mocks[-3]
        mock_get_confirmation.return_value = False
        
        # Run pipeline
        result = generate_ebook(test_mode=False)
        
        # Should return None when user cancels
        self.assertIsNone(result)


class TestPipelineHelpers(unittest.TestCase):
    """Tests for pipeline helper functions."""

    @patch('src.pipeline.load_brd')
    def test_load_brd(self, mock_load):
        """Test BRD loading."""
        from src.pipeline import load_brd
        
        mock_load.return_value = {'project': {'name': 'Test'}}
        result = load_brd()
        
        self.assertIsNotNone(result)
        self.assertIn('project', result)

    def test_count_words(self):
        """Test word counting function."""
        from src.pipeline import count_words
        
        # Test normal text
        self.assertEqual(count_words("hello world"), 2)
        self.assertEqual(count_words("one two three four"), 4)
        
        # Test empty text
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words(None), 0)
        
        # Test markdown
        markdown_text = "# Title\n\nThis is a **bold** text."
        self.assertEqual(count_words(markdown_text), 6)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)