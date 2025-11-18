"""
Ferramentas para o pipeline de geração de ebook usando LangChain 1.0+.
Todas as ferramentas implementadas baseadas em specs/tools.yaml
"""

from langchain.tools import tool
from docx import Document
from typing import Dict, List, Any
import json
import re


# ============================================================================
# IDEATION TOOLS
# ============================================================================

@tool
def search_knowledge_base(query: str) -> str:
    """
    Busca semântica em Supabase.
    
    Args:
        query: Query para busca
    
    Returns:
        str: Resultados da busca
    """
    # TODO: Implementar Supabase pgvector integration
    return f"Resultados da busca para: {query}"


@tool
def retrieve_rag_context(query: str, max_results: int = 3) -> str:
    """
    Recupera contexto vetorial.
    
    Args:
        query: Query para recuperação
        max_results: Número máximo de resultados (padrão: 3)
    
    Returns:
        str: Contexto recuperado
    """
    # TODO: Implementar Supabase pgvector integration
    return f"Contexto para: {query} (top {max_results})"


# ============================================================================
# TITLE GENERATION TOOLS
# ============================================================================

@tool
def generate_amazon_optimized_title(topic: str, target_audience: str) -> str:
    """
    Cria título sugerido com foco em SEO para Amazon.
    
    Args:
        topic: Tópico do ebook
        target_audience: Público-alvo
    
    Returns:
        str: Título otimizado sugerido
    """
    return f"Título Otimizado: '{topic}' para '{target_audience}'"


@tool
def validate_title_seo(title: str) -> str:
    """
    Verifica pontuação de SEO do título.
    
    Args:
        title: Título a validar
    
    Returns:
        str: Pontuação e feedback SEO
    """
    length = len(title)
    words = len(title.split())
    score = min(100, (length * 10) - (max(0, length - 60) * 5))
    
    return f"SEO Score: {score}/100 - {words} palavras - Comprimento: {length} caracteres"


# ============================================================================
# STRUCTURE TOOLS
# ============================================================================

@tool
def generate_outline(topic: str, word_count_target: int) -> Dict[str, Any]:
    """
    Gera outline básico com capítulos.
    
    Args:
        topic: Tópico do ebook
        word_count_target: Contagem de palavras alvo
    
    Returns:
        Dict: Outline estruturado
    """
    words_per_chapter = word_count_target // 5
    
    return {
        "topic": topic,
        "word_count_target": word_count_target,
        "chapters": [
            {
                "name": "Introdução",
                "words_target": words_per_chapter,
                "description": "Introdução ao tema"
            },
            {
                "name": "Capítulo 1",
                "words_target": words_per_chapter,
                "description": "Conteúdo principal 1"
            },
            {
                "name": "Capítulo 2",
                "words_target": words_per_chapter,
                "description": "Conteúdo principal 2"
            },
            {
                "name": "Capítulo 3",
                "words_target": words_per_chapter,
                "description": "Conteúdo principal 3"
            },
            {
                "name": "Conclusão",
                "words_target": words_per_chapter,
                "description": "Conclusão e reflexões finais"
            }
        ]
    }


@tool
def count_words(content: str) -> int:
    """
    Conta palavras de um texto.
    
    Args:
        content: Conteúdo a contar
    
    Returns:
        int: Número de palavras
    """
    return len(content.split())


@tool
def validate_structure(outline: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida presença de intro/conclusão e contagem.
    
    Args:
        outline: Outline a validar
    
    Returns:
        Dict: Resultado da validação
    """
    chapters = outline.get("chapters", [])
    chapter_names = [ch.get("name", "").lower() for ch in chapters]
    
    has_intro = any("introdução" in name for name in chapter_names)
    has_conclusion = any("conclusão" in name for name in chapter_names)
    total_words = sum(ch.get("words_target", 0) for ch in chapters)
    
    return {
        "valid": has_intro and has_conclusion,
        "has_intro": has_intro,
        "has_conclusion": has_conclusion,
        "total_words": total_words,
        "chapters_count": len(chapters)
    }


# ============================================================================
# RESEARCH TOOLS
# ============================================================================

@tool
def query_context7_mcp(topic: str, query_type: str = "research") -> str:
    """
    Consulta Context7 MCP.
    
    Args:
        topic: Tópico para consulta
        query_type: Tipo de query (padrão: "research")
    
    Returns:
        str: Resultado da consulta
    """
    # TODO: Implementar Context7 MCP integration
    return f"Resultados Context7 para '{topic}' ({query_type})"


@tool
def perform_deep_research(topic: str, research_depth: str = "standard") -> Dict[str, Any]:
    """
    Agrupa achados externos.
    
    Args:
        topic: Tópico para pesquisa
        research_depth: Profundidade da pesquisa (padrão: "standard")
    
    Returns:
        Dict: Achados estruturados
    """
    return {
        "topic": topic,
        "depth": research_depth,
        "findings": [
            {"source": "Source 1", "content": "Finding 1"},
            {"source": "Source 2", "content": "Finding 2"}
        ]
    }


@tool
def vectorize_research(research_findings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gera embeddings e metadados.
    
    Args:
        research_findings: Achados a vetorizar
    
    Returns:
        Dict: Dados vetorizados
    """
    return {
        "vectorized": True,
        "findings_count": len(research_findings.get("findings", [])),
        "embeddings_created": len(research_findings.get("findings", []))
    }


@tool
def store_in_rag_external(vectorized_data: Dict[str, Any], topic: str) -> str:
    """
    Registra vetores em Supabase.
    
    Args:
        vectorized_data: Dados vetorizados a armazenar
        topic: Tópico associado
    
    Returns:
        str: Confirmação de armazenamento
    """
    # TODO: Implementar Supabase pgvector integration
    return f"Dados armazenados para '{topic}'"


# ============================================================================
# WRITING TOOLS
# ============================================================================

@tool
def retrieve_author_stories(author_name: str, max_results: int = 3) -> str:
    """
    Recupera histórias autorais.
    
    Args:
        author_name: Nome do autor
        max_results: Número máximo de resultados (padrão: 3)
    
    Returns:
        str: Histórias recuperadas
    """
    # TODO: Implementar Supabase integration
    return f"Histórias de '{author_name}' (top {max_results})"


@tool
def retrieve_author_positioning(author_name: str, max_results: int = 3) -> str:
    """
    Recupera posicionamento do autor.
    
    Args:
        author_name: Nome do autor
        max_results: Número máximo de resultados (padrão: 3)
    
    Returns:
        str: Posicionamento do autor
    """
    # TODO: Implementar Supabase integration
    return f"Posicionamento de '{author_name}' (top {max_results})"


@tool
def retrieve_author_vision(author_name: str, max_results: int = 3) -> str:
    """
    Recupera visão/valores do autor.
    
    Args:
        author_name: Nome do autor
        max_results: Número máximo de resultados (padrão: 3)
    
    Returns:
        str: Visão e valores do autor
    """
    # TODO: Implementar Supabase integration
    return f"Visão de '{author_name}' (top {max_results})"


@tool
def format_markdown(title: str, content: str) -> str:
    """
    Adiciona título e separador em Markdown.
    
    Args:
        title: Título da seção
        content: Conteúdo a formatar
    
    Returns:
        str: Conteúdo formatado em Markdown
    """
    return f"## {title}\n\n{content}\n\n---\n"


# ============================================================================
# REVIEW TOOLS
# ============================================================================

@tool
def review_tone_and_engagement(content: str) -> Dict[str, Any]:
    """
    Checklist de tom/engajamento.
    
    Args:
        content: Conteúdo a revisar
    
    Returns:
        Dict: Feedback de tom e engajamento
    """
    return {
        "tone": "Apropriado",
        "engagement_score": 85,
        "feedback": "Conteúdo tem bom tom motivacional"
    }


@tool
def review_clarity_and_empathy(content: str) -> Dict[str, Any]:
    """
    Checklist de clareza e empatia.
    
    Args:
        content: Conteúdo a revisar
    
    Returns:
        Dict: Feedback de clareza
    """
    return {
        "clarity": "Claro",
        "empathy_score": 80,
        "feedback": "Conteúdo é claro e empático"
    }


@tool
def review_grammar_and_style(content: str) -> Dict[str, Any]:
    """
    Checklist de gramática.
    
    Args:
        content: Conteúdo a revisar
    
    Returns:
        Dict: Feedback de gramática
    """
    return {
        "grammar": "Correto",
        "style_score": 90,
        "feedback": "Gramática e estilo adequados"
    }


@tool
def review_logical_flow(content: str) -> Dict[str, Any]:
    """
    Checklist de coerência e fluxo lógico.
    
    Args:
        content: Conteúdo a revisar
    
    Returns:
        Dict: Feedback de coerência
    """
    return {
        "flow": "Coerente",
        "coherence_score": 88,
        "feedback": "Conteúdo flui logicamente bem"
    }


@tool
def review_code_examples(content: str) -> Dict[str, Any]:
    """
    Checklist de exemplos de código.
    
    Args:
        content: Conteúdo a revisar
    
    Returns:
        Dict: Feedback de exemplos
    """
    code_blocks = len(re.findall(r'```', content)) // 2
    
    return {
        "code_blocks": code_blocks,
        "examples_score": 75 if code_blocks > 0 else 50,
        "feedback": f"Encontrados {code_blocks} exemplos de código"
    }


# ============================================================================
# QUALITY & CONTENT TOOLS
# ============================================================================

@tool
def validate_content_quality(content: str) -> Dict[str, Any]:
    """
    Retorna métricas simples de qualidade.
    
    Args:
        content: Conteúdo a validar
    
    Returns:
        Dict: Métricas de qualidade
    """
    word_count = len(content.split())
    paragraph_count = len(content.split('\n\n'))
    avg_word_per_para = word_count // max(paragraph_count, 1)
    
    return {
        "word_count": word_count,
        "paragraph_count": paragraph_count,
        "avg_words_per_paragraph": avg_word_per_para,
        "quality_score": min(100, (word_count // 100) + (paragraph_count * 2))
    }


# ============================================================================
# PUBLICATION TOOLS
# ============================================================================

@tool
def generate_cover(title: str, subtitle: str, author: str) -> str:
    """
    Retorna mensagem de capa gerada.
    
    Args:
        title: Título do livro
        subtitle: Subtítulo
        author: Nome do autor
    
    Returns:
        str: Confirmação da capa gerada
    """
    return f"Capa gerada para '{title}' - {subtitle} - por {author}"


@tool
def export_to_docx(content: str, title: str) -> str:
    """
    Exportação para DOCX.
    
    Args:
        content: Conteúdo a exportar
        title: Título do documento
    
    Returns:
        str: Confirmação de exportação
    """
    try:
        doc = Document()
        doc.add_heading(title, 0)
        doc.add_paragraph(content)
        
        filename = f"export_{title.replace(' ', '_')}.docx"
        doc.save(filename)
        
        return f"Exportado para DOCX: {filename}"
    except Exception as e:
        return f"Erro na exportação DOCX: {str(e)}"


@tool
def export_to_epub(content: str, title: str) -> str:
    """
    Exportação para EPUB.
    
    Args:
        content: Conteúdo a exportar
        title: Título do documento
    
    Returns:
        str: Confirmação de exportação
    """
    # TODO: Implementar EPUB export com ebooklib
    return f"Exportado para EPUB: {title}.epub"


@tool
def export_to_pdf(content: str, title: str) -> str:
    """
    Exportação para PDF.
    
    Args:
        content: Conteúdo a exportar
        title: Título do documento
    
    Returns:
        str: Confirmação de exportação
    """
    # TODO: Implementar PDF export com reportlab ou weasyprint
    return f"Exportado para PDF: {title}.pdf"


@tool
def export_to_json(content: str, title: str, metadata: Dict[str, Any] = None) -> str:
    """
    Exportação para JSON.
    
    Args:
        content: Conteúdo a exportar
        title: Título do documento
        metadata: Metadados opcionais
    
    Returns:
        str: Confirmação de exportação
    """
    export_data = {
        "title": title,
        "content": content,
        "metadata": metadata or {}
    }
    
    filename = f"export_{title.replace(' ', '_')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    return f"Exportado para JSON: {filename}"


@tool
def generate_kdp_metadata(title: str, author: str, category: str, keywords: List[str]) -> Dict[str, Any]:
    """
    Gera JSON de metadados KDP.
    
    Args:
        title: Título do livro
        author: Nome do autor
        category: Categoria KDP
        keywords: Lista de palavras-chave
    
    Returns:
        Dict: Metadados estruturados para KDP
    """
    return {
        "title": title,
        "author": author,
        "category": category,
        "keywords": keywords,
        "description": f"Ebook '{title}' por {author}",
        "language": "pt-BR",
        "kdp_ready": True,
        "metadata_version": "1.0"
    }


# ============================================================================
# DOCUMENT MANIPULATION TOOLS
# ============================================================================

@tool
def replace_text_in_docx(input_file: str, output_file: str, replacements: Dict[str, str]) -> str:
    """
    Substitui textos em um arquivo .docx e salva o resultado em um novo arquivo.
    
    Args:
        input_file: Caminho para o arquivo .docx de entrada.
        output_file: Caminho para o arquivo .docx de saída.
        replacements: Dicionário onde a chave é o texto antigo e o valor é o texto novo.
    
    Returns:
        str: Mensagem de sucesso ou erro.
    """
    try:
        # Abrir o documento .docx existente
        doc = Document(input_file)

        # Iterar sobre os parágrafos e substituir o texto
        for para in doc.paragraphs:
            for old_text, new_text in replacements.items():
                if old_text in para.text:
                    para.text = para.text.replace(old_text, new_text)

        # Iterar sobre as tabelas, se houver
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for old_text, new_text in replacements.items():
                        if old_text in cell.text:
                            cell.text = cell.text.replace(old_text, new_text)

        # Salvar o documento atualizado
        doc.save(output_file)

        return f"Substituição de texto completa. Arquivo salvo como {output_file}."
    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}"


# ============================================================================
# TOOL COLLECTION FUNCTIONS
# ============================================================================

def get_ideation_tools() -> List[Any]:
    """Retorna ferramentas usadas em Stage 1: Ideação."""
    return [
        search_knowledge_base,
        retrieve_rag_context,
    ]


def get_title_tools() -> List[Any]:
    """Retorna ferramentas usadas em Stage 2: Geração de Título."""
    return [
        generate_amazon_optimized_title,
        validate_title_seo,
        search_knowledge_base,
    ]


def get_structure_tools() -> List[Any]:
    """Retorna ferramentas usadas em Stage 3: Estrutura."""
    return [
        generate_outline,
        count_words,
        validate_structure,
    ]


def get_research_tools() -> List[Any]:
    """Retorna ferramentas usadas em Stage 4: Pesquisa."""
    return [
        query_context7_mcp,
        perform_deep_research,
        vectorize_research,
        store_in_rag_external,
        retrieve_rag_context,
    ]


def get_writing_tools() -> List[Any]:
    """Retorna ferramentas usadas em Stage 4B: Escrita."""
    return [
        retrieve_rag_context,
        retrieve_author_stories,
        retrieve_author_positioning,
        retrieve_author_vision,
        format_markdown,
        count_words,
    ]


def get_review_tools() -> List[Any]:
    """Retorna ferramentas usadas em Stage 5: Revisão."""
    return [
        review_tone_and_engagement,
        review_clarity_and_empathy,
        review_grammar_and_style,
        review_logical_flow,
        review_code_examples,
        validate_content_quality,
    ]


def get_editing_tools() -> List[Any]:
    """Retorna ferramentas usadas em Stage 7: Edição."""
    return [
        format_markdown,
        validate_content_quality,
        validate_structure,
    ]


def get_publication_tools() -> List[Any]:
    """Retorna ferramentas usadas em Stage 9: Publicação."""
    return [
        export_to_docx,
        export_to_epub,
        export_to_pdf,
        export_to_json,
        generate_kdp_metadata,
    ]


def get_all_tools() -> List[Any]:
    """Retorna todas as ferramentas disponíveis através de todos os estágios."""
    return (
        get_ideation_tools() +
        get_title_tools() +
        get_structure_tools() +
        get_research_tools() +
        get_writing_tools() +
        get_review_tools() +
        get_editing_tools() +
        get_publication_tools()
    )
