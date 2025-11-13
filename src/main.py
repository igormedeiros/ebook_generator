"""Main pipeline orchestration for Ebook Generator 1.0.

Executes the full nine-stage editorial pipeline, coordinating research,
writing, review personas, and publication exports with colorful TUI.
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
from .config import (
    get_logger,
    get_model,
    get_research_model,
    print_stage_header,
    print_stage_complete,
    print_pipeline_start,
    print_pipeline_complete,
    print_error_panel,
    get_message,
    get_config,
)

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
    reading_level: str = "intermediate",
    transformation_promise: str = "",
    run_all_stages: bool = True,
    **kwargs,
) -> Dict[str, Any]:
    """
    Execute the 9-stage ebook generation pipeline.
    
    Stages:
    1. Ideation - Central idea, problem, promise
    2. Title - Amazon-optimized titles
    3. Structure - Hierarchical outline
    4A. Deep Research - Context7 + vectorization
    4B. Chapter Writing - Didactic content
    5. Specialized Review - 10 personas
    6. Critical Reading - 5 virtual readers (1 cycle)
    7. Editing - Formatting + validation
    8. Finalization - Cover + metadata
    9. Publication - Export (DOCX/EPUB/PDF/JSON)
    
    Args:
        topic: Main topic
        target_audience: Target audience
        word_count_target: Word count goal (default: 15000)
        reading_level: Reading level (default: intermediate)
        transformation_promise: Promise to reader (optional)
        run_all_stages: Run all 9 stages (default: True)
        **kwargs: Additional parameters stored in overrides
    
    Returns:
        Dict with stage outputs and final status
    """
    results = {
        "pipeline_status": "running",
        "stages": {},
        "metadata": {
            "topic": topic,
            "target_audience": target_audience,
            "word_count_target": word_count_target,
            "reading_level": reading_level,
            "overrides": kwargs,
        }
    }

    try:
        write_model = get_model()
        research_model = get_research_model()

        # Splash screen
        print_pipeline_start(topic, target_audience, word_count_target)

        # Stage 1 — Ideation
        stage_title = get_message("stage_1_title", "Estágio 1: Ideação")
        stage_desc = get_message("stage_1_start", "Gerando ideia central...")
        print_stage_header(1, stage_title, stage_desc)
        
        ideation_agent = create_ideation_agent(write_model)
        promise_context = (
            transformation_promise
            if transformation_promise
            else "Define the transformation promise using audience pain points."
        )
        
        # Get prompt template from config
        agent_prompts = get_config("agent_prompts")
        ideation_prompt = agent_prompts["ideation_prompt_template"].format(
            topic=topic,
            target_audience=target_audience,
            word_count_target=word_count_target,
            reading_level=reading_level,
            promise_context=promise_context,
        )
        ideation_output = execute_agent(ideation_agent, ideation_prompt)
        results["stage_1_ideation"] = {"output": ideation_output}
        print_stage_complete(1)
        logger.info("Stage 1 complete")

        if not run_all_stages:
            results["pipeline_status"] = "partial"
            return results

        # Stage 2 — Title Generation
        stage_title = get_message("stage_2_title", "Estágio 2: Geração de Títulos")
        stage_desc = get_message("stage_2_start", "Pesquisando bestsellers...")
        print_stage_header(2, stage_title, stage_desc)
        
        title_agent = create_title_agent(write_model)
        title_prompt = agent_prompts["title_prompt_template"].format(
            ideation_output=ideation_output
        )
        title_output = execute_agent(title_agent, title_prompt)
        results["stage_2_title"] = {"output": title_output}
        print_stage_complete(2)
        logger.info("Stage 2 complete")

        # Stage 3 — Structure
        stage_title = get_message("stage_3_title", "Estágio 3: Estrutura & Outline")
        stage_desc = get_message("stage_3_start", "Criando índice hierárquico...")
        print_stage_header(3, stage_title, stage_desc)
        
        structure_agent = create_structure_agent(write_model)
        structure_prompt = agent_prompts["structure_prompt_template"].format(
            topic=topic,
            target_audience=target_audience,
            word_count_target=word_count_target,
            ideation_output=ideation_output,
        )
        structure_output = execute_agent(structure_agent, structure_prompt)
        results["stage_3_structure"] = {"output": structure_output}
        print_stage_complete(3)
        logger.info("Stage 3 complete")

        # Stage 4A — Deep Research
        stage_title = get_message("stage_4a_title", "Estágio 4A: Pesquisa Profunda")
        stage_desc = get_message("stage_4a_start", "Consultando Context7 MCP...")
        print_stage_header(4, stage_title, stage_desc)
        
        deep_research_agent = create_deep_research_agent(research_model)
        deep_research_prompt = agent_prompts["deep_research_prompt_template"].format(
            structure_output=structure_output
        )
        deep_research_output = execute_agent(deep_research_agent, deep_research_prompt)
        results["stage_4a_deep_research"] = {"output": deep_research_output}
        print_stage_complete(4)
        logger.info("Stage 4A complete")

        # Stage 4B — Chapter Writing
        stage_title = get_message("stage_4b_title", "Estágio 4B: Escrita de Capítulos")
        stage_desc = get_message("stage_4b_start", "Escrevendo conteúdo didático...")
        print_stage_header(4, "Estágio 4B: Escrita de Capítulos", stage_desc)
        
        chapter_agent = create_chapter_agent(write_model)
        chapter_prompt = agent_prompts["chapter_writing_prompt_template"].format(
            structure_output=structure_output,
            deep_research_output=deep_research_output,
        )
        chapter_output = execute_agent(chapter_agent, chapter_prompt)
        results["stage_4b_chapter_writing"] = {"output": chapter_output}
        print_stage_complete(5)  # Counting 4B as stage 5
        logger.info("Stage 4B complete")

        # Stage 5 — Specialized Review
        stage_title = get_message("stage_5_title", "Estágio 5: Revisão Especializada")
        stage_desc = get_message("stage_5_start", "Executando revisões de 10 personas...")
        print_stage_header(5, stage_title, stage_desc)
        
        review_coordinator = create_review_coordinator_agent(research_model)
        personas = _build_review_persona_agents(write_model, research_model)
        review_prompt = agent_prompts["review_prompt_template"].format(
            chapter_output=chapter_output
        )
        review_output = execute_review_personas(review_coordinator, review_prompt, personas)
        results["stage_5_review"] = {"output": review_output}
        print_stage_complete(6)  # Counting as stage 6
        logger.info("Stage 5 complete")

        # Stage 6 — Critical Reading & Iteration
        stage_title = get_message("stage_6_title", "Estágio 6: Leitura Crítica")
        stage_desc = get_message("stage_6_start", "Simulando 5 leitores virtuais...")
        print_stage_header(6, stage_title, stage_desc)
        
        critical_reading = create_critical_reading_coordinator_agent(research_model)
        virtual_readers = _build_virtual_reader_agents(write_model, research_model)
        critical_prompt = agent_prompts["critical_reading_prompt_template"].format(
            review_output=review_output
        )
        critical_output = execute_review_personas(critical_reading, critical_prompt, virtual_readers)
        results["stage_6_critical_reading"] = {"output": critical_output}
        print_stage_complete(7)  # Counting as stage 7
        logger.info("Stage 6 complete")

        # Stage 7 — Editing
        stage_title = get_message("stage_7_title", "Estágio 7: Edição & Formatação")
        stage_desc = get_message("stage_7_start", "Refinando estilos...")
        print_stage_header(7, stage_title, stage_desc)
        
        editing_agent = create_editing_agent(write_model)
        editing_prompt = agent_prompts["editing_prompt_template"].format(
            critical_output=critical_output
        )
        editing_output = execute_agent(editing_agent, editing_prompt)
        results["stage_7_editing"] = {"output": editing_output}
        print_stage_complete(8)  # Counting as stage 8
        logger.info("Stage 7 complete")

        # Stage 8 — Finalization & Cover
        stage_title = get_message("stage_8_title", "Estágio 8: Finalização & Capa")
        stage_desc = get_message("stage_8_start", "Gerando capa e metadados...")
        print_stage_header(8, stage_title, stage_desc)
        
        finalization_agent = create_finalization_agent(write_model)
        finalization_prompt = agent_prompts["finalization_prompt_template"].format(
            editing_output=editing_output
        )
        finalization_output = execute_agent(finalization_agent, finalization_prompt)
        results["stage_8_finalization"] = {"output": finalization_output}
        print_stage_complete(9)  # Counting as stage 9
        logger.info("Stage 8 complete")

        # Stage 9 — Publication & Export
        stage_title = get_message("stage_9_title", "Estágio 9: Publicação & Exportação")
        stage_desc = get_message("stage_9_start", "Exportando para DOCX, EPUB, PDF, JSON...")
        print_stage_header(9, stage_title, stage_desc)
        
        publication_agent = create_publication_agent(write_model)
        publication_prompt = agent_prompts["publication_prompt_template"].format(
            editing_output_excerpt=editing_output[:2000]
        )
        publication_output = execute_agent(publication_agent, publication_prompt)
        results["stage_9_publication"] = {"output": publication_output}
        print_stage_complete(9)
        logger.info("Stage 9 complete")

        # Final summary
        results["pipeline_status"] = "completed"
        results["summary"] = {
            "topic": topic,
            "target_audience": target_audience,
            "word_count_target": word_count_target,
            "stages_completed": 9,
        }
        
        print_pipeline_complete(results)
        return results

    except Exception as exc:  # pragma: no cover - defensive logging
        logger.error("Pipeline failure", extra={"error": str(exc)})
        print_error_panel(
            error_title="Erro no Pipeline",
            error_message=str(exc),
        )
        results["pipeline_status"] = "error"
        results["error"] = str(exc)
        return results


if __name__ == "__main__":
    run_ebook_pipeline(
        topic="Python para Análise de Dados",
        target_audience="Data Scientists e Analistas",
        word_count_target=20000,
        transformation_promise="Dominar técnicas avançadas de análise em Python",
    )
