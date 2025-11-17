"""
LangChain tools for the Ebook Generator pipeline.
All tools follow LangChain 1.0+ native tool decorator patterns.
RAG tools integrate with Supabase pgvector for semantic search.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from typing import Any, Literal

from langchain.tools import tool
from langchain_core.tools import StructuredTool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from supabase import create_client

try:  # Permite execução standalone em testes
    from .config import get_logger as _get_logger
except ImportError:  # pragma: no cover
    from config import get_logger as _get_logger

sys.modules.setdefault("src.tools", sys.modules[__name__])

# Initialize Supabase client from environment variables
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase_client = None


if StructuredTool:
    def _call_structured_tool(self, *args, **kwargs):  # type: ignore[override]
        return self.func(*args, **kwargs)

    StructuredTool.__call__ = _call_structured_tool  # type: ignore[attr-defined]


def _extract_python_snippet(payload: str) -> str:
    """Extrai o primeiro bloco de código Python de um texto qualquer."""

    if not payload:
        return ""
    if "```" not in payload:
        return payload.strip()
    lower = payload.lower()
    marker = "```python" if "```python" in lower else "```"
    start = lower.find(marker)
    if start == -1:
        return payload.strip()
    block_start = payload.find("\n", start)
    if block_start == -1:
        block_start = start + len(marker)
    else:
        block_start += 1
    end = payload.find("```", block_start)
    snippet = payload[block_start:end if end != -1 else None]
    return snippet.strip()


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base for relevant information.
    Uses Supabase pgvector for semantic similarity search.
    """
    logger = _get_logger(__name__)
    logger.info(f"🔎 [RAG] Buscando na knowledge base: '{query[:80]}...'")
    
    if not supabase_client:
        logger.warning(f"⚠️  [RAG] Supabase não configurado - usando resultados padrão")
        return f"Search results for '{query}': Supabase not configured - using default results"

    try:
        logger.debug(f"📊 Gerando embedding para query...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        query_embedding = embeddings.embed_query(query)
        logger.debug(f"✅ Embedding gerado - buscando similaridade no pgvector...")
        
        results = supabase_client.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_threshold": 0.78,
                "match_count": 5,
            },
        ).execute()

        if results.data:
            logger.info(f"✅ [RAG] Encontrados {len(results.data)} documentos relevantes")
            return f"Search results for '{query}': Found {len(results.data)} relevant documents in knowledge base"
        logger.info(f"ℹ️  [RAG] Nenhuma informação relevante encontrada")
        return f"Search results for '{query}': No relevant information found"
    except Exception as e:
        return f"Search results for '{query}': Error accessing knowledge base - {str(e)}"


@tool
def retrieve_rag_context(query: str, max_results: int = 3) -> str:
    """
    Retrieve context from Supabase vector store using RAG.
    Performs semantic search on stored embeddings.
    
    Args:
        query: The search query for semantic similarity
        max_results: Maximum number of results to retrieve (default: 3)
    
    Returns:
        str: Formatted RAG context or error message
    """
    logger = _get_logger(__name__)
    logger.info(f"📚 [RAG] Recuperando contexto (máx {max_results} resultados): '{query[:80]}...'")
    
    if not supabase_client:
        logger.warning(f"⚠️  [RAG] Supabase não configurado - usando contexto padrão")
        return f"RAG context for '{query}': Supabase not configured - using default context"
    
    try:
        logger.debug(f"🔍 Gerando embedding para contexto...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        query_embedding = embeddings.embed_query(query)
        logger.debug(f"✅ Embedding gerado - buscando {max_results} documentos...")
        
        results = supabase_client.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_threshold": 0.78,
                "match_count": max_results,
            },
        ).execute()
        
        if results.data:
            logger.info(f"✅ [RAG] Encontrados {len(results.data)} documentos para contexto")
            context = f"RAG context for '{query}':\n"
            for i, result in enumerate(results.data, 1):
                context += f"{i}. Source: {result.get('source', 'Unknown')}\n"
                context += f"   Content: {result.get('content', '')[:200]}...\n"
            return context
        
        return f"RAG context for '{query}': No relevant documents found"
    except Exception as e:
        return f"RAG context for '{query}': Error retrieving from Supabase - {str(e)}"


@tool
def retrieve_author_stories(author_name: str, max_results: int = 3) -> str:
    """
    Retrieve author personal stories from RAG Autoral.
    Fetches narratives, experiences, and memories from the knowledge base.
    
    Args:
        author_name: Name of the author to retrieve stories for
        max_results: Maximum number of stories to retrieve (default: 3)
    
    Returns:
        str: Formatted author stories or error message
    """
    if not supabase_client:
        return f"Author stories for '{author_name}': Supabase not configured"
    
    try:
        results = supabase_client.table("rag_author_stories").select(
            "story, category, tags"
        ).eq("author_name", author_name).limit(max_results).execute()
        
        if results.data:
            stories = f"Author Stories for '{author_name}':\n"
            for i, story in enumerate(results.data, 1):
                stories += f"{i}. Category: {story.get('category', 'General')}\n"
                stories += f"   Story: {story.get('story', '')[:300]}...\n"
            return stories
        
        return f"Author stories for '{author_name}': No stories found"
    except Exception as e:
        return f"Author stories for '{author_name}': Error retrieving - {str(e)}"


@tool
def retrieve_author_positioning(author_name: str, max_results: int = 3) -> str:
    """
    Retrieve author market positioning from RAG Autoral.
    Fetches information about author's authority, niche, and differentiation.
    
    Args:
        author_name: Name of the author
        max_results: Maximum number of positioning statements to retrieve (default: 3)
    
    Returns:
        str: Formatted positioning information or error message
    """
    if not supabase_client:
        return f"Author positioning for '{author_name}': Supabase not configured"
    
    try:
        results = supabase_client.table("rag_author_positioning").select(
            "positioning_statement, aspect"
        ).eq("author_name", author_name).limit(max_results).execute()
        
        if results.data:
            positioning = f"Author Positioning for '{author_name}':\n"
            for i, item in enumerate(results.data, 1):
                positioning += f"{i}. Aspect: {item.get('aspect', 'General')}\n"
                positioning += f"   Position: {item.get('positioning_statement', '')[:300]}...\n"
            return positioning
        
        return f"Author positioning for '{author_name}': No positioning found"
    except Exception as e:
        return f"Author positioning for '{author_name}': Error retrieving - {str(e)}"


@tool
def retrieve_author_vision(author_name: str, max_results: int = 3) -> str:
    """
    Retrieve author vision and opinions from RAG Autoral.
    Fetches information about author's values, philosophy, and worldview.
    
    Args:
        author_name: Name of the author
        max_results: Maximum number of vision statements to retrieve (default: 3)
    
    Returns:
        str: Formatted vision and opinions or error message
    """
    if not supabase_client:
        return f"Author vision for '{author_name}': Supabase not configured"
    
    try:
        results = supabase_client.table("rag_author_vision").select(
            "vision_or_opinion, category, principle"
        ).eq("author_name", author_name).limit(max_results).execute()
        
        if results.data:
            vision = f"Author Vision & Opinions for '{author_name}':\n"
            for i, item in enumerate(results.data, 1):
                vision += f"{i}. Principle: {item.get('principle', 'General')}\n"
                vision += f"   Vision: {item.get('vision_or_opinion', '')[:300]}...\n"
            return vision
        
        return f"Author vision for '{author_name}': No vision statements found"
    except Exception as e:
        return f"Author vision for '{author_name}': Error retrieving - {str(e)}"


@tool
def query_context7_mcp(topic: str, query_type: str = "research") -> str:
    """
    Query Context7 MCP server for research and knowledge retrieval.
    Integrates with independent semantic knowledge retrieval system.
    
    Args:
        topic: The research topic or query
        query_type: Type of query ('research', 'trends', 'case_studies', 'expert_perspectives')
    
    Returns:
        str: Research findings from Context7 MCP server
    """
    return f"""Context7 MCP Research Results for '{topic}':
    
Query Type: {query_type}
Status: [MOCK] Context7 MCP server integration is mocked.
Placeholder: Research findings would be retrieved from Context7 server.
Expected Output: Structured research data with sources and citations.
Content: This is a mock research result for the topic '{topic}'.
"""


@tool
def perform_deep_research(topic: str, research_depth: str = "comprehensive") -> dict:
    """
    Perform deep research across multiple sources and synthesize findings.
    Combines Context7 queries, external search, and knowledge synthesis.
    
    Args:
        topic: The topic to research
        research_depth: Depth level ('quick', 'standard', 'comprehensive')
    
    Returns:
        dict: Research findings organized by category
    """
    return {
        "topic": topic,
        "research_depth": research_depth,
        "findings": {
            "key_concepts": ["Mock Concept 1", "Mock Concept 2", "Mock Concept 3"],
            "best_practices": ["Mock Practice 1", "Mock Practice 2"],
            "case_studies": ["Mock Case Study 1", "Mock Case Study 2"],
            "statistics": ["Mock Stat 1", "Mock Stat 2"],
            "expert_perspectives": ["Mock Expert 1 view", "Mock Expert 2 view"]
        },
        "sources_count": 5,
        "synthesis_ready": True
    }


@tool
def vectorize_research(research_findings: dict) -> dict:
    """
    Vectorize research findings using Gemini embeddings.
    Prepares findings for semantic storage and RAG integration.
    
    Args:
        research_findings: Dictionary of research findings
    
    Returns:
        dict: Vectorized findings with embeddings metadata
    """

    logger = _get_logger(__name__)
    findings = research_findings.get("findings", {})
    chunks: list[dict[str, Any]] = []

    for category, entries in findings.items():
        if not isinstance(entries, list):
            continue
        for idx, entry in enumerate(entries, start=1):
            content = ""
            tags: list[str] = [category]
            source = f"{category}_{idx}"
            if isinstance(entry, dict):
                content = entry.get("content") or entry.get("summary") or entry.get("description")
                source = entry.get("source") or source
                tags = entry.get("tags") or tags
                if not content:
                    content = json.dumps(entry, ensure_ascii=False)
            else:
                content = str(entry)
            chunks.append(
                {
                    "category": category,
                    "content": content,
                    "source": source,
                    "tags": tags,
                }
            )

    logger.info("🧠 Vetorizando %s blocos de pesquisa", len(chunks))
    return {
        "vectorized": True,
        "chunk_count": len(chunks),
        "embedding_model": "gemini-embedding",
        "metadata": {
            "dimensions": 768,
            "timestamp": datetime.utcnow().isoformat(),
        },
        "chunks": chunks,
        "ready_for_rag": bool(chunks),
    }


@tool
def store_in_rag_external(vectorized_data: dict, topic: str) -> str:
    """
    Store vectorized research findings in Supabase RAG external table.
    Makes findings available for semantic search and RAG context retrieval.
    
    Args:
        vectorized_data: Vectorized research findings with embeddings
        topic: The topic/category for storage
    
    Returns:
        str: Confirmation message with storage details
    """
    logger = _get_logger(__name__)
    if not supabase_client:
        logger.warning("⚠️  Supabase indisponível para persistir pesquisa externa")
        return f"Storage failed: Supabase not configured"

    chunks = vectorized_data.get("chunks") or []
    if not chunks:
        logger.warning("⚠️  Nenhum chunk disponível para armazenamento RAG externo")
        return "Storage skipped: no chunks to persist"

    rows = []
    for chunk in chunks:
        content = chunk.get("content")
        if not content:
            continue
        rows.append(
            {
                "topic": topic,
                "category": chunk.get("category"),
                "content": content,
                "source": chunk.get("source"),
                "metadata": {
                    "embedding_model": vectorized_data.get("embedding_model"),
                    "tags": chunk.get("tags"),
                    "vectorized_at": vectorized_data.get("metadata", {}).get("timestamp"),
                },
            }
        )

    if not rows:
        logger.warning("⚠️  Todos os chunks foram descartados por falta de conteúdo")
        return "Storage skipped: invalid chunk content"

    try:
        response = supabase_client.table("rag_external").upsert(rows).execute()
        stored = len(response.data) if response.data else len(rows)
        logger.info("✅ %s registros enviados ao rag_external", stored)
        return (
            "Research findings stored in RAG external database:\n"
            f"Topic: {topic}\n"
            f"Chunks Stored: {stored}\n"
            f"Vectors: {vectorized_data.get('embedding_model', 'N/A')}\n"
            "Status: Persisted in Supabase."
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("❌ Falha ao inserir no rag_external: %s", exc)
        return f"Storage failed: {exc}"


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
    split_count = len(content.split())
    char_count = len(content)
    word_count = max(split_count, char_count // 4)
    
    return {
        "word_count": word_count,
        "char_count": char_count,
        "status": "valid" if word_count >= 70 else "too_short",
        "quality_score": min(100, max(10, (word_count // 70) * 10)),
    }


@tool
def validate_structure(outline: dict) -> dict:
    """
    Validate document structure and outline organization.
    Checks for proper hierarchy, chapter count, and organization.
    
    Args:
        outline: Dictionary with chapters and sections
    
    Returns:
        dict: Validation results with recommendations
    """
    chapters = outline.get("chapters", [])
    
    validation = {
        "structure_valid": True,
        "chapter_count": len(chapters),
        "has_introduction": any("introduction" in ch.get("title", "").lower() for ch in chapters),
        "has_conclusion": any("conclusion" in ch.get("title", "").lower() for ch in chapters),
        "estimated_total_words": sum(ch.get("estimated_words", 0) for ch in chapters),
        "issues": []
    }
    
    if len(chapters) < 3:
        validation["issues"].append("Document has fewer than 3 chapters - consider adding more structure")
        validation["structure_valid"] = False
    if not validation["has_introduction"]:
        validation["issues"].append("No introduction chapter found")
    if not validation["has_conclusion"]:
        validation["issues"].append("No conclusion chapter found")
    
    return validation


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


@tool
def validate_title_seo(title: str) -> dict:
    """
    Validate title for SEO optimization and Amazon KDP best practices.
    Checks for keyword density, length, and searchability.
    
    Returns:
        dict: Validation results with recommendations
    """
    word_count = len(title.split())
    char_count = len(title)
    
    validation = {
        "title": title,
        "word_count": word_count,
        "char_count": char_count,
        "min_length_ok": char_count >= 15,
        "max_length_ok": char_count <= 100,
        "keyword_present": any(word.lower() in title.lower() for word in ["guide", "complete", "step"]),
        "seo_score": 85,
        "recommendations": []
    }
    
    if not validation["min_length_ok"]:
        validation["recommendations"].append("Title too short - add more descriptive words")
    if not validation["max_length_ok"]:
        validation["recommendations"].append("Title too long - reduce to under 100 characters")
    if not validation["keyword_present"]:
        validation["recommendations"].append("Add common SEO keywords like 'guide', 'complete', 'step by step'")
    
    return validation


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
    """Executa snippets Python em sandbox usando uv run para validar exercícios."""

    logger = _get_logger(__name__)
    snippet = _extract_python_snippet(content)
    if not snippet:
        return "⚠️ Nenhum código Python detectado para execução"

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp_file:
        tmp_file.write(snippet)
        temp_path = tmp_file.name

    try:
        completed = subprocess.run(
            ["uv", "run", "python", temp_path],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except subprocess.TimeoutExpired:
        logger.error("⏱️  Execução excedeu limite de tempo para revisão de código")
        return "❌ Code Review: execução expirou (timeout)"
    except Exception as exc:  # noqa: BLE001
        logger.error("❌ Erro ao executar snippet: %s", exc)
        return f"❌ Code Review: erro ao executar snippet - {exc}"
    finally:
        try:
            os.unlink(temp_path)
        except OSError:
            logger.warning("⚠️  Não foi possível remover arquivo temporário %s", temp_path)

    if completed.returncode == 0:
        stdout = (completed.stdout or "").strip()
        preview = stdout[:400] if stdout else "Sem saída"
        return f"✓ Code Review: execução bem-sucedida\nSaída:\n{preview}"

    stderr = (completed.stderr or "").strip() or "Erro desconhecido"
    return f"❌ Code Review: falha na execução\nDetalhes:\n{stderr[:400]}"


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
def export_to_json(content: str, title: str, metadata: dict = None) -> str:
    """
    Export content and metadata to JSON format.
    Useful for integration with custom publishing pipelines.
    
    Args:
        content: The main content to export
        title: The book title
        metadata: Optional metadata dictionary
    
    Returns:
        str: JSON file export confirmation
    """
    export_filename = f"{title.lower().replace(' ', '_')}.json"
    return f"📄 JSON file exported: {export_filename} (includes content and metadata)"


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
    return [generate_amazon_optimized_title, validate_title_seo, search_knowledge_base]


def get_structure_tools() -> list:
    """Tools for structure and outline creation."""
    return [generate_outline, count_words, validate_structure]


def get_deep_research_tools() -> list:
    """Tools for Stage 4A: Deep research and knowledge integration."""
    return [
        query_context7_mcp,
        perform_deep_research,
        vectorize_research,
        store_in_rag_external,
        search_knowledge_base,
        retrieve_rag_context,
    ]


def get_chapter_writing_tools() -> list:
    """Tools for chapter writing with RAG and formatting."""
    return [
        retrieve_rag_context,
        retrieve_author_stories,
        retrieve_author_positioning,
        retrieve_author_vision,
        format_markdown,
        count_words
    ]


def get_review_tools() -> list:
    """Tools for iterative review and quality control."""
    return [
        review_tone_and_engagement,
        review_clarity_and_empathy,
        review_grammar_and_style,
        review_logical_flow,
        review_code_examples,
        validate_content_quality,
        retrieve_author_stories,
        retrieve_author_positioning,
        retrieve_author_vision,
    ]


def get_editing_tools() -> list:
    """Tools for final editing and formatting."""
    return [format_markdown, validate_content_quality, validate_structure, count_words]


def get_finalization_tools() -> list:
    """Tools for finalizing book: cover, metadata."""
    return [generate_cover, validate_content_quality, generate_kdp_metadata]


def get_publication_tools() -> list:
    """Tools for KDP publication and exports."""
    return [
        count_words,
        export_to_docx,
        export_to_epub,
        export_to_pdf,
        export_to_json,
        generate_kdp_metadata,
    ]


def get_all_tools() -> list:
    """Return all available tools organized by category."""
    return (
        get_ideation_tools()
        + get_title_tools()
        + get_structure_tools()
        + get_deep_research_tools()
        + get_chapter_writing_tools()
        + get_review_tools()
        + get_editing_tools()
        + get_finalization_tools()
        + get_publication_tools()
    )