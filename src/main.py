"""Main pipeline orchestration for Ebook Generator 1.0.

Executes the full nine-stage editorial pipeline, coordinating research,
writing, review personas, and publication exports.
"""

import sys
from typing import Any, Dict

from langchain_google_genai import ChatGoogleGenerativeAI

from .agents import (
    create_author_positioning_reviewer_agent,
    create_author_stories_reviewer_agent,
    create_author_vision_reviewer_agent,
    create_chapter_agent,
    create_code_examples_reviewer_agent,
    create_content_stylist_agent,
    create_critical_reading_coordinator_agent,
    create_curious_beginner_agent,
    create_deep_research_agent,
    create_didactic_educator_agent,
    create_domain_specialist_agent,
    create_editing_agent,
    create_editorial_reviewer_agent,
    create_ethics_validator_agent,
    create_finalization_agent,
    create_governance_agent,
    create_ideation_agent,
    create_publication_agent,
    create_reflective_reader_agent,
    create_review_coordinator_agent,
    create_research_validator_agent,
    create_structure_agent,
    create_technical_professional_agent,
    create_technical_reviewer_agent,
    create_title_agent,
    execute_agent,
    execute_review_personas,
)
from .config import get_logger, get_model, get_research_model, print_panel

logger = get_logger(__name__)


def _build_review_persona_agents(
    write_model: ChatGoogleGenerativeAI,
    research_model: ChatGoogleGenerativeAI,
) -> Dict[str, Any]:
    """Instantiate the ten specialized review persona agents."""

    return {
        "Technical Reviewer": create_technical_reviewer_agent(research_model),
        "Editorial Reviewer": create_editorial_reviewer_agent(write_model),
        "Content Stylist": create_content_stylist_agent(write_model),
        "Governance QA": create_governance_agent(research_model),
        "Ethics Validator": create_ethics_validator_agent(research_model),
        "Author Stories Reviewer": create_author_stories_reviewer_agent(research_model),
        "Author Positioning Reviewer": create_author_positioning_reviewer_agent(research_model),
        "Author Vision Reviewer": create_author_vision_reviewer_agent(research_model),
        "Code Examples Reviewer": create_code_examples_reviewer_agent(research_model),
        "Research Validator": create_research_validator_agent(research_model),
    }


def _build_virtual_reader_agents(
    write_model: ChatGoogleGenerativeAI,
    research_model: ChatGoogleGenerativeAI,
) -> Dict[str, Any]:
    """Instantiate the five virtual reader personas for critical reading."""

    return {
        "Curious Beginner": create_curious_beginner_agent(write_model),
        "Technical Professional": create_technical_professional_agent(research_model),
        "Didactic Educator": create_didactic_educator_agent(write_model),
        "Domain Specialist": create_domain_specialist_agent(research_model),
        "Reflective Reader": create_reflective_reader_agent(write_model),
    }


def run_ebook_pipeline(
    topic: str,
    target_audience: str,
    word_count_target: int = 15000,
    transformation_promise: str = "",
    reading_level: str = "intermediary",
    run_all_stages: bool = True,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Execute the full pipeline and return structured stage results."""

    logger.info("Starting Ebook Generator pipeline", extra={"topic": topic})
    results: Dict[str, Any] = {
        "input": {
            "topic": topic,
            "target_audience": target_audience,
            "word_count_target": word_count_target,
            "transformation_promise": transformation_promise,
            "reading_level": reading_level,
            "overrides": kwargs,
        }
    }

    try:
        write_model = get_model()
        research_model = get_research_model()

        # Stage 1 — Ideation
        print_panel(
            title="Stage 1: Ideation",
            content="Generating central idea, problem framing, and promise...",
            style="cyan",
        )
        ideation_agent = create_ideation_agent(write_model)
        promise_context = (
            transformation_promise
            if transformation_promise
            else "Define the transformation promise using audience pain points."
        )
        ideation_prompt = (
            "Return JSON with keys idea, problem, promise, and audience_insight. Context:\n"
            f"Topic: {topic}\nAudience: {target_audience}\n"
            f"Word Count Target: {word_count_target}\nReading Level: {reading_level}\n"
            f"Transformation Promise: {promise_context}"
        )
        ideation_output = execute_agent(ideation_agent, ideation_prompt)
        results["stage_1_ideation"] = {"output": ideation_output}
        logger.info("Stage 1 complete")

        if not run_all_stages:
            results["pipeline_status"] = "partial"
            return results

        # Stage 2 — Title Generation
        print_panel(
            title="Stage 2: Title Generation",
            content="Creating Amazon-optimized title options...",
            style="cyan",
        )
        title_agent = create_title_agent(write_model)
        title_prompt = (
            "Produce exactly three Amazon KDP-ready title options in JSON with fields "
            "titles (list) and rationales (dict by title). Use these insights:\n"
            f"{ideation_output}"
        )
        title_output = execute_agent(title_agent, title_prompt)
        results["stage_2_title"] = {"output": title_output}
        logger.info("Stage 2 complete")

        # Stage 3 — Structure
        print_panel(
            title="Stage 3: Structure",
            content="Designing hierarchical outline aligned with word count target...",
            style="cyan",
        )
        structure_agent = create_structure_agent(write_model)
        structure_prompt = (
            "Create a Markdown table of contents with chapters, sections, and estimated word counts. Consider:\n"
            f"Topic: {topic}\nAudience: {target_audience}\n"
            f"Target Words: {word_count_target}\nIdeation Summary: {ideation_output}"
        )
        structure_output = execute_agent(structure_agent, structure_prompt)
        results["stage_3_structure"] = {"output": structure_output}
        logger.info("Stage 3 complete")

        # Stage 4A — Deep Research
        print_panel(
            title="Stage 4A: Deep Research",
            content="Querying Context7 MCP, vectorizing research, and storing in RAG...",
            style="cyan",
        )
        deep_research_agent = create_deep_research_agent(research_model)
        deep_research_prompt = (
            "Execute deep research for each outline section and return JSON with research_summary, sources, "
            "vector_ids, and storage_status. Outline reference:\n"
            f"{structure_output}"
        )
        deep_research_output = execute_agent(deep_research_agent, deep_research_prompt)
        results["stage_4a_deep_research"] = {"output": deep_research_output}
        logger.info("Stage 4A complete")

        # Stage 4B — Chapter Writing
        print_panel(
            title="Stage 4B: Chapter Writing",
            content="Writing didactic chapters integrating research and author context...",
            style="cyan",
        )
        chapter_agent = create_chapter_agent(write_model)
        chapter_prompt = (
            "Write the first two chapters in Markdown integrating research findings, author stories, positioning, "
            "and vision. Include examples and exercises. Context:\n"
            f"Outline: {structure_output}\nResearch: {deep_research_output}"
        )
        chapter_output = execute_agent(chapter_agent, chapter_prompt)
        results["stage_4b_chapter_writing"] = {"output": chapter_output}
        logger.info("Stage 4B complete")

        # Stage 5 — Specialized Review
        print_panel(
            title="Stage 5: Specialized Review",
            content="Collecting feedback from 10 review personas...",
            style="cyan",
        )
        review_coordinator = create_review_coordinator_agent(research_model)
        review_prompt = (
            "Coordinate all review personas and return JSON with persona_reviews, aggregate_score, critical_issues, "
            "and recommendations. Content to review:\n"
            f"{chapter_output}"
        )
        review_summary = execute_agent(review_coordinator, review_prompt)
        review_personas = _build_review_persona_agents(write_model, research_model)
        persona_feedback = execute_review_personas(review_personas, chapter_output)
        results["stage_5_review"] = {
            "coordinator_output": review_summary,
            "persona_feedback": persona_feedback,
        }
        logger.info("Stage 5 complete")

        # Stage 6 — Critical Reading (single cycle MVP)
        print_panel(
            title="Stage 6: Critical Reading",
            content="Running one iteration with five virtual readers...",
            style="cyan",
        )
        critical_agent = create_critical_reading_coordinator_agent(research_model)
        critical_prompt = (
            "Simulate one iteration cycle with all virtual readers and return JSON with cycle_reports and "
            "improvement_summary. Source content:\n"
            f"{chapter_output}"
        )
        critical_summary = execute_agent(critical_agent, critical_prompt)
        virtual_readers = _build_virtual_reader_agents(write_model, research_model)
        cycle_feedback = execute_review_personas(virtual_readers, chapter_output)
        results["stage_6_critical_reading"] = {
            "coordinator_output": critical_summary,
            "cycles": [
                {
                    "cycle": 1,
                    "feedback": cycle_feedback,
                }
            ],
        }
        logger.info("Stage 6 complete")

        # Stage 7 — Editing
        print_panel(
            title="Stage 7: Editing",
            content="Applying final editing and Markdown validation...",
            style="cyan",
        )
        editing_agent = create_editing_agent(write_model)
        editing_prompt = (
            "Edit the content for grammar, style, formatting, and structure. Return publication-ready Markdown plus any "
            "issues identified. Content:\n"
            f"{chapter_output}"
        )
        editing_output = execute_agent(editing_agent, editing_prompt)
        results["stage_7_editing"] = {"output": editing_output}
        logger.info("Stage 7 complete")

        # Stage 8 — Finalization
        print_panel(
            title="Stage 8: Finalization",
            content="Generating cover concept and metadata package...",
            style="cyan",
        )
        finalization_agent = create_finalization_agent(write_model)
        finalization_prompt = (
            "Produce JSON with cover_briefing, metadata, author_bio, and back_cover_copy using the selected titles and "
            "edited manuscript. Reference data:\n"
            f"Titles: {title_output}\nEdited Content: {editing_output[:2000]}"
        )
        finalization_output = execute_agent(finalization_agent, finalization_prompt)
        results["stage_8_finalization"] = {"output": finalization_output}
        logger.info("Stage 8 complete")

        # Stage 9 — Publication
        print_panel(
            title="Stage 9: Publication",
            content="Preparing multi-format exports and KDP compliance checks...",
            style="cyan",
        )
        publication_agent = create_publication_agent(write_model)
        publication_prompt = (
            "Export the ebook to DOCX, EPUB, PDF, and JSON. Return JSON with exports, validation_report, and "
            "kdp_package_status, highlighting compliance checkpoints. Content excerpt:\n"
            f"{editing_output[:2000]}"
        )
        publication_output = execute_agent(publication_agent, publication_prompt)
        results["stage_9_publication"] = {"output": publication_output}
        logger.info("Stage 9 complete")

        print_panel(
            title="Pipeline Complete ✓",
            content=(
                f"Topic: {topic}\n"
                f"Audience: {target_audience}\n"
                f"Word Count Target: {word_count_target}\n"
                "Stages Completed: 9"
            ),
            style="green",
        )
        results["pipeline_status"] = "completed"
        results["summary"] = {
            "topic": topic,
            "target_audience": target_audience,
            "word_count_target": word_count_target,
            "stages_completed": 9,
        }
        return results

    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Pipeline failure", extra={"error": str(exc)})
        print_panel(
            title="Pipeline Error ❌",
            content=f"An error prevented the pipeline from completing: {exc}",
            style="red",
        )
        results["pipeline_status"] = "error"
        results["error"] = str(exc)
        return results


if __name__ == "__main__":
    run_ebook_pipeline(
        topic="Python for Data Analysis",
        target_audience="Data Scientists and Analysts",
        word_count_target=20000,
        transformation_promise="Master advanced data analysis techniques in Python",
    )
