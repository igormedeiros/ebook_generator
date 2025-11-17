"""Main pipeline orchestration for Ebook Generator 1.0.

Executes the full nine-stage editorial pipeline, coordinating research,
writing, review personas, and publication exports with colorful TUI.
"""

import json
import re
import sys
import time
import unicodedata
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn

from langchain_google_genai import ChatGoogleGenerativeAI

try:
    from .agents import (
        create_document_spec_agent,
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
        print_panel,
        print_agent_status,
        print_agent_thought,
        print_agent_output,
        truncate_text,
    )
except ImportError:
    # Allow running as a script (python src/main.py) by injecting project root into sys.path
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from src.agents import (
        create_document_spec_agent,
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
        print_panel,
        print_agent_status,
        print_agent_thought,
        print_agent_output,
        truncate_text,
    )

logger = get_logger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = PROJECT_ROOT / "dist"
TOTAL_STAGES = 11


def _ensure_dist_dir() -> Path:
    """Create and return the dist directory path."""

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    return DIST_DIR


def _serialize_output_for_file(content: Any) -> str:
    """Convert pipeline output into a string for writing to disk."""

    if isinstance(content, str):
        return content
    try:
        return json.dumps(content, ensure_ascii=False, indent=2)
    except Exception:  # noqa: BLE001
        return str(content)


STAGE_FILENAMES = {
    "stage_1_document_spec": "01_document_spec.json",
    "stage_2_ideation": "02_ideation.json",
    "stage_3_title_generation": "03_titles.json",
    "stage_4_structure": "04_structure.md",
    "stage_5_research": "05_research.json",
    "stage_6_writing": "06_chapters.md",
    "stage_7_specialized_review": "07_reviews.json",
    "stage_8_critical_reading": "08_critical_reading.json",
    "stage_9_editing": "09_editing.md",
    "stage_10_finalization": "10_finalization.json",
    "stage_11_publication": "11_publication.json",
}

JSON_FENCE_PATTERN = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)
JSON_WRAPPER_KEYS = {"type", "text", "extras"}


def _slugify_title(value: str) -> str:
    """Gera slug ASCII seguro para formar o nome final do arquivo."""

    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text).strip("-")
    return ascii_text.lower() or "ebook"


def _extract_structured_output(content: Any) -> Any:
    """Extrai dicionário/lista estruturado mesmo quando o LLM usa wrappers."""

    if content is None:
        return None

    if isinstance(content, dict):
        if "text" in content and set(content.keys()).issubset(JSON_WRAPPER_KEYS):
            return _extract_structured_output(content.get("text"))
        return content

    if isinstance(content, list):
        if content and all(isinstance(item, dict) and "text" in item for item in content):
            for item in content:
                nested = _extract_structured_output(item.get("text"))
                if nested is not None:
                    return nested
            return None
        return content

    if isinstance(content, str):
        text = content.strip()
        if not text:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = JSON_FENCE_PATTERN.search(text)
            if match:
                return _extract_structured_output(match.group(1))
        return None

    return None


def _ensure_dict(value: Any) -> Optional[Dict[str, Any]]:
    """Garante retorno de dicionário quando possível."""

    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                return item
    return None


def _ensure_list(value: Any) -> Optional[list]:
    """Converte estruturas conhecidas em lista quando aplicável."""

    if isinstance(value, list):
        return value
    if isinstance(value, dict) and isinstance(value.get("chapters"), list):
        return value.get("chapters")
    return None


def _extract_plain_text(payload: Any) -> str:
    """Normaliza payload arbitrário em texto simples."""

    if payload is None:
        return ""
    if isinstance(payload, str):
        structured = _extract_structured_output(payload)
        if structured is not None and structured is not payload:
            return _extract_plain_text(structured)
        return payload.strip()
    if isinstance(payload, dict):
        if "text" in payload and set(payload.keys()).issubset(JSON_WRAPPER_KEYS):
            return _extract_plain_text(payload.get("text"))
        return json.dumps(payload, ensure_ascii=False, indent=2)
    if isinstance(payload, list):
        pieces = [_extract_plain_text(item) for item in payload]
        combined = "\n\n".join(piece for piece in pieces if piece)
        return combined.strip()
    return str(payload)


def _render_outline_markdown(structure_data: Any) -> str:
    """Transforma a estrutura hierárquica em lista Markdown."""

    chapters = _ensure_list(structure_data)
    if not chapters:
        return ""

    lines: List[str] = []
    for idx, chapter in enumerate(chapters, start=1):
        if not isinstance(chapter, dict):
            continue
        title = chapter.get("title") or f"Capítulo {idx}"
        word_count = chapter.get("word_count")
        header = f"{idx}. **{title}**"
        if word_count:
            header += f" ({word_count} palavras)"
        lines.append(header)
        for section in chapter.get("sections", []) or []:
            if isinstance(section, dict):
                section_title = section.get("title")
                if section_title:
                    lines.append(f"   - {section_title}")
                for subsection in section.get("subsections", []) or []:
                    lines.append(f"      - {subsection}")
            elif isinstance(section, str):
                lines.append(f"   - {section}")
    return "\n".join(lines).strip()


def _render_chapter_markdown(chapter_data: Any) -> str:
    """Gera conteúdo Markdown a partir da estrutura de capítulos."""

    chapters = _ensure_list(chapter_data)
    if not chapters:
        return ""

    lines: List[str] = []
    for idx, chapter in enumerate(chapters, start=1):
        if isinstance(chapter, dict):
            title = chapter.get("title") or f"Capítulo {idx}"
            lines.append(f"## {title}")
            summary = chapter.get("summary") or chapter.get("description")
            if summary:
                lines.append(summary.strip())
            for section in chapter.get("sections", []) or []:
                if isinstance(section, dict):
                    section_title = section.get("title")
                    if section_title:
                        lines.append(f"### {section_title}")
                    section_content = section.get("content") or section.get("summary")
                    if section_content:
                        lines.append(section_content.strip())
                    for subsection in section.get("subsections", []) or []:
                        lines.append(f"- {subsection}")
                elif isinstance(section, str):
                    lines.append(section)
        elif isinstance(chapter, str):
            lines.append(chapter)

    return "\n\n".join(lines).strip()


def _resolve_title_and_subtitle(
    metadata: Dict[str, Any],
    titles_data: Any,
) -> Tuple[str, Optional[str]]:
    """Determina título e subtítulo a partir da ideação e metadados."""

    default_title = metadata.get("topic") or "Ebook sem título"
    default_subtitle = metadata.get("structure_overview")

    titles_dict = _ensure_dict(titles_data)
    if not titles_dict:
        return default_title, default_subtitle

    titles = titles_dict.get("titles")
    chosen = titles[0] if isinstance(titles, list) and titles else default_title
    subtitle = None
    rationales = titles_dict.get("rationales")
    if isinstance(rationales, dict):
        option = rationales.get(chosen)
        if isinstance(option, dict):
            subtitle = option.get("subtitle")
        else:
            first = next((val for val in rationales.values() if isinstance(val, dict)), None)
            if first:
                subtitle = first.get("subtitle")

    return chosen or default_title, subtitle or default_subtitle


def _render_blueprint_section(doc_spec_data: Any, ideation_data: Any) -> str:
    """Cria resumo textual da DEL e da ideação."""

    lines: list[str] = []
    doc_spec = _ensure_dict(doc_spec_data)
    if doc_spec:
        blueprint_id = doc_spec.get("blueprint_id")
        if blueprint_id:
            lines.append(f"- **Blueprint:** {blueprint_id}")
        idea_brief = _ensure_dict(doc_spec.get("idea_brief")) or {}
        concept = idea_brief.get("concept_statement")
        if concept:
            lines.append(f"- **Conceito:** {concept}")
        promise = _ensure_dict(doc_spec.get("promise")) or {}
        transformation = _ensure_dict(promise.get("transformation")) or {}
        if transformation:
            from_state = transformation.get("from")
            to_state = transformation.get("to")
            if from_state and to_state:
                lines.append(f"- **Transformação:** de '{from_state}' para '{to_state}'.")

    ideation_dict = _ensure_dict(ideation_data)
    if ideation_dict:
        idea = ideation_dict.get("idea")
        if idea:
            lines.append(f"- **Ideia Central:** {idea}")
        promise = ideation_dict.get("promise")
        if promise:
            lines.append(f"- **Promessa Refinada:** {promise}")
        audience = ideation_dict.get("audience_insight")
        if audience:
            lines.append(f"- **Insight da Audiência:** {audience}")

    return "\n".join(lines).strip()


def _resolve_final_body(
    editing_data: Any,
    editing_raw: Any,
    chapter_data: Any,
    chapter_raw: Any,
) -> str:
    """Define o corpo principal do ebook combinando edição e capítulos."""

    editing_dict = _ensure_dict(editing_data)
    if editing_dict:
        edited_content = editing_dict.get("edited_content") or editing_dict.get("text")
        if edited_content:
            return edited_content.strip()

    editing_text = _extract_plain_text(editing_raw)
    if editing_text:
        return editing_text

    chapter_markdown = _render_chapter_markdown(chapter_data)
    if chapter_markdown:
        return chapter_markdown

    return _extract_plain_text(chapter_raw)


def _generate_final_ebook(results: Dict[str, Any]) -> Optional[Path]:
    """Consolida os artefatos em dist/ebook_<titulo>.md."""

    try:
        metadata = results.get("metadata", {})
        if not metadata:
            return None

        stage_outputs = {
            key: value.get("output")
            for key, value in results.items()
            if key.startswith("stage_") and isinstance(value, dict)
        }
        if not stage_outputs:
            return None

        doc_spec_data = _extract_structured_output(stage_outputs.get("stage_1_document_spec"))
        ideation_data = _extract_structured_output(stage_outputs.get("stage_2_ideation"))
        titles_data = _extract_structured_output(stage_outputs.get("stage_3_title_generation"))
        structure_data = _extract_structured_output(stage_outputs.get("stage_4_structure"))
        chapter_data = _extract_structured_output(stage_outputs.get("stage_6_writing"))
        editing_data = _extract_structured_output(stage_outputs.get("stage_9_editing"))

        title, subtitle = _resolve_title_and_subtitle(metadata, titles_data)
        outline_md = _render_outline_markdown(structure_data)
        blueprint_md = _render_blueprint_section(doc_spec_data, ideation_data)
        final_body = _resolve_final_body(
            editing_data,
            stage_outputs.get("stage_9_editing"),
            chapter_data,
            stage_outputs.get("stage_6_writing"),
        )

        lines = [f"# {title}"]
        if subtitle:
            lines.append(f"### {subtitle}")

        lines.append("## Especificações Principais")
        lines.append(f"- **Tópico:** {metadata.get('topic', '—')}")
        lines.append(f"- **Público-alvo:** {metadata.get('target_audience', '—')}")
        lines.append(f"- **Meta de palavras:** {metadata.get('word_count_target', '—')}")
        lines.append(f"- **Nível de leitura:** {metadata.get('reading_level', '—')}")
        promise = metadata.get("transformation_promise")
        if promise:
            lines.append(f"- **Promessa de transformação:** {promise}")
        author_name = metadata.get("author_name")
        if author_name:
            lines.append(f"- **Autor:** {author_name}")

        if blueprint_md:
            lines.append("## Blueprint & Promessa")
            lines.append(blueprint_md)

        if outline_md:
            lines.append("## Sumário Estruturado")
            lines.append(outline_md)

        lines.append("## Conteúdo Final")
        lines.append(final_body or "_Conteúdo indisponível nesta execução._")

        markdown = "\n\n".join(line.strip("\n") for line in lines if line is not None).strip() + "\n"
        filename = f"ebook_{_slugify_title(title)}.md"
        return _write_dist_file(filename, markdown)
    except Exception as exc:  # noqa: BLE001
        logger.error(f"⚠️  Falha ao consolidar ebook final: {exc}")
        return None


def _write_dist_file(filename: str, content: Any) -> Path:
    """Persist content under dist/ and log its relative path."""

    dist_dir = _ensure_dist_dir()
    file_path = dist_dir / filename
    file_path.write_text(_serialize_output_for_file(content), encoding="utf-8")
    logger.info(f"💾 Artefato salvo: {file_path.relative_to(PROJECT_ROOT)}")
    return file_path


def _persist_stage_output(stage_key: str, content: Any) -> None:
    """Write a single stage output to the dist folder."""

    filename = STAGE_FILENAMES.get(stage_key, f"{stage_key}.txt")
    _write_dist_file(filename, content)


def _persist_pipeline_summary(results: Dict[str, Any]) -> None:
    """Write a pipeline summary JSON file referencing stage artifacts."""

    summary = {
        "metadata": results.get("metadata", {}),
        "pipeline_status": results.get("pipeline_status"),
        "summary": results.get("summary", {}),
        "stages": {},
    }
    for stage_key, stage_data in results.items():
        if not stage_key.startswith("stage_"):
            continue
        summary["stages"][stage_key] = {
            "artifact": STAGE_FILENAMES.get(stage_key, f"{stage_key}.txt"),
            "has_output": bool(stage_data.get("output")) if isinstance(stage_data, dict) else bool(stage_data),
        }

    _write_dist_file("pipeline_summary.json", summary)


def _estimate_tokens(content: Any) -> int:
    """Rudimentary token estimate based on character count."""

    text = _serialize_output_for_file(content)
    return max(1, len(text) // 4)


def _record_stage_metrics(metrics: Dict[str, Any], stage_key: str, content: Any) -> None:
    """Update metrics dictionary with token estimates per stage."""

    tokens = _estimate_tokens(content)
    metrics.setdefault("stages", {})[stage_key] = {
        "tokens_estimated": tokens,
    }
    metrics["total_tokens"] = metrics.get("total_tokens", 0) + tokens


def _print_metrics_summary(metrics: Dict[str, Any]) -> None:
    """Display a Rich panel with total elapsed time and token estimate."""

    elapsed = metrics.get("elapsed_seconds", 0.0)
    total_tokens = metrics.get("total_tokens", 0)
    content = (
        f"[bold white]Tempo total:[/bold white] {elapsed:.2f} s\n"
        f"[bold white]Tokens estimados:[/bold white] {total_tokens}"
    )
    print_panel("📊 Resumo de Execução", content, style="bright_blue")


def _describe_model(model: Any) -> str:
    """Return human-readable label for current LLM model."""

    return getattr(model, "model", type(model).__name__)


def _show_agent_debug(
    agent_name: str,
    stage_label: str,
    model: Any,
    objective: str,
    prompt_preview: str,
) -> None:
    """Surface status + thought panels for the running agent."""

    print_agent_status(agent_name, stage_label, _describe_model(model), objective)
    if prompt_preview:
        print_agent_thought(
            agent_name,
            f"{objective}\n\n📝 Prompt preview:\n{truncate_text(prompt_preview, 700)}",
        )


def _summarize_feedback(feedback: Dict[str, Any], limit: int = 3) -> str:
    """Create printable summary for persona feedback dictionaries."""

    if not feedback:
        return "(sem feedback registrado)"

    lines = []
    for idx, (persona, text) in enumerate(feedback.items()):
        if idx >= limit:
            break
        lines.append(f"{persona}:\n{truncate_text(str(text), 250)}")
    remaining = len(feedback) - limit
    if remaining > 0:
        lines.append(f"… (+{remaining} análises adicionais)")
    return "\n\n".join(lines)


def show_stage_status(stage_num: int, stage_name: str, action: str):
    """Display current stage action with progress indicator."""
    logger.info(f"[{stage_num}/{TOTAL_STAGES}] 🎯 {stage_name}: {action}")


def _prepare_agent(
    factory: Callable[[ChatGoogleGenerativeAI], Any],
    model: ChatGoogleGenerativeAI,
    mode: str,
) -> Any:
    """Instantiate agent using provided factory."""

    return factory(model)


def _build_review_persona_agents(
    write_model: ChatGoogleGenerativeAI,
    research_model: ChatGoogleGenerativeAI,
) -> Dict[str, Any]:
    """Instantiate the ten specialized review persona agents."""

    return {
        "Technical Reviewer": _prepare_agent(create_technical_reviewer_agent, research_model, "research"),
        "Editorial Reviewer": _prepare_agent(create_editorial_reviewer_agent, write_model, "write"),
        "Content Stylist": _prepare_agent(create_content_stylist_agent, write_model, "write"),
        "Governance QA": _prepare_agent(create_governance_agent, research_model, "research"),
        "Ethics Validator": _prepare_agent(create_ethics_validator_agent, research_model, "research"),
        "Author Stories Reviewer": _prepare_agent(create_author_stories_reviewer_agent, research_model, "research"),
        "Author Positioning Reviewer": _prepare_agent(create_author_positioning_reviewer_agent, research_model, "research"),
        "Author Vision Reviewer": _prepare_agent(create_author_vision_reviewer_agent, research_model, "research"),
        "Code Examples Reviewer": _prepare_agent(create_code_examples_reviewer_agent, research_model, "research"),
        "Research Validator": _prepare_agent(create_research_validator_agent, research_model, "research"),
    }


def _build_virtual_reader_agents(
    write_model: ChatGoogleGenerativeAI,
    research_model: ChatGoogleGenerativeAI,
) -> Dict[str, Any]:
    """Instantiate the five virtual reader personas for critical reading."""

    return {
        "Curious Beginner": _prepare_agent(create_curious_beginner_agent, write_model, "write"),
        "Technical Professional": _prepare_agent(create_technical_professional_agent, research_model, "research"),
        "Didactic Educator": _prepare_agent(create_didactic_educator_agent, write_model, "write"),
        "Domain Specialist": _prepare_agent(create_domain_specialist_agent, research_model, "research"),
        "Reflective Reader": _prepare_agent(create_reflective_reader_agent, write_model, "write"),
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
    metrics: Dict[str, Any] = {
        "start_time": time.time(),
        "total_tokens": 0,
        "stages": {},
    }

    results = {
        "pipeline_status": "running",
        "stages": {},
        "metadata": {
            "topic": topic,
            "target_audience": target_audience,
            "word_count_target": word_count_target,
            "reading_level": reading_level,
            "transformation_promise": transformation_promise,
            "author_name": kwargs.get("author_name", ""),
            "author_bio": kwargs.get("author_bio", ""),
            "extra_notes": kwargs.get("extra_notes", ""),
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
            overall_task = progress.add_task("[bold cyan]📚 Pipeline[/bold cyan]", total=TOTAL_STAGES)
            
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

            # Stage 1 — Documento de Especificação (DEL)
            progress.update(overall_task, description="[bold cyan]1️⃣  Documento de Especificação[/bold cyan]")
            show_stage_status(1, "Documento de Especificação", "Consolidando DEL...")
            stage_title = get_message("stage_1_title", "Estágio 1: Documento de Especificação")
            stage_desc = get_message("stage_1_start", "Consolidando DEL...")
            logger.info(f"\n{'=' * 70}")
            logger.info("ESTÁGIO 1: DOCUMENTO DE ESPECIFICAÇÃO")
            logger.info(f"{'=' * 70}")
            print_stage_header(1, stage_title, stage_desc)

            logger.info("📋 Carregando templates de prompts...")
            agent_prompts = get_config("agent_prompts")
            logger.info("✅ Templates carregados")

            logger.info("🤖 Criando agente DEL...")
            document_spec_agent = _prepare_agent(create_document_spec_agent, research_model, "research")
            logger.info(f"✅ Agente criado: {type(document_spec_agent).__name__}")

            author_name = kwargs.get("author_name", "")
            author_bio = kwargs.get("author_bio", "")
            extra_notes = kwargs.get("extra_notes", "")

            logger.info("🔧 Montando prompt do DEL...")
            document_spec_prompt = agent_prompts["document_spec_prompt_template"].format(
                topic=topic,
                target_audience=target_audience,
                word_count_target=word_count_target,
                reading_level=reading_level,
                author_name=author_name,
                author_bio=author_bio,
                extra_notes=extra_notes,
            )
            logger.info(f"✅ Prompt ({len(document_spec_prompt)} chars)")

            logger.info("🤖 Executando agente DEL (Gemini 2.5 Pro)...")
            _show_agent_debug(
                agent_name="Document Specification Agent",
                stage_label=stage_title,
                model=research_model,
                objective="Gerar blueprint completo do livro",
                prompt_preview=document_spec_prompt,
            )
            document_spec_output = execute_agent(document_spec_agent, document_spec_prompt)
            logger.info("✅ DEL gerado")
            logger.info(f"\n📤 RESULTADO DO DEL:\n{'-' * 70}\n{document_spec_output}\n{'-' * 70}\n")
            print_agent_output(stage_title, document_spec_output)

            results["stage_1_document_spec"] = {"output": document_spec_output}
            _persist_stage_output("stage_1_document_spec", document_spec_output)
            _record_stage_metrics(metrics, "stage_1_document_spec", document_spec_output)
            print_stage_complete(1)
            logger.info("✅ ESTÁGIO 1 CONCLUÍDO\n")
            progress.advance(overall_task)

            if not run_all_stages:
                results["pipeline_status"] = "partial"
                return results

            # Stage 2 — Ideação
            progress.update(overall_task, description="[bold cyan]2️⃣  Ideação[/bold cyan]")
            show_stage_status(2, "Ideação", "Gerando ideia central...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 2: IDEAÇÃO")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_2_title", "Estágio 2: Ideação")
            stage_desc = get_message("stage_2_start", "Desdobrando promessa e definindo problema central...")
            print_stage_header(2, stage_title, stage_desc)

            logger.info("🤖 Criando agente de ideação...")
            ideation_agent = _prepare_agent(create_ideation_agent, write_model, "write")
            logger.info(f"✅ Agente criado: {type(ideation_agent).__name__}")

            promise_context = (
                transformation_promise
                if transformation_promise
                else "Define the transformation promise using audience pain points."
            )

            logger.info("🔧 Montando prompt...")
            ideation_prompt = agent_prompts["ideation_prompt_template"].format(
                topic=topic,
                target_audience=target_audience,
                word_count_target=word_count_target,
                reading_level=reading_level,
                promise_context=promise_context,
            )
            ideation_prompt = (
                f"{ideation_prompt}\n\nDEL Context:\n{document_spec_output}"
            )
            logger.info(f"✅ Prompt ({len(ideation_prompt)} chars)")

            logger.info("🤖 Executando agente de ideação (Gemini 2.5 Flash)...")
            _show_agent_debug(
                agent_name="Ideation Agent",
                stage_label=stage_title,
                model=write_model,
                objective="Gerar ideia central, problema e promessa",
                prompt_preview=ideation_prompt,
            )
            ideation_output = execute_agent(ideation_agent, ideation_prompt)
            logger.info("✅ Ideação concluída")
            logger.info(f"\n📤 RESULTADO DA IDEAÇÃO:\n{'-' * 70}\n{ideation_output}\n{'-' * 70}\n")
            print_agent_output(stage_title, ideation_output)

            results["stage_2_ideation"] = {"output": ideation_output}
            _persist_stage_output("stage_2_ideation", ideation_output)
            _record_stage_metrics(metrics, "stage_2_ideation", ideation_output)
            print_stage_complete(2)
            logger.info("✅ ESTÁGIO 2 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 3 — Título & Subtítulo
            progress.update(overall_task, description="[bold cyan]3️⃣  Títulos[/bold cyan]")
            show_stage_status(3, "Geração de Títulos", "Pesquisando bestsellers...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 3: TÍTULO & SUBTÍTULO")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_3_title", "Estágio 3: Título & Subtítulo")
            stage_desc = get_message("stage_3_start", "Pesquisando bestsellers e propondo títulos otimizados...")
            print_stage_header(3, stage_title, stage_desc)

            logger.info("🤖 Criando agente de títulos...")
            title_agent = _prepare_agent(create_title_agent, write_model, "write")
            logger.info("✅ Agente criado")

            logger.info("🔧 Montando prompt...")
            title_prompt = agent_prompts["title_prompt_template"].format(
                ideation_output=ideation_output
            )
            logger.info(f"✅ Prompt ({len(title_prompt)} chars)")

            logger.info("🤖 Executando agente de títulos (Gemini 2.5 Flash)...")
            _show_agent_debug(
                agent_name="Title Agent",
                stage_label=stage_title,
                model=write_model,
                objective="Gerar 3 títulos otimizados para Amazon",
                prompt_preview=title_prompt,
            )
            title_output = execute_agent(title_agent, title_prompt)
            logger.info("✅ Títulos gerados")
            logger.info(f"\n📤 RESULTADO DOS TÍTULOS:\n{'-' * 70}\n{title_output}\n{'-' * 70}\n")
            print_agent_output(stage_title, title_output)

            results["stage_3_title_generation"] = {"output": title_output}
            _persist_stage_output("stage_3_title_generation", title_output)
            _record_stage_metrics(metrics, "stage_3_title_generation", title_output)
            print_stage_complete(3)
            logger.info("✅ ESTÁGIO 3 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 4 — Estrutura
            progress.update(overall_task, description="[bold cyan]4️⃣  Estrutura[/bold cyan]")
            show_stage_status(4, "Estrutura", "Criando índice hierárquico...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 4: ESTRUTURA")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_4_title", "Estágio 4: Estrutura")
            stage_desc = get_message("stage_4_start", "Criando capítulos, seções e distribuição de palavras...")
            print_stage_header(4, stage_title, stage_desc)

            logger.info("🤖 Criando agente de estrutura...")
            structure_agent = _prepare_agent(create_structure_agent, write_model, "write")
            logger.info("✅ Agente criado")

            logger.info("🔧 Montando prompt...")
            structure_prompt = agent_prompts["structure_prompt_template"].format(
                topic=topic,
                target_audience=target_audience,
                word_count_target=word_count_target,
                ideation_output=ideation_output,
            )
            logger.info(f"✅ Prompt ({len(structure_prompt)} chars)")

            logger.info("🤖 Executando agente de estrutura (Gemini 2.5 Flash)...")
            _show_agent_debug(
                agent_name="Structure Agent",
                stage_label=stage_title,
                model=write_model,
                objective="Criar sumário hierárquico com distribuição de palavras",
                prompt_preview=structure_prompt,
            )
            structure_output = execute_agent(structure_agent, structure_prompt)
            logger.info("✅ Estrutura criada")
            logger.info(f"\n📤 RESULTADO DA ESTRUTURA:\n{'-' * 70}\n{structure_output}\n{'-' * 70}\n")
            print_agent_output(stage_title, structure_output)

            results["stage_4_structure"] = {"output": structure_output}
            _persist_stage_output("stage_4_structure", structure_output)
            _record_stage_metrics(metrics, "stage_4_structure", structure_output)
            print_stage_complete(4)
            logger.info("✅ ESTÁGIO 4 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 5 — Pesquisa Profunda
            progress.update(overall_task, description="[bold cyan]5️⃣  Pesquisa[/bold cyan]")
            show_stage_status(5, "Pesquisa Profunda", "Consultando Context7 MCP...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 5: PESQUISA PROFUNDA")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_5_title", "Estágio 5: Pesquisa Profunda")
            stage_desc = get_message("stage_5_start", "Executando Context7 + Supabase e registrando RAG...")
            print_stage_header(5, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de pesquisa profunda...")
            deep_research_agent = _prepare_agent(create_deep_research_agent, research_model, "research")
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            deep_research_prompt = agent_prompts["deep_research_prompt_template"].format(
                structure_output=structure_output
            )
            logger.info(f"✅ Prompt ({len(deep_research_prompt)} chars)")
            
            logger.info("🤖 Executando agente (Gemini 2.5 Pro - RAG enabled)...")
            logger.info("📚 [RAG] Será utilizado para Context7 MCP e Supabase pgvector")
            _show_agent_debug(
                agent_name="Deep Research Agent",
                stage_label=stage_title,
                model=research_model,
                objective="Orquestrar Context7 + vetorização no Supabase",
                prompt_preview=deep_research_prompt,
            )
            deep_research_output = execute_agent(deep_research_agent, deep_research_prompt)
            logger.info(f"✅ Pesquisa profunda concluída")
            logger.info(f"\n📤 RESULTADO DA PESQUISA PROFUNDA:\n{'-' * 70}\n{deep_research_output}\n{'-' * 70}\n")
            print_agent_output(stage_title, deep_research_output)
            
            results["stage_5_research"] = {"output": deep_research_output}
            _persist_stage_output("stage_5_research", deep_research_output)
            _record_stage_metrics(metrics, "stage_5_research", deep_research_output)
            print_stage_complete(5)
            logger.info("✅ ESTÁGIO 5 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 6 — Escrita
            progress.update(overall_task, description="[bold cyan]6️⃣  Escrita[/bold cyan]")
            show_stage_status(6, "Escrita", "Produzindo capítulos completos...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 6: ESCRITA")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_6_title", "Estágio 6: Escrita")
            stage_desc = get_message("stage_6_start", "Produzindo capítulos inteiros com integração RAG...")
            print_stage_header(6, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de escrita...")
            chapter_agent = _prepare_agent(create_chapter_agent, write_model, "write")
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            chapter_prompt = agent_prompts["chapter_writing_prompt_template"].format(
                structure_output=structure_output,
                deep_research_output=deep_research_output,
            )
            logger.info(f"✅ Prompt ({len(chapter_prompt)} chars)")
            
            logger.info("🤖 Executando agente (Gemini 2.5 Flash)...")
            _show_agent_debug(
                agent_name="Chapter Writing Agent",
                stage_label=stage_title,
                model=write_model,
                objective="Produzir capítulos didáticos com RAG e voz do autor",
                prompt_preview=chapter_prompt,
            )
            chapter_output = execute_agent(chapter_agent, chapter_prompt)
            logger.info(f"✅ Capítulos escritos")
            logger.info(f"\n📤 RESULTADO DOS CAPÍTULOS:\n{'-' * 70}\n{chapter_output}\n{'-' * 70}\n")
            print_agent_output(stage_title, chapter_output)
            
            results["stage_6_writing"] = {"output": chapter_output}
            _persist_stage_output("stage_6_writing", chapter_output)
            _record_stage_metrics(metrics, "stage_6_writing", chapter_output)
            print_stage_complete(6)
            logger.info("✅ ESTÁGIO 6 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 7 — Revisão Especializada
            progress.update(overall_task, description="[bold cyan]7️⃣  Revisão[/bold cyan]")
            show_stage_status(7, "Revisão Especializada", "Executando 10 personas...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 7: REVISÃO ESPECIALIZADA (10 PERSONAS)")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_7_title", "Estágio 7: Revisão Especializada")
            stage_desc = get_message("stage_7_start", "Coordenando personas técnicas/editoriais...")
            print_stage_header(7, stage_title, stage_desc)
            
            logger.info("🤖 Criando coordenador de revisões...")
            review_coordinator = _prepare_agent(create_review_coordinator_agent, research_model, "research")
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
            _show_agent_debug(
                agent_name="Review Coordinator",
                stage_label=stage_title,
                model=research_model,
                objective="Orquestrar 10 personas especializadas",
                prompt_preview=review_prompt,
            )
            review_output = execute_review_personas(review_coordinator, review_prompt, personas)
            logger.info(f"✅ Revisão concluída com 10 personas")
            logger.info(f"📤 Feedback recebido de: {len(review_output)} personas")
            logger.info(f"\n📤 RESULTADO DA REVISÃO:\n{'-' * 70}")
            for persona, feedback_text in review_output.items():
                logger.info(f"\n👤 {persona}:")
                logger.info(f"{feedback_text}")
            logger.info(f"{'-' * 70}\n")
            print_agent_output(stage_title, _summarize_feedback(review_output))
            
            results["stage_7_specialized_review"] = {"output": review_output}
            _persist_stage_output("stage_7_specialized_review", review_output)
            _record_stage_metrics(metrics, "stage_7_specialized_review", review_output)
            print_stage_complete(7)
            logger.info("✅ ESTÁGIO 7 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 8 — Leitura Crítica
            progress.update(overall_task, description="[bold cyan]8️⃣  Leitura Crítica[/bold cyan]")
            show_stage_status(8, "Leitura Crítica", "Simulando 5 leitores virtuais...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 8: LEITURA CRÍTICA (5 PERSONAS, 3 CICLOS)")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_8_title", "Estágio 8: Leitura Crítica")
            stage_desc = get_message("stage_8_start", "Simulando leitores virtuais em ciclos iterativos...")
            print_stage_header(8, stage_title, stage_desc)
            
            logger.info("🤖 Criando coordenador de leitura crítica...")
            critical_reading = _prepare_agent(create_critical_reading_coordinator_agent, research_model, "research")
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
            _show_agent_debug(
                agent_name="Critical Reading Coordinator",
                stage_label=stage_title,
                model=research_model,
                objective="Consolidar 5 leitores virtuais em 3 ciclos",
                prompt_preview=critical_prompt,
            )
            critical_output = execute_review_personas(critical_reading, critical_prompt, virtual_readers)
            logger.info(f"✅ Leitura crítica concluída")
            logger.info(f"📤 Feedback de {len(critical_output)} leitores virtuais")
            logger.info(f"\n📤 RESULTADO DA LEITURA CRÍTICA:\n{'-' * 70}")
            for reader, feedback_text in critical_output.items():
                logger.info(f"\n👁️  {reader}:")
                logger.info(f"{feedback_text}")
            logger.info(f"{'-' * 70}\n")
            print_agent_output(stage_title, _summarize_feedback(critical_output))
            
            results["stage_8_critical_reading"] = {"output": critical_output}
            _persist_stage_output("stage_8_critical_reading", critical_output)
            _record_stage_metrics(metrics, "stage_8_critical_reading", critical_output)
            print_stage_complete(8)
            logger.info("✅ ESTÁGIO 8 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 9 — Edição
            progress.update(overall_task, description="[bold cyan]9️⃣  Edição[/bold cyan]")
            show_stage_status(9, "Edição", "Refinando estilos...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 9: EDIÇÃO & FORMATAÇÃO")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_9_title", "Estágio 9: Edição")
            stage_desc = get_message("stage_9_start", "Aplicando copidesque e validando Markdown...")
            print_stage_header(9, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de edição...")
            editing_agent = _prepare_agent(create_editing_agent, write_model, "write")
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            editing_prompt = agent_prompts["editing_prompt_template"].format(
                critical_output=critical_output
            )
            logger.info(f"✅ Prompt ({len(editing_prompt)} chars)")
            
            logger.info("🤖 Executando agente de edição (Gemini 2.5 Flash)...")
            _show_agent_debug(
                agent_name="Editing Agent",
                stage_label=stage_title,
                model=write_model,
                objective="Refinar estilo, consistência e validação final",
                prompt_preview=editing_prompt,
            )
            editing_output = execute_agent(editing_agent, editing_prompt)
            logger.info(f"✅ Edição concluída")
            logger.info(f"\n📤 RESULTADO DA EDIÇÃO:\n{'-' * 70}\n{editing_output}\n{'-' * 70}\n")
            print_agent_output(stage_title, editing_output)
            
            results["stage_9_editing"] = {"output": editing_output}
            _persist_stage_output("stage_9_editing", editing_output)
            _record_stage_metrics(metrics, "stage_9_editing", editing_output)
            print_stage_complete(9)
            logger.info("✅ ESTÁGIO 9 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 10 — Finalização
            progress.update(overall_task, description="[bold cyan]🔟  Finalização[/bold cyan]")
            show_stage_status(10, "Finalização", "Gerando capa e metadados...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 10: FINALIZAÇÃO & CAPA")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_10_title", "Estágio 10: Finalização")
            stage_desc = get_message("stage_10_start", "Gerando capa conceitual, metadados e sumário navegável...")
            print_stage_header(10, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de finalização...")
            finalization_agent = _prepare_agent(create_finalization_agent, write_model, "write")
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            finalization_prompt = agent_prompts["finalization_prompt_template"].format(
                editing_output=editing_output
            )
            logger.info(f"✅ Prompt ({len(finalization_prompt)} chars)")
            
            logger.info("🤖 Executando agente de finalização (Gemini 2.5 Flash)...")
            _show_agent_debug(
                agent_name="Finalization Agent",
                stage_label=stage_title,
                model=write_model,
                objective="Gerar pitch final, capa conceitual e metadados",
                prompt_preview=finalization_prompt,
            )
            finalization_output = execute_agent(finalization_agent, finalization_prompt)
            logger.info(f"✅ Finalização concluída")
            logger.info(f"\n📤 RESULTADO DA FINALIZAÇÃO:\n{'-' * 70}\n{finalization_output}\n{'-' * 70}\n")
            print_agent_output(stage_title, finalization_output)
            
            results["stage_10_finalization"] = {"output": finalization_output}
            _persist_stage_output("stage_10_finalization", finalization_output)
            _record_stage_metrics(metrics, "stage_10_finalization", finalization_output)
            print_stage_complete(10)
            logger.info("✅ ESTÁGIO 10 CONCLUÍDO\n")
            progress.advance(overall_task)

            # Stage 11 — Publicação e Exportação
            progress.update(overall_task, description="[bold cyan]⓫  Publicação[/bold cyan]")
            show_stage_status(11, "Publicação", "Exportando para DOCX, EPUB, PDF, JSON...")
            logger.info(f"{'=' * 70}")
            logger.info("ESTÁGIO 11: PUBLICAÇÃO & EXPORTAÇÃO")
            logger.info(f"{'=' * 70}")
            stage_title = get_message("stage_11_title", "Estágio 11: KDP & Exportação")
            stage_desc = get_message("stage_11_start", "Exportando formatos finais e montando pacote KDP...")
            print_stage_header(11, stage_title, stage_desc)
            
            logger.info("🤖 Criando agente de publicação...")
            publication_agent = _prepare_agent(create_publication_agent, write_model, "write")
            logger.info(f"✅ Agente criado")
            
            logger.info("🔧 Montando prompt...")
            publication_prompt = agent_prompts["publication_prompt_template"].format(
                final_output_excerpt=editing_output[:2000]
            )
            logger.info(f"✅ Prompt ({len(publication_prompt)} chars)")
            
            logger.info("🤖 Executando agente de publicação (Gemini 2.5 Flash)...")
            logger.info("📦 Formatos suportados: DOCX, EPUB, PDF, JSON")
            logger.info("🔗 Integração: Pandoc para conversão, KDP para publicação")
            _show_agent_debug(
                agent_name="Publication Agent",
                stage_label=stage_title,
                model=write_model,
                objective="Gerar pacotes DOCX/EPUB/PDF/JSON e checklist KDP",
                prompt_preview=publication_prompt,
            )
            publication_output = execute_agent(publication_agent, publication_prompt)
            logger.info(f"✅ Publicação concluída")
            logger.info(f"\n📤 RESULTADO DA PUBLICAÇÃO:\n{'-' * 70}\n{publication_output}\n{'-' * 70}\n")
            print_agent_output(stage_title, publication_output)
            
            results["stage_11_publication"] = {"output": publication_output}
            _persist_stage_output("stage_11_publication", publication_output)
            _record_stage_metrics(metrics, "stage_11_publication", publication_output)
            print_stage_complete(11)
            logger.info("✅ ESTÁGIO 11 CONCLUÍDO\n")
            progress.advance(overall_task)

            final_ebook_path = _generate_final_ebook(results)
            relative_final_path = None
            if final_ebook_path:
                try:
                    relative_final_path = str(final_ebook_path.relative_to(PROJECT_ROOT))
                except ValueError:
                    relative_final_path = str(final_ebook_path)
                results["final_ebook_path"] = relative_final_path
                logger.info(f"📘 Ebook consolidado salvo em: {relative_final_path}")

            # Final summary
            logger.info(f"{'=' * 70}")
            logger.info("🎉 PIPELINE CONCLUÍDO COM SUCESSO!")
            logger.info(f"{'=' * 70}")
            results["pipeline_status"] = "completed"
            elapsed = time.time() - metrics["start_time"]
            metrics["elapsed_seconds"] = elapsed
            results["summary"] = {
                "topic": topic,
                "target_audience": target_audience,
                "word_count_target": word_count_target,
                "stages_completed": TOTAL_STAGES,
                "total_stages": TOTAL_STAGES,
                "token_estimate": metrics.get("total_tokens", 0),
                "elapsed_seconds": elapsed,
                "final_ebook_path": relative_final_path,
            }
            
            _persist_pipeline_summary(results)
            _print_metrics_summary(metrics)
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
    try:
        try:
            from .input_validator import validate_book_input
        except ImportError:
            from src.input_validator import validate_book_input

        book_config = validate_book_input()
        metadata = book_config.get("metadata", {})
        parameters = book_config.get("parameters", {})

        run_ebook_pipeline(
            topic=metadata.get("topic", ""),
            target_audience=metadata.get("target_audience", ""),
            word_count_target=parameters.get("word_count_target", 15000),
            reading_level=parameters.get("reading_level", "intermediate"),
            transformation_promise=parameters.get("transformation_promise", ""),
            author_name=metadata.get("author_name", ""),
            author_bio=metadata.get("author_bio", ""),
            extra_notes=metadata.get("personal_story_usage", ""),
        )
    except Exception as exc:  # noqa: BLE001
        print_error_panel("Erro na Execução", str(exc))
        logger.error(f"Pipeline failed: {exc}")
        sys.exit(1)
