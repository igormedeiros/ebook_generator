"""Command line entry-point for the ebook generator pipeline."""

from __future__ import annotations

import sys

from .config import print_error_panel
from .input_validator import validate_book_input
from .pipeline import generate_ebook as run_ebook_pipeline


def main() -> None:
    """Validate user input and execute the ebook pipeline."""

    try:
        book_config = validate_book_input()
        metadata = book_config.get("metadata", {})
        parameters = book_config.get("parameters", {})

        run_ebook_pipeline(
            topic=metadata.get("topic", ""),
            target_audience=metadata.get("target_audience", ""),
            word_count_target=parameters.get("word_count_target", 10000),
            transformation_promise=parameters.get("transformation_promise"),
            reading_level=parameters.get("reading_level"),
            run_all_stages=True,
        )
    except Exception as exc:  # noqa: BLE001
        print_error_panel("Erro na Execução", str(exc))
        sys.exit(1)


if __name__ == "__main__":
    main()
