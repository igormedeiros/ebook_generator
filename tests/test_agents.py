import unittest
from unittest.mock import patch, MagicMock, call
from pathlib import Path
import yaml

from src.agents import (
    create_ideation_agent,
    create_technical_reviewer_agent,
    execute_agent,
    execute_review_personas,
)

class TestAgents(unittest.TestCase):

    def setUp(self):
        """Set up mock model and configs."""
        self.mock_model = MagicMock()
        
        # Load mock agent specs from our test file
        mock_specs_dir = Path(__file__).parent / 'specs'
        with open(mock_specs_dir / 'agents.yaml', 'r') as f:
            self.mock_agents_config = yaml.safe_load(f)

    @patch('src.agents.get_agents_config')
    @patch('src.agents.create_agent')
    @patch('src.agents.get_ideation_tools')
    def test_create_ideation_agent(self, mock_get_tools, mock_create_agent, mock_get_config):
        """Test the creation of the ideation agent."""
        mock_get_config.return_value = {"main_pipeline_agents": {"ideation_agent": {"system_prompt": "You are the Agente de Ideação - Estrategista Criativo."}}}
        mock_get_tools.return_value = [MagicMock()] # Dummy tool
        
        create_ideation_agent(self.mock_model)
        
        mock_create_agent.assert_called_once()
        args, kwargs = mock_create_agent.call_args
        self.assertEqual(kwargs['model'], self.mock_model)
        self.assertEqual(len(kwargs['tools']), 1)
        self.assertIn("You are the Agente de Ideação - Estrategista Criativo.", kwargs['system_prompt'])

    @patch('src.agents.get_personas_config')
    @patch('src.agents.create_agent')
    @patch('src.agents.get_review_tools')
    def test_create_technical_reviewer_agent(self, mock_get_tools, mock_create_agent, mock_get_config):
        """Test the creation of a review persona agent."""
        mock_get_config.return_value = {"review_personas": {"technical_reviewer": {}}}
        mock_get_tools.return_value = [MagicMock()]
        
        create_technical_reviewer_agent(self.mock_model)
        
        mock_create_agent.assert_called_once()
        args, kwargs = mock_create_agent.call_args
        self.assertEqual(kwargs['model'], self.mock_model)
        self.assertIn("You are technical_reviewer", kwargs['system_prompt'])

    def test_execute_agent_success(self):
        """Test executing an agent successfully."""
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {"messages": [MagicMock(content="Agent response")]}
        
        response = execute_agent(mock_agent, "Test query")
        
        self.assertEqual(response, "Agent response")
        mock_agent.invoke.assert_called_once_with({"messages": [{"role": "user", "content": "Test query"}]}, config={"callbacks": [unittest.mock.ANY]})

    def test_execute_agent_error(self):
        """Test handling an error during agent execution."""
        mock_agent = MagicMock()
        mock_agent.invoke.side_effect = Exception("Something went wrong")
        
        response = execute_agent(mock_agent, "Test query")
        
        self.assertIn("Error executing agent: Something went wrong", response)

    @patch('src.agents.execute_agent')
    def test_execute_review_personas(self, mock_execute_agent):
        """Test the execution of multiple review personas."""
        mock_execute_agent.side_effect = ["Feedback from reviewer 1", "Feedback from reviewer 2"]
        
        personas = {
            "reviewer_1": MagicMock(),
            "reviewer_2": MagicMock(),
        }
        
        feedback = execute_review_personas(MagicMock(), "Content to review", personas)
        
        self.assertEqual(len(feedback), 2)
        self.assertEqual(feedback['reviewer_1'], "Feedback from reviewer 1")
        self.assertEqual(feedback['reviewer_2'], "Feedback from reviewer 2")
        
        # Check that execute_agent was called for each persona
        self.assertEqual(mock_execute_agent.call_count, 2)
        calls = [
            call(personas['reviewer_1'], "[reviewer_1] Review and provide specialized feedback:\n\nContent to review"),
            call(personas['reviewer_2'], "[reviewer_2] Review and provide specialized feedback:\n\nContent to review")
        ]
        mock_execute_agent.assert_has_calls(calls)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)