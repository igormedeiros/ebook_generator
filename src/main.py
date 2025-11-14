"""Main pipeline orchestration for Ebook Generator 1.0.

Executes the full nine-stage editorial pipeline, coordinating research,
writing, review personas, and publication exports with colorful TUI.
"""

import sys
from pathlib import Path
from typing import Any, Dict
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn

from langchain_google_genai import ChatGoogleGenerativeAI

try:
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
except ImportError:
    # Allow running as a script (python src/main.py) by injecting project root into sys.path
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.agents import (
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
    from src.config import (
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


def show_stage_status(stage_num: int, stage_name: str, action: str):
    """Display current stage action with progress indicator."""
    logger.info(f"[{stage_num}/9] 🎯 {stage_name}: {action}")


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
        # Initialize overall progress tracker
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=50),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            transient=False,
        ) as progress:
            overall_task = progress.add_task("[bold cyan]📚 Pipeline[/bold cyan]", total=9)
            
            logger.info("=" * 70)
            logger.info("🚀 INICIANDO PIPELINE DE EBOOK GENERATOR 1.0")
            logger.info("=" * 70)
            logger.info(f"📖 Tópico: {topic}")
            logger.info(f"👥 Público-alvo: {target_audience}")
            logger.info(f"📝 Meta de palavras: {word_count_target}")
            logger.info(f"📊 Nível de leitura: {reading_level}")
            logger.info("=" * 70)
            
            show_stage_status(0, "Inicialização", "Carregando modelos com suporte a fallback...")
            
            try:
                from .config import get_model_with_fallback, get_research_model_with_fallback
                write_model = get_model_with_fallback()
                logger.info(f"✅ Modelo de escrita (com fallback): {type(write_model).__name__}")
                
                research_model = get_research_model_with_fallback()
                logger.info(f"✅ Modelo de pesquisa (com fallback): {type(research_model).__name__}")
            except Exception as e:
                logger.warning(f"⚠️  Fallback não disponível, usando padrão: {str(e)}")
                write_model = get_model()
                logger.info(f"✅ Modelo de escrita (padrão): {type(write_model).__name__}")
                
                research_model = get_research_model()
                logger.info(f"✅ Modelo de pesquisa (padrão): {type(research_model).__name__}")

            # Splash screen
            print_pipeline_start(topic, target_audience, word_count_target)

            # Stage 1 — Ideation
            progress.update(overall_task, description="[bold cyan]1️⃣  Ideação[/bold cyan]")
            show_stage_status(1, "Ideação", "Gerando ideia central...")
            stage_title = get_message("stage_1_title", "Estágio 1: Ideação")
            stage_desc = get_message("stage_1_start", "Gerando ideia central...")
            logger.info(f"\n{'=' * 70}")
            logger.info("ESTÁGIO 1: IDEAÇÃO")
            logger.info(f"{'=' * 70}")
            print_stage_header(1, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de ideação...")
            ideation_agent = create_ideation_agent(write_model)
            logger.info(f"✅ Agente criado: {type(ideation_agent).__name__}")
            
            promise_context = (
                transformation_promise
                if transformation_promise
                else "Define the transformation promise using audience pain points."
            )
            
            logger.info("📋 Carregando templates de prompts...")
            agent_prompts = get_config("agent_prompts")
            logger.info(f"✅ Templates carregados")
            
            logger.info("🔧 Montando prompt...")
            ideation_prompt = agent_prompts["ideation_prompt_template"].format(
                topic=topic,
                target_audience=target_audience,
                word_count_target=word_count_target,
                reading_level=reading_level,
                promise_context=promise_context,
            )
            logger.info(f"✅ Prompt ({len(ideation_prompt)} chars)")
            
            logger.info("🤖 Executando agente (Gemini 2.5 Flash)...")
            ideation_output = execute_agent(ideation_agent, ideation_prompt)
            logger.info(f"✅ Ideação concluída")
            logger.info(f"\n📤 RESULTADO DA IDEAÇÃO:\n{'-' * 70}\n{ideation_output}\n{'-' * 70}\n")
            
            results["stage_1_ideation"] = {"output": ideation_output}
            print_stage_complete(1)
            logger.info(f"✅ ESTÁGIO 1 CONCLUÍDO\n")
            progress.advance(overall_task)

            if not run_all_stages:
                results["pipeline_status"] = "partial"
                return results

            # Stage 2 — Title Generation
            progress.update(overall_task, description="[bold cyan]2️⃣  Títulos[/bold cyan]")
            show_stage_status(2, "Geração de Títulos", "Pesquisando bestsellers...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 2: GERAÇÃO DE TÍTULOS")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_2_title", "Estágio 2: Geração de Títulos")
            stage_desc = get_message("stage_2_start", "Pesquisando bestsellers...")
            print_stage_header(2, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de títulos...")
            title_agent = create_title_agent(write_model)
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            title_prompt = agent_prompts["title_prompt_template"].format(
                ideation_output=ideation_output
            )
            logger.info(f"✅ Prompt ({len(title_prompt)} chars)")
            
            logger.info("🤖 Executando agente (Gemini 2.5 Flash)...")
            title_output = execute_agent(title_agent, title_prompt)
            logger.info(f"✅ Títulos gerados")
            logger.info(f"\n📤 RESULTADO DOS TÍTULOS:\n{'-' * 70}\n{title_output}\n{'-' * 70}\n")
            
            results["stage_2_title"] = {"output": title_output}
            print_stage_complete(2)
            logger.info(f"✅ ESTÁGIO 2 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 3 — Structure
            progress.update(overall_task, description="[bold cyan]3️⃣  Estrutura[/bold cyan]")
            show_stage_status(3, "Estrutura", "Criando índice hierárquico...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 3: ESTRUTURA")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_3_title", "Estágio 3: Estrutura & Outline")
            stage_desc = get_message("stage_3_start", "Criando índice hierárquico...")
            print_stage_header(3, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de estrutura...")
            structure_agent = create_structure_agent(write_model)
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            structure_prompt = agent_prompts["structure_prompt_template"].format(
                topic=topic,
                target_audience=target_audience,
                word_count_target=word_count_target,
                ideation_output=ideation_output,
            )
            logger.info(f"✅ Prompt ({len(structure_prompt)} chars)")
            
            logger.info("🤖 Executando agente (Gemini 2.5 Flash)...")
            structure_output = execute_agent(structure_agent, structure_prompt)
            logger.info(f"✅ Estrutura criada")
            logger.info(f"\n📤 RESULTADO DA ESTRUTURA:\n{'-' * 70}\n{structure_output}\n{'-' * 70}\n")
            
            results["stage_3_structure"] = {"output": structure_output}
            print_stage_complete(3)
            logger.info(f"✅ ESTÁGIO 3 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 4A — Deep Research
            progress.update(overall_task, description="[bold cyan]4️⃣A 🔍 Pesquisa[/bold cyan]")
            show_stage_status(4, "Pesquisa Profunda", "Consultando Context7 MCP...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 4A: PESQUISA PROFUNDA")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_4a_title", "Estágio 4A: Pesquisa Profunda")
            stage_desc = get_message("stage_4a_start", "Consultando Context7 MCP...")
            print_stage_header(4, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de pesquisa profunda...")
            deep_research_agent = create_deep_research_agent(research_model)
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            deep_research_prompt = agent_prompts["deep_research_prompt_template"].format(
                structure_output=structure_output
            )
            logger.info(f"✅ Prompt ({len(deep_research_prompt)} chars)")
            
            logger.info("🤖 Executando agente (Gemini 2.5 Pro - RAG enabled)...")
            logger.info("📚 [RAG] Será utilizado para Context7 MCP e Supabase pgvector")
            deep_research_output = execute_agent(deep_research_agent, deep_research_prompt)
            logger.info(f"✅ Pesquisa profunda concluída")
            logger.info(f"\n📤 RESULTADO DA PESQUISA PROFUNDA:\n{'-' * 70}\n{deep_research_output}\n{'-' * 70}\n")
            
            results["stage_4a_deep_research"] = {"output": deep_research_output}
            print_stage_complete(4)
            logger.info(f"✅ ESTÁGIO 4A CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 4B — Chapter Writing
            progress.update(overall_task, description="[bold cyan]4️⃣B ✍️  Escrita[/bold cyan]")
            show_stage_status(4, "Escrita de Capítulos", "Escrevendo conteúdo didático...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 4B: ESCRITA DE CAPÍTULOS")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_4b_title", "Estágio 4B: Escrita de Capítulos")
            stage_desc = get_message("stage_4b_start", "Escrevendo conteúdo didático...")
            print_stage_header(4, "Estágio 4B: Escrita de Capítulos", stage_desc)
            
            logger.info("🤖 Criando agente de escrita...")
            chapter_agent = create_chapter_agent(write_model)
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            chapter_prompt = agent_prompts["chapter_writing_prompt_template"].format(
                structure_output=structure_output,
                deep_research_output=deep_research_output,
            )
            logger.info(f"✅ Prompt ({len(chapter_prompt)} chars)")
            
            logger.info("🤖 Executando agente (Gemini 2.5 Flash)...")
            chapter_output = execute_agent(chapter_agent, chapter_prompt)
            logger.info(f"✅ Capítulos escritos")
            logger.info(f"\n📤 RESULTADO DOS CAPÍTULOS:\n{'-' * 70}\n{chapter_output}\n{'-' * 70}\n")
            
            results["stage_4b_chapter_writing"] = {"output": chapter_output}
            print_stage_complete(5)
            logger.info(f"✅ ESTÁGIO 4B CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 5 — Specialized Review
            progress.update(overall_task, description="[bold cyan]5️⃣  Revisão[/bold cyan]")
            show_stage_status(5, "Revisão Especializada", "Executando 10 personas...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 5: REVISÃO ESPECIALIZADA (10 PERSONAS)")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_5_title", "Estágio 5: Revisão Especializada")
            stage_desc = get_message("stage_5_start", "Executando revisões de 10 personas...")
            print_stage_header(5, stage_title, stage_desc)
            
            logger.info("🤖 Criando coordenador de revisões...")
            review_coordinator = create_review_coordinator_agent(research_model)
            logger.info(f"✅ Coordenador criado")
            
            logger.info("👥 Construindo 10 personas especializadas...")
            personas = _build_review_persona_agents(write_model, research_model)
            logger.info(f"✅ Personas criadas: {', '.join(personas.keys())}")
            
            logger.info("🔧 Montando prompt...")
            review_prompt = agent_prompts["review_prompt_template"].format(
                chapter_output=chapter_output
            )
            logger.info(f"✅ Prompt ({len(review_prompt)} chars)")
            
            logger.info("🤖 Executando revisões em paralelo (10 perspectivas)...")
            review_output = execute_review_personas(review_coordinator, review_prompt, personas)
            logger.info(f"✅ Revisão concluída com 10 personas")
            logger.info(f"📤 Feedback recebido de: {len(review_output)} personas")
            logger.info(f"\n📤 RESULTADO DA REVISÃO:\n{'-' * 70}")
            for persona, feedback_text in review_output.items():
                logger.info(f"\n👤 {persona}:")
                logger.info(f"{feedback_text}")
            logger.info(f"{'-' * 70}\n")
            
            results["stage_5_review"] = {"output": review_output}
            print_stage_complete(6)
            logger.info(f"✅ ESTÁGIO 5 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 6 — Critical Reading & Iteration
            progress.update(overall_task, description="[bold cyan]6️⃣  Leitura Crítica[/bold cyan]")
            show_stage_status(6, "Leitura Crítica", "Simulando 5 leitores virtuais...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 6: LEITURA CRÍTICA (5 PERSONAS, 3 CICLOS)")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_6_title", "Estágio 6: Leitura Crítica")
            stage_desc = get_message("stage_6_start", "Simulando 5 leitores virtuais...")
            print_stage_header(6, stage_title, stage_desc)
            
            logger.info("🤖 Criando coordenador de leitura crítica...")
            critical_reading = create_critical_reading_coordinator_agent(research_model)
            logger.info(f"✅ Coordenador criado")
            
            logger.info("👁️  Construindo 5 leitores virtuais...")
            virtual_readers = _build_virtual_reader_agents(write_model, research_model)
            logger.info(f"✅ Leitores criados: {', '.join(virtual_readers.keys())}")
            
            logger.info("🔧 Montando prompt...")
            critical_prompt = agent_prompts["critical_reading_prompt_template"].format(
                review_output=review_output
            )
            logger.info(f"✅ Prompt ({len(critical_prompt)} chars)")
            
            logger.info("🤖 Executando 3 ciclos de leitura crítica...")
            logger.info("📖 Perspectivas: Curiosidade, Profundidade, Didática, Especialização, Reflexão")
            critical_output = execute_review_personas(critical_reading, critical_prompt, virtual_readers)
            logger.info(f"✅ Leitura crítica concluída")
            logger.info(f"📤 Feedback de {len(critical_output)} leitores virtuais")
            logger.info(f"\n📤 RESULTADO DA LEITURA CRÍTICA:\n{'-' * 70}")
            for reader, feedback_text in critical_output.items():
                logger.info(f"\n👁️  {reader}:")
                logger.info(f"{feedback_text}")
            logger.info(f"{'-' * 70}\n")
            
            results["stage_6_critical_reading"] = {"output": critical_output}
            print_stage_complete(7)
            logger.info(f"✅ ESTÁGIO 6 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 7 — Editing
            progress.update(overall_task, description="[bold cyan]7️⃣  Edição[/bold cyan]")
            show_stage_status(7, "Edição", "Refinando estilos...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 7: EDIÇÃO & FORMATAÇÃO")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_7_title", "Estágio 7: Edição & Formatação")
            stage_desc = get_message("stage_7_start", "Refinando estilos...")
            print_stage_header(7, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de edição...")
            editing_agent = create_editing_agent(write_model)
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            editing_prompt = agent_prompts["editing_prompt_template"].format(
                critical_output=critical_output
            )
            logger.info(f"✅ Prompt ({len(editing_prompt)} chars)")
            
            logger.info("🤖 Executando agente de edição (Gemini 2.5 Flash)...")
            editing_output = execute_agent(editing_agent, editing_prompt)
            logger.info(f"✅ Edição concluída")
            logger.info(f"\n📤 RESULTADO DA EDIÇÃO:\n{'-' * 70}\n{editing_output}\n{'-' * 70}\n")
            
            results["stage_7_editing"] = {"output": editing_output}
            print_stage_complete(8)
            logger.info(f"✅ ESTÁGIO 7 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 8 — Finalization & Cover
            progress.update(overall_task, description="[bold cyan]8️⃣  Finalização[/bold cyan]")
            show_stage_status(8, "Finalização", "Gerando capa e metadados...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 8: FINALIZAÇÃO & CAPA")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_8_title", "Estágio 8: Finalização & Capa")
            stage_desc = get_message("stage_8_start", "Gerando capa e metadados...")
            print_stage_header(8, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de finalização...")
            finalization_agent = create_finalization_agent(write_model)
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            finalization_prompt = agent_prompts["finalization_prompt_template"].format(
                editing_output=editing_output
            )
            logger.info(f"✅ Prompt ({len(finalization_prompt)} chars)")
            
            logger.info("🤖 Executando agente de finalização (Gemini 2.5 Flash)...")
            finalization_output = execute_agent(finalization_agent, finalization_prompt)
            logger.info(f"✅ Finalização concluída")
            logger.info(f"\n📤 RESULTADO DA FINALIZAÇÃO:\n{'-' * 70}\n{finalization_output}\n{'-' * 70}\n")
            
            results["stage_8_finalization"] = {"output": finalization_output}
            print_stage_complete(9)
            logger.info(f"✅ ESTÁGIO 8 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 9 — Publication & Export
            progress.update(overall_task, description="[bold cyan]9️⃣  Publicação[/bold cyan]")
            show_stage_status(9, "Publicação", "Exportando para DOCX, EPUB, PDF, JSON...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 9: PUBLICAÇÃO & EXPORTAÇÃO")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_9_title", "Estágio 9: Publicação & Exportação")
            stage_desc = get_message("stage_9_start", "Exportando para DOCX, EPUB, PDF, JSON...")
            print_stage_header(9, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de publicação...")
            publication_agent = create_publication_agent(write_model)
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            publication_prompt = agent_prompts["publication_prompt_template"].format(
                editing_output_excerpt=editing_output[:2000]
            )
            logger.info(f"✅ Prompt ({len(publication_prompt)} chars)")
            
            logger.info("🤖 Executando agente de publicação (Gemini 2.5 Flash)...")
            logger.info("📦 Formatos suportados: DOCX, EPUB, PDF, JSON")
            logger.info("🔗 Integração: Pandoc para conversão, KDP para publicação")
            publication_output = execute_agent(publication_agent, publication_prompt)
            logger.info(f"✅ Publicação concluída")
            logger.info(f"\n📤 RESULTADO DA PUBLICAÇÃO:\n{'-' * 70}\n{publication_output}\n{'-' * 70}\n")
            
            results["stage_9_publication"] = {"output": publication_output}
            print_stage_complete(9)
            logger.info(f"✅ ESTÁGIO 9 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Final summary
            logger.info(f"{'=' * 70}")
            logger.info("🎉 PIPELINE CONCLUÍDO COM SUCESSO!")
            logger.info(f"{'=' * 70}")
            results["pipeline_status"] = "completed"
            results["summary"] = {
                "topic": topic,
                "target_audience": target_audience,
                "word_count_target": word_count_target,
                "stages_completed": 9,
            }
            
            print_pipeline_complete(results)
            return results

    except Exception as exc:
        logger.error(f"❌ Pipeline failure: {str(exc)}")
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
