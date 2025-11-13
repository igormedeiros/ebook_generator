""""""

Input validator for ebook generator book specifications.Input validator for ebook generator book specifications.



Loads specs/book.yaml (the single source of truth) and validates all fields.Loads specs/book.yaml (the single source of truth) and validates all fields.

Missing or empty fields are collected via interactive terminal prompts.Missing or empty fields are collected via interactive terminal prompts.



This module:This module:

1. Loads specs/book.yaml1. Loads specs/book.yaml

2. Checks for empty/null fields in metadata and parameters2. Checks for empty/null fields in metadata and parameters

3. Validates field types and value ranges3. Validates field types and value ranges against specs/pipeline.yaml

4. Interactively prompts for missing or invalid fields4. Interactively prompts for missing or invalid fields

5. Updates specs/book.yaml with validated data5. Updates specs/book.yaml with validated data

6. Returns complete configuration ready for pipeline execution6. Returns complete configuration ready for pipeline execution

""""""



from pathlib import Pathimport os

from typing import Dict, Any, Optionalfrom pathlib import Path

import yamlfrom typing import Dict, Any, Optional

import yaml

from .config import (

    get_logger,from .config import (

    get_pipeline_config,    get_logger,

    get_config,    get_pipeline_config,

    console,    get_config,

)    console,

    print_panel,

logger = get_logger(__name__))



logger = get_logger(__name__)

class SpecValidator:

    """

    Validates and processes book specifications from specs/book.yaml.class SpecValidator:

        """

    Loads specs/book.yaml (single source of truth) and prompts for any    Validates and processes book specifications from specs/book.yaml.

    missing/empty fields interactively with proper type checking and validation.    

    """    Loads specs/book.yaml (single source of truth) and prompts for any

    missing/empty fields interactively with proper type checking and validation.

    # Fields that are considered mandatory (must have non-null value)    """

    MANDATORY_METADATA = ["topic", "target_audience", "author_name"]

    MANDATORY_PARAMS = ["word_count_target", "transformation_promise"]    # Fields that are considered mandatory (must have non-null value)

    MANDATORY_METADATA = ["topic", "target_audience", "author_name"]

    def __init__(self):    MANDATORY_PARAMS = ["word_count_target", "transformation_promise"]

        """Initialize the specification validator."""

        self.pipeline_config = get_pipeline_config()    def __init__(self):

        self.config_messages = get_config()        """Initialize the specification validator."""

        self.spec_file = Path("specs/book.yaml")        self.pipeline_config = get_pipeline_config()

        self.config_messages = get_config()

    def validate(self) -> Dict[str, Any]:        self.spec_file = Path("specs/book.yaml")

        """

        Validate specs/book.yaml and fill missing fields interactively.    def validate(self) -> Dict[str, Any]:

                """

        Returns:        Validate specs/book.yaml and fill missing fields interactively.

            dict: Complete validated book configuration ready for pipeline        

                    Returns:

        Raises:            dict: Complete validated book configuration ready for pipeline

            FileNotFoundError: If specs/book.yaml does not exist            

        """        Raises:

        logger.info("Carregando e validando specs/book.yaml")            FileNotFoundError: If specs/book.yaml does not exist

        """

        if not self.spec_file.exists():        logger.info("Carregando e validando specs/book.yaml")

            raise FileNotFoundError(f"Arquivo {self.spec_file} não encontrado")

        if not self.spec_file.exists():

        # Load current specs            raise FileNotFoundError(f"Arquivo {self.spec_file} não encontrado")

        spec_data = self._load_spec_file()

                # Load current specs

        # Validate and fill missing metadata fields        spec_data = self._load_spec_file()

        spec_data["metadata"] = self._validate_metadata(spec_data.get("metadata", {}))        

                # Validate and fill missing metadata fields

        # Validate and fill missing parameter fields        spec_data["metadata"] = self._validate_metadata(spec_data.get("metadata", {}))

        spec_data["parameters"] = self._validate_parameters(spec_data.get("parameters", {}))        

        # Validate and fill missing parameter fields

        # Save updated specs        spec_data["parameters"] = self._validate_parameters(spec_data.get("parameters", {}))

        self._save_spec_file(spec_data)

        # Save updated specs

        logger.info("Validação de specs concluída com sucesso")        self._save_spec_file(spec_data)

        return spec_data

        logger.info("Validação de specs concluída com sucesso")

    def _load_spec_file(self) -> Dict[str, Any]:        return spec_data

        """

        Load specs/book.yaml file.    def _load_spec_file(self) -> Dict[str, Any]:

                """

        Returns:        Load specs/book.yaml file.

            dict: Loaded YAML content        

        """        Returns:

        try:            dict: Loaded YAML content

            with open(self.spec_file, "r", encoding="utf-8") as f:        """

                content = yaml.safe_load(f)        try:

                return content if content else {}            with open(self.spec_file, "r", encoding="utf-8") as f:

        except yaml.YAMLError as e:                content = yaml.safe_load(f)

            logger.error(f"Erro ao processar YAML: {str(e)}")                return content if content else {}

            raise ValueError(f"Arquivo YAML inválido: {str(e)}")        except yaml.YAMLError as e:

            logger.error(f"Erro ao processar YAML: {str(e)}")

    def _validate_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:            raise ValueError(f"Arquivo YAML inválido: {str(e)}")

        """        try:

        Validate and complete metadata fields.            with open(self.input_file, "r", encoding="utf-8") as f:

                        content = yaml.safe_load(f)

        Args:                return content if content else {}

            metadata: Current metadata dictionary        except yaml.YAMLError as e:

                        logger.error(f"Erro ao processar YAML: {str(e)}")

        Returns:            raise ValueError(f"Arquivo YAML inválido: {str(e)}")

            dict: Validated metadata with all fields filled

        """    def _validate_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:

        validated = metadata.copy() if metadata else {}        """

        Validate and complete metadata fields.

        # Check and prompt for missing mandatory metadata        

        for field in self.MANDATORY_METADATA:        Args:

            if not validated.get(field):            metadata: Current metadata dictionary

                logger.warning(f"Campo obrigatório faltando: metadata.{field}")            

                validated[field] = self._prompt_for_field(f"metadata_{field}")        Returns:

            dict: Validated metadata with all fields filled

        # Check optional metadata fields        """

        optional_metadata = ["author_bio", "publication_year"]        validated = metadata.copy() if metadata else {}

        for field in optional_metadata:

            if field not in validated or not validated[field]:        # Check and prompt for missing mandatory metadata

                response = self._prompt_optional_field(f"metadata_{field}")        for field in self.MANDATORY_METADATA:

                if response:            if not validated.get(field):

                    validated[field] = response                logger.warning(f"Campo obrigatório faltando: metadata.{field}")

                validated[field] = self._prompt_for_field(f"metadata_{field}")

        return validated

        # Check optional metadata fields

    def _validate_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:        optional_metadata = ["author_bio", "publication_year"]

        """        for field in optional_metadata:

        Validate and complete parameters fields.            if field not in validated or not validated[field]:

                        response = self._prompt_optional_field(f"metadata_{field}")

        Args:                if response:

            parameters: Current parameters dictionary                    validated[field] = response

            

        Returns:        return validated

            dict: Validated parameters with all fields filled

        """    def _validate_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:

        validated = parameters.copy() if parameters else {}        """

        Validate and complete parameters fields.

        # Check mandatory parameters        

        for field in self.MANDATORY_PARAMS:        Args:

            if not validated.get(field):            parameters: Current parameters dictionary

                logger.warning(f"Campo obrigatório faltando: parameters.{field}")            

                validated[field] = self._prompt_for_field(f"parameters_{field}")        Returns:

            dict: Validated parameters with all fields filled

        # Ensure reading_level has a value        """

        if "reading_level" not in validated or not validated["reading_level"]:        validated = parameters.copy() if parameters else {}

            validated["reading_level"] = "intermediate"

        # Check mandatory parameters

        return validated        for field in self.MANDATORY_PARAMS:

            if not validated.get(field):

    def _validate_field_value(self, field: str, value: Any) -> Any:                logger.warning(f"Campo obrigatório faltando: parameters.{field}")

        """                validated[field] = self._prompt_for_field(f"parameters_{field}")

        Validate individual field value against schema.

                # Ensure reading_level has a value

        Args:        if "reading_level" not in validated or not validated["reading_level"]:

            field: Full field path (e.g., "parameters_word_count_target")            validated["reading_level"] = "intermediate"

            value: Value to validate

                    return validated

        Returns:

            Any: Validated value    def _validate_field_value(self, field: str, value: Any) -> Any:

                    """

        Raises:        Validate individual field value against schema.

            ValueError: If validation fails        

        """        Args:

        # Extract field name without prefix            field: Full field path (e.g., "parameters_word_count_target")

        field_name = field.split("_", 1)[1] if "_" in field else field            value: Value to validate

            

        # Type validation        Returns:

        if field_name == "word_count_target":            Any: Validated value

            # Convert string to int if necessary            

            if isinstance(value, str):        Raises:

                try:            ValueError: If validation fails

                    value = int(value)        """

                except ValueError:        # Extract field name without prefix

                    raise ValueError(f"word_count_target deve ser um número inteiro")        field_name = field.split("_", 1)[1] if "_" in field else field

            

            if not isinstance(value, int):        # Type validation

                raise ValueError(f"word_count_target deve ser um número inteiro")        if field_name == "word_count_target":

                        # Convert string to int if necessary

            # Range check: 5000-100000            if isinstance(value, str):

            if not (5000 <= value <= 100000):                try:

                raise ValueError(f"word_count_target deve estar entre 5000 e 100000")                    value = int(value)

                except ValueError:

        elif field_name == "reading_level":                    raise ValueError(f"word_count_target deve ser um número inteiro")

            valid_levels = ["beginner", "intermediate", "advanced", "expert"]            

            if value not in valid_levels:            if not isinstance(value, int):

                raise ValueError(                raise ValueError(f"word_count_target deve ser um número inteiro")

                    f"reading_level deve ser um de: {', '.join(valid_levels)}"            

                )            # Range check: 5000-100000

            if not (5000 <= value <= 100000):

        elif field_name in ["topic", "target_audience", "transformation_promise", "author_name", "author_bio"]:                raise ValueError(f"word_count_target deve estar entre 5000 e 100000")

            if not isinstance(value, str) or not value.strip():

                raise ValueError(f"{field_name} deve ser uma string não vazia")        elif field_name == "reading_level":

            valid_levels = ["beginner", "intermediate", "advanced", "expert"]

        return value            if value not in valid_levels:

                raise ValueError(

    def _prompt_for_field(self, field: str) -> str:                    f"reading_level deve ser um de: {', '.join(valid_levels)}"

        """                )

        Interactively prompt user for a required field value.

                elif field_name in ["topic", "target_audience", "transformation_promise", "author_name", "author_bio"]:

        Args:            if not isinstance(value, str) or not value.strip():

            field: Field name to prompt for (e.g., "metadata_topic")                raise ValueError(f"{field_name} deve ser uma string não vazia")

            

        Returns:        return value

            str: User-provided value

        """    def _prompt_for_field(self, field: str) -> str:

        messages = get_config()        """

        prompts = messages.get("input_prompts", {})        Interactively prompt user for a required field value.

        

        # Get field-specific prompt        Args:

        prompt_key = f"prompt_{field}"            field: Field name to prompt for (e.g., "metadata_topic")

        prompt_text = prompts.get(prompt_key, f"Digite o valor para {field}:")            

        Returns:

        # Show prompt and get input            str: User-provided value

        while True:        """

            value = console.input(f"\n[cyan]{prompt_text}[/cyan] ")        messages = get_config()

            if value.strip():        prompts = messages.get("input_prompts", {})

                try:

                    validated_value = self._validate_field_value(field, value)        # Get field-specific prompt

                    return validated_value if isinstance(validated_value, str) else str(validated_value)        prompt_key = f"prompt_{field}"

                except ValueError as e:        prompt_text = prompts.get(prompt_key, f"Digite o valor para {field}:")

                    logger.warning(f"Valor inválido: {str(e)}")

                    console.print(f"[red]❌ {str(e)}[/red]")        # Show prompt and get input

            else:        while True:

                logger.warning(f"Campo {field} não pode estar vazio")            value = console.input(f"\n[cyan]{prompt_text}[/cyan] ")

                console.print("[red]❌ Este campo é obrigatório[/red]")            if value.strip():

                try:

    def _prompt_optional_field(self, field: str) -> Optional[str]:                    self._validate_field_value(field, value)

        """                    return value.strip()

        Interactively prompt user for an optional field value.                except ValueError as e:

                            logger.warning(f"Valor inválido: {str(e)}")

        Args:                    console.print(f"[red]❌ {str(e)}[/red]")

            field: Field name to prompt for (e.g., "metadata_author_bio")            else:

                            logger.warning(f"Campo {field} não pode estar vazio")

        Returns:                console.print("[red]❌ Este campo é obrigatório[/red]")

            Optional[str]: User-provided value or None if skipped

        """    def _create_interactive_input(self) -> Dict[str, Any]:

        messages = get_config()        """

        prompts = messages.get("input_prompts", {})        Create input interactively when input file doesn't exist.

        

        # Get field-specific prompt        Returns:

        prompt_key = f"prompt_{field}"            dict: User-provided configuration

        prompt_text = prompts.get(prompt_key, f"Digite o valor para {field} (opcional):")        """

        logger.info("Criando entrada interativa")

        value = console.input(f"\n[yellow]{prompt_text}[/yellow] [dim](deixe em branco para pular)[/dim] ")        print_panel(

        if value.strip():            title="Novo Projeto de E-book",

            try:            content="Vou guiá-lo através da criação de um novo e-book",

                return self._validate_field_value(field, value)            style="cyan",

            except ValueError as e:        )

                logger.warning(f"Valor inválido: {str(e)}")

                console.print(f"[yellow]⚠️  {str(e)} - usando valor padrão[/yellow]")        validated = {}

                return None

        return None        # Prompt for mandatory fields

        for field in self.MANDATORY_FIELDS:

    def _save_spec_file(self, data: Dict[str, Any]) -> None:            validated[field] = self._prompt_for_field(field)

        """

        Save validated specifications to specs/book.yaml.        # Prompt for optional fields

                for field, default in self.OPTIONAL_FIELDS.items():

        Args:            prompt_key = f"prompt_{field}"

            data: Complete specification dictionary            prompts = get_config().get("input_prompts", {})

        """            prompt_text = prompts.get(prompt_key)

        self.spec_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.spec_file, "w", encoding="utf-8") as f:            if prompt_text:

            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)                response = console.input(f"\n[yellow]{prompt_text}[/yellow] [dim](opcional)[/dim] ")

        logger.info(f"Especificações salvas em {self.spec_file}")                if response.strip():

                    validated[field] = response.strip()

                else:

def validate_book_input() -> Dict[str, Any]:                    validated[field] = default

    """            else:

    Validate specs/book.yaml and return complete configuration.                validated[field] = default

    

    This is the main entry point for specification validation. It:        # Save input for future reference

    1. Loads specs/book.yaml (single source of truth)        self._save_input_file(validated)

    2. Checks for empty/null fields

    3. Validates all fields against schema        # Merge with defaults

    4. Prompts for missing mandatory fields interactively        merged = self._merge_with_defaults(validated)

    5. Updates specs/book.yaml with validated data

    6. Returns complete configuration ready for pipeline        # Save generated config

            self._save_book_config(merged)

    Returns:

        dict: Complete validated book configuration        return merged

        

    Example:    def _merge_with_defaults(self, validated: Dict[str, Any]) -> Dict[str, Any]:

        >>> config = validate_book_input()        """

        >>> config['metadata']['topic']        Merge validated input with system defaults from pipeline config.

        'Python para Análise de Dados'        

        >>> config['parameters']['word_count_target']        Args:

        15000            validated: Validated user input

    """            

    validator = SpecValidator()        Returns:

    return validator.validate()            dict: Merged configuration with all defaults

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
    validator = SpecValidator()
    return validator.validate()
