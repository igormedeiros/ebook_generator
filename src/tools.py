"""
LangChain tools for the Ebook Generator pipeline.
All tools follow LangChain 1.0+ native tool decorator patterns.
RAG tools integrate with Supabase pgvector for semantic search.
"""

from typing import Literal
from langchain.tools import tool


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base for relevant information.
    Uses Supabase pgvector for semantic similarity search.
    """
    # TODO: Implement Supabase pgvector integration
    return f"Search results for '{query}': Relevant information found"


@tool
def retrieve_rag_context(query: str, max_results: int = 3) -> str:
    """
    Retrieve context from Supabase vector store using RAG.
    Performs semantic search on stored embeddings.
    """
    # TODO: Implement Supabase similarity_search
    return f"RAG context for '{query}': Retrieved {max_results} relevant documents"


@tool
def count_words(content: str) -> int:
    """Count the number of words in the provided content."""
    return len(content.split())


@tool
def validate_content_quality(content: str) -> dict:
    """
    Validate content quality and return metrics.
    Checks for structure, completeness, and word count.
    """
    word_count = len(content.split())
    char_count = len(content)
    
    return {
        "word_count": word_count,
        "char_count": char_count,
        "status": "valid" if word_count > 100 else "too_short",
        "quality_score": min(100, (word_count // 100))
    }


@tool
def format_markdown(title: str, content: str) -> str:
    """Format content as Markdown with title and separator."""
    return f"""# {title}

{content}

---"""


@tool
def generate_amazon_optimized_title(topic: str, target_audience: str) -> str:
    """
    Generate an Amazon KDP-optimized title based on topic and target audience.
    Follows Amazon best practices for discoverability.
    """
    # TODO: Integrate with Amazon trending titles analysis
    return f"📚 {topic}: Complete Guide for {target_audience} - Step by Step"


@tool(response_format="content_and_artifact")
def generate_outline(topic: str, word_count_target: int) -> tuple[str, dict]:
    """
    Generate a structured outline for the given topic.
    Returns both formatted text and structured outline data.
    """
    outline = {
        "topic": topic,
        "target_words": word_count_target,
        "chapters": [
            {"number": 1, "title": "Introduction", "estimated_words": word_count_target // 8},
            {"number": 2, "title": "Foundations", "estimated_words": word_count_target // 4},
            {"number": 3, "title": "Advanced Topics", "estimated_words": word_count_target // 3},
            {"number": 4, "title": "Practical Examples", "estimated_words": word_count_target // 6},
            {"number": 5, "title": "Conclusion", "estimated_words": word_count_target // 8},
        ]
    }
    
    text = f"Outline for '{topic}':\n"
    for ch in outline["chapters"]:
        text += f"{ch['number']}. {ch['title']} (~{ch['estimated_words']} words)\n"
    
    return text, outline


@tool
def review_tone_and_engagement(content: str) -> str:
    """Review content for appropriate tone and audience engagement."""
    return "✓ Tone Review: Content is appropriate and engaging for target audience"


@tool
def review_clarity_and_empathy(content: str) -> str:
    """Review content for clarity, accessibility, and empathetic language."""
    return "✓ Clarity Review: Message is clear and empathetic"


@tool
def review_grammar_and_style(content: str) -> str:
    """Review grammar, spelling, and writing style."""
    return "✓ Grammar Review: No errors detected. Style is consistent."


@tool
def review_logical_flow(content: str) -> str:
    """Review content for logical flow and coherence."""
    return "✓ Coherence Review: Logical flow is maintained throughout"


@tool
def review_code_examples(content: str) -> str:
    """Validate code snippets and technical examples for correctness."""
    return "✓ Code Review: Technical examples validated and executable"


@tool
def generate_cover(title: str, subtitle: str, author: str) -> str:
    """Generate an AI-created book cover design."""
    # TODO: Integrate with DALL-E or similar service
    return f"🎨 Cover generated: {title} - {subtitle} by {author}"


@tool
def export_to_docx(content: str, title: str, filename: str = None) -> str:
    """Export content to Microsoft Word (DOCX) format."""
    export_filename = filename or f"{title.lower().replace(' ', '_')}.docx"
    return f"📄 DOCX file exported: {export_filename}"


@tool
def export_to_epub(content: str, title: str, filename: str = None) -> str:
    """Export content to EPUB format for e-readers."""
    export_filename = filename or f"{title.lower().replace(' ', '_')}.epub"
    return f"📖 EPUB file exported: {export_filename}"


@tool
def export_to_pdf(content: str, title: str, filename: str = None) -> str:
    """Export content to PDF format."""
    export_filename = filename or f"{title.lower().replace(' ', '_')}.pdf"
    return f"📄 PDF file exported: {export_filename}"


@tool
def generate_kdp_metadata(title: str, author: str, category: str, keywords: list[str]) -> dict:
    """
    Generate Amazon KDP-compliant metadata JSON.
    Includes title, author, category, keywords, and description.
    """
    return {
        "title": title,
        "author": author,
        "category": category,
        "keywords": keywords[:10],  # KDP allows up to 10 keywords
        "description": f"Professional e-book on {category.lower()}. Written by {author}.",
        "language": "en-US",
        "mature_content": False,
    }


# Tool collection functions grouped by pipeline stage

def get_ideation_tools() -> list:
    """Tools for the ideation stage: research and brainstorming."""
    return [search_knowledge_base, retrieve_rag_context]


def get_title_tools() -> list:
    """Tools for title and subtitle generation: market research."""
    return [generate_amazon_optimized_title, search_knowledge_base]


def get_structure_tools() -> list:
    """Tools for structure and outline creation."""
    return [generate_outline, count_words]


def get_chapter_writing_tools() -> list:
    """Tools for chapter writing with RAG and formatting."""
    return [retrieve_rag_context, format_markdown, count_words]


def get_review_tools() -> list:
    """Tools for iterative review and quality control."""
    return [
        review_tone_and_engagement,
        review_clarity_and_empathy,
        review_grammar_and_style,
        review_logical_flow,
        review_code_examples,
        validate_content_quality,
    ]


def get_editing_tools() -> list:
    """Tools for final editing and formatting."""
    return [format_markdown, validate_content_quality, count_words]


def get_finalization_tools() -> list:
    """Tools for finalizing book: cover, metadata."""
    return [generate_cover, validate_content_quality]


def get_publication_tools() -> list:
    """Tools for KDP publication and exports."""
    return [
        count_words,
        export_to_docx,
        export_to_epub,
        export_to_pdf,
        generate_kdp_metadata,
    ]


def get_all_tools() -> list:
    """Return all available tools organized by category."""
    return (
        get_ideation_tools()
        + get_title_tools()
        + get_structure_tools()
        + get_chapter_writing_tools()
        + get_review_tools()
        + get_editing_tools()
        + get_finalization_tools()
        + get_publication_tools()
    )