import unittest
from unittest.mock import patch, mock_open, MagicMock
import yaml
from pathlib import Path

from src.config import (
    load_yaml_config,
    get_config,
    get_message,
    get_pipeline_config,
    get_models_config,
    get_personas_config,
    get_tools_config,
    get_agents_config,
    get_agent_for_stage,
    get_model,
    get_research_model
)

class TestConfig(unittest.TestCase):

    @patch('src.config.SPECS_DIR', Path(__file__).parent / 'specs')
    def test_load_yaml_config_success(self):
        """Test loading a valid YAML file."""
        config = load_yaml_config('test_config.yaml')
        self.assertIn('messages', config)
        self.assertEqual(config['messages']['pipeline_start'], 'Iniciando o pipeline...')

    @patch('src.config.SPECS_DIR', Path(__file__).parent / 'specs')
    def test_load_yaml_config_not_found(self):
        """Test that FileNotFoundError is raised for a missing file."""
        with self.assertRaises(FileNotFoundError):
            load_yaml_config('non_existent_file.yaml')

    @patch('src.config.SPECS_DIR', Path(__file__).parent / 'specs')
    def test_load_yaml_config_yaml_error(self):
        """Test that YAMLError is raised for a malformed file."""
        with patch('builtins.open', mock_open(read_data='invalid_yaml: [')):
            with self.assertRaises(yaml.YAMLError):
                load_yaml_config('any_file.yaml')

    @patch('src.config.load_yaml_config')
    def test_get_config_section(self, mock_load_yaml):
        """Test getting a specific section from the main config."""
        mock_load_yaml.return_value = {
            'messages': {'greeting': 'Hello'},
            'labels': {'name': 'Name'}
        }
        messages = get_config('messages')
        self.assertEqual(messages, {'greeting': 'Hello'})
        mock_load_yaml.assert_called_once_with('config.yaml')

    @patch('src.config.get_config')
    def test_get_message(self, mock_get_config):
        """Test getting a localized message."""
        mock_get_config.return_value = {'pipeline_start': 'Pipeline has started'}
        message = get_message('pipeline_start')
        self.assertEqual(message, 'Pipeline has started')
        mock_get_config.assert_called_once_with('messages')

    @patch('src.config.load_yaml_config')
    def test_get_pipeline_config(self, mock_load_yaml):
        """Test getting the pipeline config."""
        get_pipeline_config()
        mock_load_yaml.assert_called_once_with('pipeline.yaml')

    @patch('src.config.load_yaml_config')
    def test_get_models_config(self, mock_load_yaml):
        """Test getting the models config."""
        get_models_config()
        mock_load_yaml.assert_called_once_with('models.yaml')

    @patch('src.config.load_yaml_config')
    def test_get_personas_config(self, mock_load_yaml):
        """Test getting the personas config."""
        get_personas_config()
        mock_load_yaml.assert_called_once_with('personas.yaml')

    @patch('src.config.load_yaml_config')
    def test_get_tools_config(self, mock_load_yaml):
        """Test getting the tools config."""
        get_tools_config()
        mock_load_yaml.assert_called_once_with('tools.yaml')

    @patch('src.config.load_yaml_config')
    def test_get_agents_config(self, mock_load_yaml):
        """Test getting the agents config."""
        get_agents_config()
        mock_load_yaml.assert_called_once_with('agents.yaml')

    @patch('src.config.get_pipeline_config')
    def test_get_agent_for_stage(self, mock_get_pipeline_config):
        """Test getting the agent for a specific stage."""
        mock_get_pipeline_config.return_value = {
            'stages': {
                'stage_1_document_spec': {
                    'agent': 'document_spec_agent'
                }
            }
        }
        agent = get_agent_for_stage('stage_1_document_spec')
        self.assertEqual(agent, 'document_spec_agent')

    @patch('src.config.get_pipeline_config')
    def test_get_agent_for_stage_not_found(self, mock_get_pipeline_config):
        """Test that ValueError is raised for a non-existent stage."""
        mock_get_pipeline_config.return_value = {'stages': {}}
        with self.assertRaises(ValueError):
            get_agent_for_stage('non_existent_stage')

    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_api_key'})
    @patch('src.config.ChatGoogleGenerativeAI')
    def test_get_model_success(self, mock_chat_model):
        """Test getting the writing model successfully."""
        mock_model_instance = MagicMock()
        mock_model_instance.model_name = 'gemini-2.5-flash'
        mock_chat_model.return_value = mock_model_instance

        model = get_model()
        self.assertIsNotNone(model)
        self.assertEqual(model.model_name, 'gemini-2.5-flash')

    @patch.dict('os.environ', {}, clear=True)
    def test_get_model_no_api_key(self):
        """Test that ValueError is raised when GOOGLE_API_KEY is not set."""
        with self.assertRaises(ValueError):
            get_model()

    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_api_key'})
    @patch('src.config.ChatGoogleGenerativeAI')
    def test_get_research_model_success(self, mock_chat_model):
        """Test getting the research model successfully."""
        mock_model_instance = MagicMock()
        mock_model_instance.model_name = 'gemini-2.5-pro'
        mock_chat_model.return_value = mock_model_instance

        model = get_research_model()
        self.assertIsNotNone(model)
        self.assertEqual(model.model_name, 'gemini-2.5-pro')

    @patch.dict('os.environ', {}, clear=True)
    def test_get_research_model_no_api_key(self):
        """Test that ValueError is raised when GOOGLE_API_KEY is not set for the research model."""
        with self.assertRaises(ValueError):
            get_research_model()

if __name__ == '__main__':
    unittest.main()