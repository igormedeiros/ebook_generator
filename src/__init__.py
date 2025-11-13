"""
Ebook Generator 1.0 - Multi-agent editorial automation platform.
Transforms raw ideas into publication-ready ebooks using LangChain 1.0+ and Gemini 2.5.

9-Stage Pipeline with Specialized Agents and Iterative Review:
1. Ideation - Central idea, problem definition, target audience
2. Title Generation - Amazon-optimized title options
3. Structure & Outline - Hierarchical table of contents
4A. Deep Research - Context7 MCP queries, vectorization, RAG integration
4B. Chapter Writing - Didactic content with research + author context
5. Specialized Review - 10 specialized reviewer personas
6. Critical Reading & Iteration - 3 cycles with 5 virtual readers
7. Editing & Formatting - Final formatting and validation
8. Finalization & Cover - Cover generation and metadata
9. Publication & Export - DOCX, EPUB, PDF, JSON export for KDP

Total: 25 Agents + 30+ Tools + Multi-persona Review System
"""

__version__ = "1.0.0"
__author__ = "Igor Medeiros"
__description__ = "Autonomous editorial automation with AI"

from config import (
    get_model,
    get_research_model,
    get_logger,
    console,
    get_config,
    get_message,
    get_pipeline_config,
    get_models_config,
    get_personas_config,
    get_tools_config,
    get_agents_config,
    get_agent_for_stage,
    print_panel,
    print_table,
    print_progress,
)
from input_validator import validate_book_input

# Agents imports commented out for now (will be uncommented when agents.py is ready)
# from agents import (
#     create_title_agent,
#     create_structure_agent,
#     create_deep_research_agent,
#     create_chapter_agent,
#     create_review_agent,
#     create_editing_agent,
#     create_finalization_agent,
#     create_publication_agent,
#     # Specialized Review Personas (10)
#     create_technical_reviewer_agent,
#     create_editorial_reviewer_agent,
#     create_content_stylist_agent,
#     create_governance_agent,
#     create_ethics_validator_agent,
#     create_author_stories_reviewer_agent,
#     create_author_positioning_reviewer_agent,
#     create_author_vision_opinions_reviewer_agent,
#     create_examples_exercises_code_reviewer_agent,
#     create_research_references_validator_agent,
#     # Virtual Reader Agents (5)
#     create_curious_beginner_reader_agent,
#     create_technical_professional_reader_agent,
#     create_didactic_educator_reader_agent,
#     create_domain_specialist_reader_agent,
#     create_reflective_reader_agent,
#     # Coordinator Agent (1)
#     create_coordinator_superagent,
#     # Execution Functions
#     execute_agent,
#     execute_review_personas,
#     execute_critical_reading_iterations,
# )
# from tools import (
#     # RAG Tools
#     search_knowledge_base,
#     retrieve_rag_context,
#     retrieve_author_stories,
#     retrieve_author_positioning,
#     retrieve_author_vision,
#     # Stage 4A: Deep Research Tools
#     query_context7_mcp,
#     perform_deep_research,
#     vectorize_research,
#     store_in_rag_external,
#     # Content Tools
#     count_words,
#     validate_content_quality,
#     format_markdown,
#     # Generation Tools
#     generate_amazon_optimized_title,
#     generate_outline,
#     generate_cover,
#     generate_kdp_metadata,
#     # Export Tools
#     export_to_docx,
#     export_to_epub,
#     export_to_pdf,
#     # Review Tools
#     review_tone_and_engagement,
#     review_clarity_and_empathy,
#     review_grammar_and_style,
#     review_logical_flow,
#     review_code_examples,
#     # Tool Collection Functions
#     get_ideation_tools,
#     get_title_tools,
#     get_structure_tools,
#     get_deep_research_tools,
#     get_chapter_writing_tools,
#     get_review_tools,
#     get_editing_tools,
#     get_finalization_tools,
#     get_publication_tools,
#     get_all_tools,
# )
# from main import run_ebook_pipeline

__all__ = [
    # Configuration
    "get_model",
    "get_research_model",
    "get_logger",
    "console",
    "get_config",
    "get_message",
    "get_pipeline_config",
    "get_models_config",
    "get_personas_config",
    "get_tools_config",
    "get_agents_config",
    "get_agent_for_stage",
    "print_panel",
    "print_table",
    "print_progress",
    "validate_book_input",
]