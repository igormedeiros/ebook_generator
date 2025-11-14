import unittest
from unittest.mock import patch, MagicMock, call

# Temporarily add src to path to allow imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from main import run_ebook_pipeline, _build_review_persona_agents, _build_virtual_reader_agents

class TestMainPipeline(unittest.TestCase):

    @patch('src.main.get_model')
    @patch('src.main.get_research_model')
    @patch('src.main.get_config')
    @patch('src.main.get_message')
    @patch('src.main.print_pipeline_start')
    @patch('src.main.print_stage_header')
    @patch('src.main.print_stage_complete')
    @patch('src.main.print_pipeline_complete')
    @patch('src.main.create_ideation_agent')
    @patch('src.main.create_title_agent')
    @patch('src.main.create_structure_agent')
    @patch('src.main.create_deep_research_agent')
    @patch('src.main.create_chapter_agent')
    @patch('src.main.create_review_coordinator_agent')
    @patch('src.main.create_critical_reading_coordinator_agent')
    @patch('src.main.create_editing_agent')
    @patch('src.main.create_finalization_agent')
    @patch('src.main.create_publication_agent')
    @patch('src.main.execute_agent')
    @patch('src.main.execute_review_personas')
    def test_run_full_pipeline(self, mock_execute_review, mock_execute_agent, *args):
        """Test a full run of the ebook pipeline."""
        # Mock the return values of agent executions
        mock_execute_agent.side_effect = [
            "ideation_output",
            "title_output",
            "structure_output",
            "deep_research_output",
            "chapter_output",
            "editing_output",
            "finalization_output",
            "publication_output",
        ]
        mock_execute_review.side_effect = ["review_output", "critical_reading_output"]

        # Mock config loader
        mock_get_config = args[10]
        mock_get_config.return_value = {
            "agent_prompts": {
                "ideation_prompt_template": "{topic}",
                "title_prompt_template": "{ideation_output}",
                "structure_prompt_template": "{topic}",
                "deep_research_prompt_template": "{structure_output}",
                "chapter_writing_prompt_template": "{structure_output}",
                "review_prompt_template": "{chapter_output}",
                "critical_reading_prompt_template": "{review_output}",
                "editing_prompt_template": "{critical_output}",
                "finalization_prompt_template": "{editing_output}",
                "publication_prompt_template": "{editing_output_excerpt}",
            }
        }

        results = run_ebook_pipeline(
            topic="Test Topic",
            target_audience="Test Audience",
            word_count_target=1000,
            run_all_stages=True
        )

        self.assertEqual(results['pipeline_status'], 'completed')
        self.assertEqual(mock_execute_agent.call_count, 8)
        self.assertEqual(mock_execute_review.call_count, 2)
        self.assertIn('stage_1_ideation', results)
        self.assertIn('stage_9_publication', results)

    @patch('src.main.get_model')
    @patch('src.main.get_research_model')
    @patch('src.main.get_config')
    @patch('src.main.get_message')
    @patch('src.main.print_pipeline_start')
    @patch('src.main.print_stage_header')
    @patch('src.main.print_stage_complete')
    @patch('src.main.create_ideation_agent')
    @patch('src.main.execute_agent')
    def test_run_partial_pipeline(self, mock_execute_agent, mock_create_ideation_agent, *args):
        """Test running only the first stage of the pipeline."""
        mock_execute_agent.return_value = "ideation_output"
        mock_get_config = args[5]
        mock_get_config.return_value = {"agent_prompts": {"ideation_prompt_template": "{topic}"}}

        results = run_ebook_pipeline(
            topic="Test Topic",
            target_audience="Test Audience",
            run_all_stages=False
        )

        self.assertEqual(results['pipeline_status'], 'partial')
        mock_execute_agent.assert_called_once()
        self.assertIn('stage_1_ideation', results)
        self.assertNotIn('stage_2_title', results)

    @patch('src.main.get_model', side_effect=Exception("Test Exception"))
    @patch('src.main.print_error_panel')
    def test_pipeline_exception_handling(self, mock_print_error, mock_get_model):
        """Test the pipeline's main exception handling."""
        results = run_ebook_pipeline("Test", "Test")
        self.assertEqual(results['pipeline_status'], 'error')
        self.assertEqual(results['error'], 'Test Exception')
        mock_print_error.assert_called_once()

    @patch('src.main.create_technical_reviewer_agent')
    def test_build_review_persona_agents(self, mock_create_agent):
        """Test the construction of review persona agents."""
        agents = _build_review_persona_agents(MagicMock(), MagicMock())
        self.assertIn("Technical Reviewer", agents)
        self.assertEqual(mock_create_agent.call_count, 1) # Only one is mocked

    @patch('src.main.create_curious_beginner_agent')
    def test_build_virtual_reader_agents(self, mock_create_agent):
        """Test the construction of virtual reader agents."""
        agents = _build_virtual_reader_agents(MagicMock(), MagicMock())
        self.assertIn("Curious Beginner", agents)
        self.assertEqual(mock_create_agent.call_count, 1)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)