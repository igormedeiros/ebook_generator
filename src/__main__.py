"""Entry point for Ebook Generator 1.0.

Loads specifications from specs/book.yaml (single source of truth) and executes 
the nine-stage editorial pipeline. Missing fields are collected via interactive 
terminal prompts.
"""

import sys

from .input_validator import validate_book_input
from .main import run_ebook_pipeline
from .config import get_logger, print_error_panel

logger = get_logger(__name__)


def main():
    """Load and validate book specs, then execute the ebook pipeline."""
    try:
        # Load and validate specs from specs/book.yaml
        # Missing fields will be prompted interactively
        book_config = validate_book_input()

        # Extract required parameters
        metadata = book_config.get("metadata", {})
        parameters = book_config.get("parameters", {})
        
        topic = metadata.get("topic")
        target_audience = metadata.get("target_audience")
        word_count_target = parameters.get("word_count_target", 15000)
        transformation_promise = parameters.get("transformation_promise", "")
        reading_level = parameters.get("reading_level", "intermediate")

        # Execute the pipeline
        result = run_ebook_pipeline(
            topic=topic,
            target_audience=target_audience,
            word_count_target=word_count_target,
            transformation_promise=transformation_promise,
            reading_level=reading_level,
            run_all_stages=True,
        )
        logger.info(f"Pipeline executado com sucesso. Status: {result.get('pipeline_status')}")

    except Exception as e:
        print_error_panel("Erro na Execução", str(e))
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
