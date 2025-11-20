import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import yaml

# Temporarily add src to path to allow imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from input_validator import SpecValidator, validate_book_input

class TestSpecValidator(unittest.TestCase):

    def setUp(self):
        """Set up a validator instance and mock dependencies."""
        self.mock_specs_dir = Path(__file__).parent / 'specs'
        
        # This patch points the SpecValidator to the test specs directory
        self.spec_file_patch = patch('src.input_validator.Path')
        self.mock_path = self.spec_file_patch.start()
        self.mock_path.return_value = self.mock_specs_dir / 'book.yaml'

        # We also need to patch the config loader to use our test config
        self.config_patch = patch('src.input_validator.get_config')
        self.mock_get_config = self.config_patch.start()
        self.mock_get_config.return_value = self._load_test_config()
        
        self.pipeline_config_patch = patch('src.input_validator.get_pipeline_config')
        self.mock_get_pipeline_config = self.pipeline_config_patch.start()
        self.mock_get_pipeline_config.return_value = {}

        self.validator = SpecValidator()
        # Point the validator to the correct test file after instantiation
        self.validator.spec_file = self.mock_specs_dir / 'book.yaml'


    def tearDown(self):
        """Stop all patches."""
        self.spec_file_patch.stop()
        self.config_patch.stop()
        self.pipeline_config_patch.stop()

    def _load_test_config(self):
        with open(self.mock_specs_dir / 'config.yaml', 'r') as f:
            return yaml.safe_load(f)

    def test_validate_field_value_valid(self):
        """Test _validate_field_value with valid data."""
        self.assertEqual(self.validator._validate_field_value('parameters_word_count_target', '50000'), 50000)
        self.assertEqual(self.validator._validate_field_value('parameters_reading_level', 'intermediate'), 'intermediate')
        self.assertEqual(self.validator._validate_field_value('metadata_topic', 'A great topic'), 'A great topic')

    def test_validate_field_value_invalid(self):
        """Test _validate_field_value with invalid data."""
        with self.assertRaises(ValueError):
            self.validator._validate_field_value('parameters_word_count_target', 'abc')
        with self.assertRaises(ValueError):
            self.validator._validate_field_value('parameters_word_count_target', '1000') # Too low
        with self.assertRaises(ValueError):
            self.validator._validate_field_value('parameters_reading_level', 'invalid_level')
        with self.assertRaises(ValueError):
            self.validator._validate_field_value('metadata_topic', '  ') # Empty

    @patch('src.input_validator.console.input')
    def test_prompt_for_field(self, mock_input):
        """Test the interactive prompt for a required field."""
        mock_input.return_value = "Test Value"
        value = self.validator._prompt_for_field('metadata_topic')
        self.assertEqual(value, "Test Value")
        mock_input.assert_called_once()

    @patch('src.input_validator.SpecValidator._prompt_for_field')
    @patch('src.input_validator.SpecValidator._prompt_optional_field')
    def test_validate_metadata_prompts_for_missing(self, mock_prompt_optional, mock_prompt):
        """Test that _validate_metadata prompts for missing mandatory fields."""
        mock_prompt.return_value = "Filled by prompt"
        mock_prompt_optional.return_value = "Optional Value"
        metadata = {'author_name': 'Test Author'} # Missing topic and target_audience
        
        validated_metadata = self.validator._validate_metadata(metadata)
        
        self.assertEqual(mock_prompt.call_count, 2)
        self.assertEqual(validated_metadata['topic'], "Filled by prompt")
        self.assertEqual(validated_metadata['target_audience'], "Filled by prompt")

    @patch('src.input_validator.SpecValidator._prompt_for_field')
    @patch('src.input_validator.SpecValidator._prompt_optional_field')
    def test_validate_parameters_prompts_for_missing(self, mock_prompt_optional, mock_prompt):
        """Test that _validate_parameters prompts for missing mandatory fields."""
        mock_prompt.return_value = "Filled by prompt"
        mock_prompt_optional.return_value = "Optional Value"
        parameters = {'word_count_target': 50000} # Missing transformation_promise
        
        validated_params = self.validator._validate_parameters(parameters)
        
        mock_prompt.assert_called_once_with('parameters_transformation_promise')
        self.assertEqual(validated_params['transformation_promise'], "Filled by prompt")

    @patch('builtins.open', new_callable=mock_open, read_data="metadata:\n  topic: 'Test Topic'")
    def test_load_spec_file_success(self, mock_file):
        """Test loading a valid spec file."""
        data = self.validator._load_spec_file()
        self.assertEqual(data['metadata']['topic'], 'Test Topic')

    def test_load_spec_file_not_found(self):
        """Test loading a non-existent spec file."""
        self.validator.spec_file = self.mock_specs_dir / 'non_existent.yaml'
        # The check is in validate(), not _load_spec_file(), so we test validate()
        with self.assertRaises(FileNotFoundError):
            self.validator.validate()

    @patch('builtins.open', new_callable=mock_open, read_data="invalid_yaml: [")
    def test_load_spec_file_yaml_error(self, mock_file):
        """Test loading a malformed spec file."""
        with self.assertRaises(ValueError):
            self.validator._load_spec_file()

    @patch('src.input_validator.SpecValidator._validate_metadata')
    @patch('src.input_validator.SpecValidator._validate_parameters')
    @patch('src.input_validator.SpecValidator._save_spec_file')
    def test_validate_orchestration(self, mock_save, mock_validate_params, mock_validate_metadata):
        """Test the main validate() method orchestration."""
        mock_validate_metadata.return_value = {'meta': 'data'}
        mock_validate_params.return_value = {'param': 'data'}
        
        # Create a temporary valid book.yaml for this test
        with open(self.validator.spec_file, 'w') as f:
            yaml.dump({'metadata': {}, 'parameters': {}}, f)

        result = self.validator.validate()

        mock_validate_metadata.assert_called_once()
        mock_validate_params.assert_called_once()
        mock_save.assert_called_once()
        self.assertIn('metadata', result)
        self.assertIn('parameters', result)

@patch('src.input_validator.SpecValidator')
def test_validate_book_input_calls_validator(MockSpecValidator):
    """Test that the main entry point uses the SpecValidator class."""
    instance = MockSpecValidator.return_value
    instance.validate.return_value = {"validated": True}
    
    result = validate_book_input()
    
    MockSpecValidator.assert_called_once()
    instance.validate.assert_called_once()
    assertEqual(result, {"validated": True})

# Helper for the standalone test function
def assertEqual(a, b):
    assert a == b

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)