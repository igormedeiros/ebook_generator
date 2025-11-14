import unittest
from unittest.mock import patch, MagicMock

# Temporarily add src to path to allow imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tools import (
    search_knowledge_base,
    retrieve_rag_context,
    count_words,
    validate_content_quality,
    validate_structure,
    format_markdown,
    generate_amazon_optimized_title,
    validate_title_seo,
    generate_outline,
    get_ideation_tools,
    get_all_tools,
)

class TestTools(unittest.TestCase):

    def test_count_words(self):
        """Test the word count tool."""
        self.assertEqual(count_words("Hello world"), 2)
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words("One"), 1)

    def test_format_markdown(self):
        """Test the markdown formatting tool."""
        title = "My Title"
        content = "This is the content."
        expected_output = f"# {title}\n\n{content}\n\n---"
        self.assertEqual(format_markdown(title, content), expected_output)

    def test_validate_content_quality(self):
        """Test the content quality validation tool."""
        short_content = "This is short."
        long_content = "This is a much longer content that should pass the validation with a good score. " * 5
        result_short = validate_content_quality(short_content)
        result_long = validate_content_quality(long_content)

        self.assertEqual(result_short['status'], 'too_short')
        self.assertEqual(result_long['status'], 'valid')
        self.assertGreater(result_long['word_count'], 100)

    def test_validate_structure(self):
        """Test the outline structure validation tool."""
        valid_outline = {
            "chapters": [
                {"title": "Introduction", "estimated_words": 100},
                {"title": "Main Content", "estimated_words": 500},
                {"title": "Conclusion", "estimated_words": 100},
            ]
        }
        invalid_outline = {"chapters": [{"title": "Only one chapter"}]}
        
        result_valid = validate_structure(valid_outline)
        result_invalid = validate_structure(invalid_outline)

        self.assertTrue(result_valid['structure_valid'])
        self.assertFalse(result_invalid['structure_valid'])
        self.assertIn('No introduction chapter found', result_invalid['issues'])

    def test_generate_amazon_optimized_title(self):
        """Test the Amazon KDP title generation tool."""
        topic = "Python Programming"
        audience = "Beginners"
        title = generate_amazon_optimized_title(topic, audience)
        self.assertIn(topic, title)
        self.assertIn(audience, title)

    def test_validate_title_seo(self):
        """Test the title SEO validation tool."""
        short_title = "Short"
        long_title = "This is a very long title that will definitely exceed the maximum length allowed for an SEO optimized title and should fail the validation."
        good_title = "A Complete Guide to Python for Beginners"

        self.assertFalse(validate_title_seo(short_title)['min_length_ok'])
        self.assertFalse(validate_title_seo(long_title)['max_length_ok'])
        self.assertTrue(validate_title_seo(good_title)['min_length_ok'])
        self.assertTrue(validate_title_seo(good_title)['max_length_ok'])
        self.assertTrue(validate_title_seo(good_title)['keyword_present'])

    def test_generate_outline(self):
        """Test the outline generation tool."""
        topic = "Test Topic"
        word_count = 10000
        text_outline, dict_outline = generate_outline(topic, word_count)

        self.assertIn(topic, text_outline)
        self.assertEqual(dict_outline['topic'], topic)
        self.assertEqual(len(dict_outline['chapters']), 5)
        self.assertEqual(dict_outline['target_words'], word_count)

    def test_get_ideation_tools(self):
        """Test that the ideation tools are returned correctly."""
        tools = get_ideation_tools()
        self.assertEqual(len(tools), 2)
        self.assertIn(search_knowledge_base, tools)
        self.assertIn(retrieve_rag_context, tools)

    def test_get_all_tools(self):
        """Test that all tools are returned."""
        tools = get_all_tools()
        self.assertGreater(len(tools), 20) # Check for a reasonable number of tools

    @patch('src.tools.supabase_client', None)
    def test_search_knowledge_base_no_supabase(self):
        """Test RAG search when Supabase is not configured."""
        result = search_knowledge_base("test query")
        self.assertIn("Supabase not configured", result)

    @patch('src.tools.supabase_client')
    def test_search_knowledge_base_with_supabase(self, mock_supabase_client):
        """Test RAG search with a mocked Supabase client."""
        mock_supabase_client.rpc.return_value.execute.return_value.data = [{'content': 'mock result'}]
        
        # Mock the embeddings as well
        with patch('src.tools.GoogleGenerativeAIEmbeddings') as mock_embeddings:
            mock_embeddings.return_value.embed_query.return_value = [0.1] * 768
            result = search_knowledge_base("test query")
            self.assertIn("Found 1 relevant documents", result)
            mock_supabase_client.rpc.assert_called_once()

if __name__ == '__main__':
    unittest.main()