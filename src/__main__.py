"""Entry point for Ebook Generator 1.0 CLI execution.

Enables running the pipeline via: python -m src
"""

import argparse
import sys

from .main import run_ebook_pipeline
from .config import get_logger

logger = get_logger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Ebook Generator 1.0 - Multi-agent editorial automation"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Python for Data Analysis",
        help="Book topic (default: Python for Data Analysis)",
    )
    parser.add_argument(
        "--audience",
        type=str,
        default="Data Scientists and Analysts",
        help="Target audience (default: Data Scientists and Analysts)",
    )
    parser.add_argument(
        "--word-count",
        type=int,
        default=20000,
        help="Target word count (default: 20000)",
    )
    parser.add_argument(
        "--promise",
        type=str,
        default="Master advanced data analysis techniques in Python",
        help="Transformation promise (optional)",
    )
    
    args = parser.parse_args()
    
    logger.info("Starting Ebook Generator pipeline...")
    logger.info(f"Topic: {args.topic}")
    logger.info(f"Audience: {args.audience}")
    logger.info(f"Word count target: {args.word_count}")
    
    result = run_ebook_pipeline(
        topic=args.topic,
        target_audience=args.audience,
        word_count_target=args.word_count,
        transformation_promise=args.promise,
    )
    
    if result.get("pipeline_status") == "completed":
        logger.info("✓ Pipeline completed successfully")
        return 0
    else:
        logger.error("✗ Pipeline failed")
        if "error" in result:
            logger.error(f"Error: {result['error']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
