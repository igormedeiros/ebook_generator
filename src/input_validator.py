"""
Input validator for ebook generator book specifications.

Validates user-provided input/book_input.yaml against the system's configuration
schema and generates specs/book.yaml with merged defaults.

This module:
1. Loads input/book_input.yaml
2. Validates mandatory fields (topic, target_audience, word_count_target)
3. Validates field types and value ranges against specs/pipeline.yaml
4. Interactively prompts for missing or invalid fields
5. Merges with defaults from specs/pipeline.yaml
6. Generates specs/book.yaml for pipeline execution
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

from config import (
    get_logger,
    get_pipeline_config,
    get_config,
    console,
    print_panel,
)

logger = get_logger(__name__)


class InputValidator:
    """
    Validates and processes book input specifications.
    
    Validates input/book_input.yaml and generates specs/book.yaml with proper
    type checking, range validation, and interactive prompts for missing fields.
    """

    # Mandatory fields that must be provided by user
    MANDATORY_FIELDS = ["topic", "target_audience", "word_count_target"]

    # Optional fields with defaults
    OPTIONAL_FIELDS = {
        "transformation_promise": None,
        "reading_level": "intermediate",
        "stage_overrides": {},
        "author_name": None,
        "author_bio": None,
        "publication_year": None,
    }

    def __init__(self):
        """Initialize the input validator with configuration."""
        self.pipeline_config = get_pipeline_config()
        self.config_messages = get_config()
        self.input_file = Path("input/book_input.yaml")
        self.output_file = Path("specs/book.yaml")

    def validate(self) -> Dict[str, Any]:
        """
        Validate input and generate book configuration.
        
        Returns:
            dict: Validated and merged book configuration ready for pipeline
            
        Raises:
            FileNotFoundError: If input/book_input.yaml does not exist
            ValueError: If validation fails and user doesn't complete interactive prompts
        """
        logger.info("Iniciando validação de entrada")

        # Check if input file exists
        if not self.input_file.exists():
            logger.warning(f"Arquivo {self.input_file} não encontrado")
            return self._create_interactive_input()

        # Load and validate user input
        user_input = self._load_input_file()
        validated = self._validate_fields(user_input)

        # Merge with defaults from pipeline config
        merged = self._merge_with_defaults(validated)

        # Save generated configuration
        self._save_book_config(merged)

        logger.info("Validação concluída com sucesso")
        return merged

    def _load_input_file(self) -> Dict[str, Any]:
        """
        Load input/book_input.yaml file.
        
        Returns:
            dict: Loaded YAML content
            
        Raises:
            ValueError: If file is malformed YAML
        """
        try:
            with open(self.input_file, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)
                return content if content else {}
        except yaml.YAMLError as e:
            logger.error(f"Erro ao processar YAML: {str(e)}")
            raise ValueError(f"Arquivo YAML inválido: {str(e)}")

    def _validate_fields(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user input fields against schema.
        
        Args:
            user_input: Dictionary from input/book_input.yaml
            
        Returns:
            dict: Validated input (completes missing mandatory fields interactively)
        """
        validated = {}

        # Validate each mandatory field
        for field in self.MANDATORY_FIELDS:
            if field in user_input and user_input[field]:
                # Field provided, validate type and range
                value = user_input[field]
                validated[field] = self._validate_field_value(field, value)
            else:
                # Field missing, prompt user
                logger.warning(f"Campo obrigatório ausente: {field}")
                validated[field] = self._prompt_for_field(field)

        # Process optional fields
        for field, default in self.OPTIONAL_FIELDS.items():
            if field in user_input and user_input[field]:
                validated[field] = self._validate_field_value(field, user_input[field])
            else:
                validated[field] = default

        # Add any additional fields from user input that aren't in our schema
        for key, value in user_input.items():
            if key not in validated:
                validated[key] = value

        return validated

    def _validate_field_value(self, field: str, value: Any) -> Any:
        """
        Validate individual field value against schema.
        
        Args:
            field: Field name to validate
            value: Value to validate
            
        Returns:
            Any: Validated value
            
        Raises:
            ValueError: If validation fails
        """
        # Type validation
        if field == "word_count_target":
            if not isinstance(value, int):
                raise ValueError(f"{field} deve ser um número inteiro")
            # Range check from pipeline config
            stage_cfg = self.pipeline_config.get("stages", {}).get("stage_1_ideation", {})
            params = stage_cfg.get("parameters", {})
            word_count_param = params.get("word_count_target", {})
            min_val = word_count_param.get("minimum", 5000)
            max_val = word_count_param.get("maximum", 100000)
            if not (min_val <= value <= max_val):
                raise ValueError(
                    f"{field} deve estar entre {min_val} e {max_val} "
                    f"(recebido: {value})"
                )

        elif field == "reading_level":
            valid_levels = ["beginner", "intermediate", "advanced"]
            if value not in valid_levels:
                raise ValueError(
                    f"{field} deve ser um de: {', '.join(valid_levels)} "
                    f"(recebido: {value})"
                )

        elif field == "topic":
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field} deve ser uma string não vazia")

        elif field == "target_audience":
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field} deve ser uma string não vazia")

        return value

    def _prompt_for_field(self, field: str) -> str:
        """
        Interactively prompt user for a field value.
        
        Args:
            field: Field name to prompt for
            
        Returns:
            str: User-provided value
        """
        messages = get_config()
        prompts = messages.get("input_prompts", {})

        # Get field-specific prompt
        prompt_key = f"prompt_{field}"
        prompt_text = prompts.get(prompt_key, f"Digite o valor para {field}:")

        # Show prompt and get input
        while True:
            value = console.input(f"\n[cyan]{prompt_text}[/cyan] ")
            if value.strip():
                try:
                    self._validate_field_value(field, value)
                    return value.strip()
                except ValueError as e:
                    logger.warning(f"Valor inválido: {str(e)}")
                    console.print(f"[red]❌ {str(e)}[/red]")
            else:
                logger.warning(f"Campo {field} não pode estar vazio")
                console.print("[red]❌ Este campo é obrigatório[/red]")

    def _create_interactive_input(self) -> Dict[str, Any]:
        """
        Create input interactively when input file doesn't exist.
        
        Returns:
            dict: User-provided configuration
        """
        logger.info("Criando entrada interativa")
        print_panel(
            title="Novo Projeto de E-book",
            content="Vou guiá-lo através da criação de um novo e-book",
            style="cyan",
        )

        validated = {}

        # Prompt for mandatory fields
        for field in self.MANDATORY_FIELDS:
            validated[field] = self._prompt_for_field(field)

        # Prompt for optional fields
        for field, default in self.OPTIONAL_FIELDS.items():
            prompt_key = f"prompt_{field}"
            prompts = get_config().get("input_prompts", {})
            prompt_text = prompts.get(prompt_key)

            if prompt_text:
                response = console.input(f"\n[yellow]{prompt_text}[/yellow] [dim](opcional)[/dim] ")
                if response.strip():
                    validated[field] = response.strip()
                else:
                    validated[field] = default
            else:
                validated[field] = default

        # Save input for future reference
        self._save_input_file(validated)

        # Merge with defaults
        merged = self._merge_with_defaults(validated)

        # Save generated config
        self._save_book_config(merged)

        return merged

    def _merge_with_defaults(self, validated: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge validated input with system defaults from pipeline config.
        
        Args:
            validated: Validated user input
            
        Returns:
            dict: Merged configuration with all defaults
        """
        # Start with stage defaults
        merged = {
            "metadata": {
                "topic": validated.get("topic"),
                "target_audience": validated.get("target_audience"),
                "author_name": validated.get("author_name"),
                "author_bio": validated.get("author_bio"),
                "publication_year": validated.get("publication_year"),
            },
            "parameters": {
                "word_count_target": validated.get("word_count_target", 50000),
                "reading_level": validated.get("reading_level", "intermediate"),
                "transformation_promise": validated.get("transformation_promise"),
            },
            "stages": {},
        }

        # Merge stage configurations with defaults
        pipeline_stages = self.pipeline_config.get("stages", {})
        stage_overrides = validated.get("stage_overrides", {})

        for stage_name, stage_config in pipeline_stages.items():
            # Use user override if provided, otherwise use default
            if stage_name in stage_overrides:
                merged["stages"][stage_name] = stage_overrides[stage_name]
            else:
                merged["stages"][stage_name] = stage_config.copy()

        return merged

    def _save_input_file(self, data: Dict[str, Any]) -> None:
        """
        Save validated input to input/book_input.yaml for future reference.
        
        Args:
            data: Dictionary to save
        """
        self.input_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.input_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        logger.info(f"Entrada salva em {self.input_file}")

    def _save_book_config(self, data: Dict[str, Any]) -> None:
        """
        Save generated book configuration to specs/book.yaml.
        
        Args:
            data: Merged configuration dictionary
        """
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        logger.info(f"Configuração gerada em {self.output_file}")


def validate_book_input() -> Dict[str, Any]:
    """
    Validate book input and return merged configuration.
    
    This is the main entry point for input validation. It:
    1. Loads input/book_input.yaml (or creates interactively)
    2. Validates all fields against schema
    3. Prompts for missing mandatory fields
    4. Merges with defaults from specs/pipeline.yaml
    5. Generates specs/book.yaml
    
    Returns:
        dict: Complete validated book configuration ready for pipeline
        
    Example:
        >>> config = validate_book_input()
        >>> config['metadata']['topic']
        'Python para Análise de Dados'
        >>> config['parameters']['word_count_target']
        50000
    """
    validator = InputValidator()
    return validator.validate()
