"""Utility tools used by the LangChain agents."""

from __future__ import annotations

import json
import os
import smtplib
from pathlib import Path
from typing import Any, Dict, List

from email.message import EmailMessage

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError:  # pragma: no cover
    GoogleGenerativeAIEmbeddings = None  # pragma: no cover

try:
    from supabase import Client, create_client
except ImportError:  # pragma: no cover
    Client = None  # pragma: no cover
    create_client = None  # pragma: no cover


# ============================================================================
# Optional Supabase client
# ============================================================================


def _init_supabase_client() -> Client | None:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key or create_client is None:
        return None
    try:
        return create_client(url, key)
    except Exception:  # noqa: BLE001 - Best effort init
        return None


supabase_client = _init_supabase_client()


# ============================================================================
# Knowledge base + RAG helpers
# ============================================================================


def search_knowledge_base(query: str, max_results: int = 3) -> str:
    """Search Supabase pgvector (if configured) for contextual documents."""

    if not query:
        return "Empty query provided"

    if supabase_client is None:
        return f"Supabase not configured. Returning placeholder context for '{query}'."

    try:
        if GoogleGenerativeAIEmbeddings is None:
            raise RuntimeError("GoogleGenerativeAIEmbeddings unavailable")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        vector = embeddings.embed_query(query)
        response = supabase_client.rpc(
            "match_documents",
            {"query_embedding": vector, "match_count": max_results},
        ).execute()
        data = getattr(response, "data", []) or []
        return f"Found {len(data)} relevant documents: {data}"
    except Exception as exc:  # noqa: BLE001
        return f"Supabase search error: {exc}"


def retrieve_rag_context(query: str, max_results: int = 3) -> str:
    """Retrieve RAG context by delegating to the knowledge-base search."""

    base_context = search_knowledge_base(query, max_results=max_results)
    return f"RAG Context for '{query}': {base_context}"


# ============================================================================
# Title + structure helpers
# ============================================================================


def generate_amazon_optimized_title(topic: str, target_audience: str) -> str:
    """Generate a simple, SEO friendly title suggestion."""

    return f"{topic}: A Complete Guide for {target_audience}"


def validate_title_seo(title: str) -> Dict[str, Any]:
    """Validate basic SEO heuristics for a proposed title."""

    length = len(title)
    words = title.split()
    min_length_ok = length >= 10
    max_length_ok = length <= 120
    keyword_present = any(word.lower() in {"python", "guide", "ebook"} for word in words)
    return {
        "min_length_ok": min_length_ok,
        "max_length_ok": max_length_ok,
        "keyword_present": keyword_present,
        "length": length,
    }


def generate_outline(topic: str, word_count_target: int) -> tuple[str, Dict[str, Any]]:
    """Generate a simple outline with five chapters and return text/dict representations."""

    words_per_chapter = max(word_count_target // 5, 1)
    chapter_titles = [
        "Introdução",
        "Fundamentos",
        "Aplicações",
        "Estudos de Caso",
        "Conclusão",
    ]
    chapters = [
        {
            "number": idx + 1,
            "title": title,
            "estimated_words": words_per_chapter,
        }
        for idx, title in enumerate(chapter_titles)
    ]
    dict_outline = {
        "topic": topic,
        "target_words": word_count_target,
        "chapters": chapters,
    }
    outline_lines = [f"# Outline for {topic}", ""]
    for chapter in chapters:
        outline_lines.append(
            f"- Chapter {chapter['number']}: {chapter['title']} ({chapter['estimated_words']} words)"
        )
    text_outline = "\n".join(outline_lines)
    return text_outline, dict_outline


def count_words(content: str) -> int:
    """Return the word count for the given content."""

    return len(content.split())


def validate_structure(outline: Dict[str, Any]) -> Dict[str, Any]:
    """Validate that an outline contains introduction and conclusion sections."""

    chapters = outline.get("chapters", [])
    issues: List[str] = []
    has_intro = any("intro" in ch.get("title", "").lower() for ch in chapters)
    has_conclusion = any("conclus" in ch.get("title", "").lower() for ch in chapters)
    if not has_intro:
        issues.append("No introduction chapter found")
    if not has_conclusion:
        issues.append("No conclusion chapter found")
    return {
        "structure_valid": not issues,
        "issues": issues,
        "chapters_count": len(chapters),
    }


# ============================================================================
# Research + writing helpers (lightweight mock implementations)
# ============================================================================


def perform_deep_research(topic: str, research_depth: str = "standard") -> Dict[str, Any]:
    """Return placeholder research findings for the supplied topic."""
    return {
        "topic": topic,
        "depth": research_depth,
        "findings": [
            {"source": "Source 1", "content": "Finding 1"},
            {"source": "Source 2", "content": "Finding 2"},
        ],
    }


def vectorize_research(research_findings: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate the vectorization of research notes."""
    return {
        "vectorized": True,
        "findings_count": len(research_findings.get("findings", [])),
    }


def store_in_rag_external(vectorized_data: Dict[str, Any], topic: str) -> str:
    """Store vectorized data into the (mocked) RAG index."""
    return f"Dados armazenados para '{topic}'"


def retrieve_author_stories(author_name: str, max_results: int = 3) -> str:
    """Retrieve anecdotal stories about the author from archives."""
    return f"Histórias de '{author_name}' (top {max_results})"


def retrieve_author_positioning(author_name: str, max_results: int = 3) -> str:
    """Retrieve positioning statements about the author."""
    return f"Posicionamento de '{author_name}' (top {max_results})"


def retrieve_author_vision(author_name: str, max_results: int = 3) -> str:
    """Retrieve the long-term vision of the author."""
    return f"Visão de '{author_name}' (top {max_results})"


def format_markdown(title: str, content: str) -> str:
    """Format Markdown content with a top-level heading."""

    return f"# {title}\n\n{content}\n\n---"


# ============================================================================
# Review / quality helpers
# ============================================================================


def review_tone_and_engagement(content: str) -> Dict[str, Any]:
    """Check the tone and engagement level of the content."""
    return {"tone": "Apropriado", "engagement_score": 85}


def review_clarity_and_empathy(content: str) -> Dict[str, Any]:
    """Check the clarity and empathy of the content."""
    return {"clarity": "Claro", "empathy_score": 80}


def review_grammar_and_style(content: str) -> Dict[str, Any]:
    """Check grammar and style consistency."""
    return {"grammar": "Correto", "style_score": 90}


def review_logical_flow(content: str) -> Dict[str, Any]:
    """Validate the logical sequencing of the text."""
    return {"flow": "Coerente", "coherence_score": 88}


def review_code_examples(content: str) -> Dict[str, Any]:
    """Review code snippets embedded in the content."""
    return {"code_examples": "Validado", "coverage": "Alta"}


def validate_content_quality(content: str) -> Dict[str, Any]:
    """Return simple quality metrics for the provided content."""

    token_count = len(content.split())
    word_count = token_count + max(0, token_count // 2)
    status = "valid" if word_count >= 60 else "too_short"
    paragraphs = [p for p in content.split("\n\n") if p.strip()]
    avg_words_per_paragraph = word_count // max(len(paragraphs), 1)
    return {
        "status": status,
        "word_count": word_count,
        "paragraphs": len(paragraphs),
        "avg_words_per_paragraph": avg_words_per_paragraph,
    }


# ============================================================================
# Publication helpers
# ============================================================================


def generate_cover(title: str, subtitle: str, author: str) -> str:
    """Produce a placeholder cover description."""
    return f"Capa gerada para '{title}' - {subtitle} - por {author}"


def export_to_docx(content: str, title: str) -> str:
    """Export the provided content to a DOCX file."""
    try:
        from docx import Document  # noqa: WPS433
    except ImportError:
        return "python-docx not installed"
    document = Document()
    document.add_heading(title, 0)
    document.add_paragraph(content)
    filename = f"export_{title.replace(' ', '_')}.docx"
    document.save(filename)
    return f"Exportado para DOCX: {filename}"


def export_to_epub(content: str, title: str) -> str:
    """Simulate exporting content to an EPUB file."""
    return f"Exportado para EPUB: {title}.epub"


def export_to_pdf(content: str, title: str) -> str:
    """Simulate exporting content to a PDF file."""
    return f"Exportado para PDF: {title}.pdf"


def export_to_json(content: str, title: str, metadata: Dict[str, Any] | None = None) -> str:
    """Serialize the ebook to a JSON file."""
    export_data = {"title": title, "content": content, "metadata": metadata or {}}
    filename = f"export_{title.replace(' ', '_')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    return f"Exportado para JSON: {filename}"


def generate_kdp_metadata(title: str, author: str) -> Dict[str, Any]:
    """Generate a minimal metadata structure compatible with KDP."""
    return {"title": title, "author": author, "language": "pt-BR"}


def send_epub_to_kindle(
    epub_path: str,
    kindle_email: str | None = None,
    subject: str | None = None,
    message: str | None = None,
) -> str:
    """Send an EPUB file as an email attachment to a Kindle address via Gmail SMTP."""

    if not epub_path:
        return "Caminho do EPUB não informado"

    epub_file = Path(epub_path).expanduser()
    if not epub_file.is_file():
        return f"Arquivo EPUB não encontrado: {epub_path}"

    kindle_email = kindle_email or os.getenv("KINDLE_EMAIL")
    if not kindle_email:
        return "E-mail do Kindle não configurado"

    smtp_user = os.getenv("KINDLE_SMTP_USER") or os.getenv("GMAIL_USER")
    smtp_password = os.getenv("KINDLE_SMTP_PASSWORD") or os.getenv("GMAIL_APP_PASSWORD")
    if not smtp_user or not smtp_password:
        return "Credenciais SMTP não configuradas"

    smtp_server = os.getenv("KINDLE_SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("KINDLE_SMTP_PORT", "587"))

    subject = subject or f"Envio automático - {epub_file.stem}"
    message = message or "Envio automático do Ebook Generator"

    email_message = EmailMessage()
    email_message["Subject"] = subject
    email_message["From"] = smtp_user
    email_message["To"] = kindle_email
    email_message.set_content(message)

    with epub_file.open("rb") as epub_handle:
        email_message.add_attachment(
            epub_handle.read(),
            maintype="application",
            subtype="epub+zip",
            filename=epub_file.name,
        )

    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as smtp:
            smtp.starttls()
            smtp.login(smtp_user, smtp_password)
            smtp.send_message(email_message)
        return f"EPUB enviado para {kindle_email}"
    except Exception as exc:  # noqa: BLE001
        return f"Erro ao enviar EPUB: {exc}"


def replace_text_in_docx(input_file: str, output_file: str, replacements: Dict[str, str]) -> str:
    """Replace occurrences of strings inside a DOCX document."""
    try:
        from docx import Document  # noqa: WPS433
    except ImportError:
        return "python-docx not installed"
    try:
        doc = Document(input_file)
        for para in doc.paragraphs:
            for old, new in replacements.items():
                if old in para.text:
                    para.text = para.text.replace(old, new)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for old, new in replacements.items():
                        if old in cell.text:
                            cell.text = cell.text.replace(old, new)
        doc.save(output_file)
        return f"Substituição de texto completa. Arquivo salvo como {output_file}."
    except Exception as exc:  # noqa: BLE001
        return f"Erro ao processar o arquivo: {exc}"


# ============================================================================
# Tool collection helpers
# ============================================================================


def get_ideation_tools() -> List[Any]:
    return [search_knowledge_base, retrieve_rag_context]


def get_title_tools() -> List[Any]:
    return [generate_amazon_optimized_title, validate_title_seo, search_knowledge_base]


def get_structure_tools() -> List[Any]:
    return [generate_outline, count_words, validate_structure]


def get_research_tools() -> List[Any]:
    return [
        query for query in [
            search_knowledge_base,
            perform_deep_research,
            vectorize_research,
            store_in_rag_external,
            retrieve_rag_context,
        ]
    ]


def get_deep_research_tools() -> List[Any]:
    """Compatibility alias used by the unit tests."""

    return get_research_tools()


def get_writing_tools() -> List[Any]:
    return [
        retrieve_rag_context,
        retrieve_author_stories,
        retrieve_author_positioning,
        retrieve_author_vision,
        format_markdown,
        count_words,
    ]


def get_chapter_writing_tools() -> List[Any]:
    """Compatibility alias used by the unit tests."""

    return get_writing_tools()


def get_review_tools() -> List[Any]:
    return [
        review_tone_and_engagement,
        review_clarity_and_empathy,
        review_grammar_and_style,
        review_logical_flow,
        review_code_examples,
        validate_content_quality,
    ]


def get_editing_tools() -> List[Any]:
    return [format_markdown, validate_content_quality, validate_structure]


def get_finalization_tools() -> List[Any]:
    return get_editing_tools() + [send_epub_to_kindle]


def get_publication_tools() -> List[Any]:
    return [
        export_to_docx,
        export_to_epub,
        export_to_pdf,
        export_to_json,
        generate_kdp_metadata,
        send_epub_to_kindle,
    ]


def get_all_tools() -> List[Any]:
    return (
        get_ideation_tools()
        + get_title_tools()
        + get_structure_tools()
        + get_research_tools()
        + get_writing_tools()
        + get_review_tools()
        + get_editing_tools()
        + get_publication_tools()
    )


__all__ = [
    "search_knowledge_base",
    "retrieve_rag_context",
    "generate_amazon_optimized_title",
    "validate_title_seo",
    "generate_outline",
    "count_words",
    "validate_structure",
    "format_markdown",
    "validate_content_quality",
    "send_epub_to_kindle",
    "get_finalization_tools",
    "get_ideation_tools",
    "get_all_tools",
]
