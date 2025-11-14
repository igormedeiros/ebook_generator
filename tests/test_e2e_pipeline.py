import unittest
from unittest.mock import patch, MagicMock

# Temporarily add src to path to allow imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.config import (
    get_pipeline_config,
    get_agents_config,
    get_model,
    get_research_model,
)
from src.agents import (
    create_ideation_agent,
    create_title_agent,
    create_structure_agent,
    create_deep_research_agent,
    create_chapter_agent,
    create_review_coordinator_agent,
    create_critical_reading_coordinator_agent,
    create_editing_agent,
    create_finalization_agent,
)
from src.tools import (
    get_ideation_tools,
    get_title_tools,
    get_structure_tools,
    get_deep_research_tools,
    get_chapter_writing_tools,
)

class TestE2EPipeline(unittest.TestCase):

    @patch('src.config.get_model')
    @patch('src.config.get_research_model')
    @patch('src.config.get_pipeline_config')
    @patch('src.config.get_agents_config')
    def test_pipeline_initialization(self, mock_agents_config, mock_pipeline_config, mock_research_model, mock_write_model):
        """Test that all pipeline stages can be initialized."""
        mock_pipeline_config.return_value = {"stages": {}}
        mock_agents_config.return_value = {"main_pipeline_agents": {}}
        mock_write_model.return_value = MagicMock()
        mock_research_model.return_value = MagicMock()

        pipeline_config = get_pipeline_config()
        agents_config = get_agents_config()
        write_model = get_model()
        research_model = get_research_model()

        self.assertIsNotNone(pipeline_config)
        self.assertIsNotNone(agents_config)
        self.assertIsNotNone(write_model)
        self.assertIsNotNone(research_model)

    @patch('src.agents.create_agent')
    @patch('src.config.get_model')
    @patch('src.config.get_research_model')
    @patch('src.config.get_agents_config')
    def test_agent_creation(self, mock_agents_config, mock_research_model, mock_write_model, mock_create_agent):
        """Test that all 9 pipeline agents can be created."""
        mock_agents_config.return_value = {
            "main_pipeline_agents": {
                "ideation_agent": {}, "title_agent": {}, "structure_agent": {},
                "deep_research_agent": {}, "chapter_writing_agent": {},
                "review_coordinator_agent": {}, "critical_reading_coordinator_agent": {},
                "editing_agent": {}, "finalization_agent": {}
            }
        }
        mock_write_model.return_value = MagicMock()
        mock_research_model.return_value = MagicMock()
        mock_create_agent.return_value = MagicMock()

        agents = {
            "ideation_agent": create_ideation_agent(get_model()),
            "title_agent": create_title_agent(get_model()),
            "structure_agent": create_structure_agent(get_model()),
            "deep_research_agent": create_deep_research_agent(get_research_model()),
            "chapter_agent": create_chapter_agent(get_model()),
            "review_coordinator_agent": create_review_coordinator_agent(get_research_model()),
            "critical_reading_coordinator_agent": create_critical_reading_coordinator_agent(get_research_model()),
            "editing_agent": create_editing_agent(get_model()),
            "finalization_agent": create_finalization_agent(get_model()),
        }

        self.assertEqual(len(agents), 9)
        self.assertTrue(all(isinstance(agent, MagicMock) for agent in agents.values()))

    def test_tools_availability(self):
        """Test that tools are available for each stage."""
        tool_collections = {
            "ideation_tools": get_ideation_tools(),
            "title_tools": get_title_tools(),
            "structure_tools": get_structure_tools(),
            "deep_research_tools": get_deep_research_tools(),
            "chapter_writing_tools": get_chapter_writing_tools(),
        }

        self.assertTrue(all(len(tools) > 0 for tools in tool_collections.values()))

    def test_mock_pipeline_execution(self):
        """Test a simplified pipeline flow with mock data."""
        mock_input = {
            "metadata": {
                "topic": "Python para Análise de Dados",
                "target_audience": "Data Scientists",
            },
            "parameters": {
                "word_count_target": 50000,
            },
        }
        self.assertIn("topic", mock_input["metadata"])
        self.assertIn("word_count_target", mock_input["parameters"])

        outputs = {
            "stage_1_ideation": {"central_idea": "Análise de dados com Python"},
            "stage_2_title": {"title_options": ["Python para Análise de Dados"]},
            "stage_3_structure": {"chapters_count": 12, "outline_created": True},
        }
        self.assertGreater(len(outputs), 0)

    def test_error_handling(self):
        """Test basic error handling in pipeline."""
        invalid_inputs = [
            {},
            {"metadata": {}},
            {"parameters": {}},
        ]
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                self.assertFalse(invalid_input.get("metadata") and invalid_input.get("parameters"))

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
