"""
Ebook Generator 1.0 - Multi-agent editorial automation platform.
Transforms raw ideas into publication-ready ebooks using LangChain 1.0+ and Gemini 2.5.
"""

__version__ = "1.0.0"
__author__ = "Igor Medeiros"
__description__ = "Autonomous editorial automation with AI"

from config import get_model, get_research_model
from agents import (
    create_ideation_agent,
    create_title_agent,
    create_structure_agent,
    create_chapter_agent,
    create_review_agent,
    create_editing_agent,
    create_finalization_agent,
    create_publication_agent,
    create_coordinator_superagent,
    create_technical_reviewer_agent,
    create_editorial_reviewer_agent,
    create_content_stylist_agent,
    create_governance_agent,
    create_ethics_validator_agent,
    execute_agent,
    execute_review_personas,
)
from tools import (
    search_knowledge_base,
    retrieve_rag_context,
    retrieve_author_stories,
    retrieve_author_positioning,
    retrieve_author_vision,
)
from main import run_ebook_pipeline

__all__ = [
    "get_model",
    "get_research_model",
    "create_ideation_agent",
    "create_title_agent",
    "create_structure_agent",
    "create_chapter_agent",
    "create_review_agent",
    "create_editing_agent",
    "create_finalization_agent",
    "create_publication_agent",
    "create_coordinator_superagent",
    "create_technical_reviewer_agent",
    "create_editorial_reviewer_agent",
    "create_content_stylist_agent",
    "create_governance_agent",
    "create_ethics_validator_agent",
    "execute_agent",
    "execute_review_personas",
    "search_knowledge_base",
    "retrieve_rag_context",
    "retrieve_author_stories",
    "retrieve_author_positioning",
    "retrieve_author_vision",
    "run_ebook_pipeline",
]

