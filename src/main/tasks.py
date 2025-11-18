"""
Config loader para BRD e estrutura de capítulos.
Carrega configuration do YAML para gerar queries do agente.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any

def load_brd() -> Dict[str, Any]:
    """
    Carrega o BRD do arquivo specs/brd.yaml.
    
    Returns:
        dict: BRD carregado com todas as configurações
    """
    brd_path = Path(__file__).parent.parent.parent / "specs" / "brd.yaml"
    
    with open(brd_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_chapters() -> List[Dict[str, Any]]:
    """
    Retorna lista de capítulos do BRD.
    
    Returns:
        list: Capítulos com name, purpose, elements
    """
    brd = load_brd()
    return brd["content_structure"]["chapters"]

def get_chapter_query(chapter: Dict[str, Any], brd: Dict[str, Any]) -> str:
    """
    Constrói uma query para o agente baseada na configuração do BRD.
    
    Args:
        chapter: Configuração do capítulo do BRD
        brd: BRD completo com writing_style, etc
    
    Returns:
        str: Query estruturada para o agente
    """
    name = chapter["name"]
    purpose = chapter["purpose"]
    elements = "\n".join([f"  - {elem}" for elem in chapter["elements"]])
    
    style = brd["writing_style"]
    inspiration = ", ".join(style["inspiration"])
    tone = style["tone"]
    approach = style["approach"]
    
    characteristics = "\n".join([f"  • {char}" for char in style["characteristics"]])
    
    return f"""Gere o capítulo "{name}" do ebook.

PROPÓSITO:
{purpose}

ELEMENTOS A INCLUIR:
{elements}

CONTEXTO DE ESCRITA:
- Tom: {tone}
- Abordagem: {approach}
- Inspiração: {inspiration}

CARACTERÍSTICAS DO ESTILO:
{characteristics}

Público-alvo: {brd['project']['target_audience']}

Escreva o conteúdo deste capítulo seguindo as orientações acima.
Mantenha a linguagem motivacional, acessível mas profunda.
Inclua histórias e exemplos práticos quando apropriado.
Assegure que o conteúdo seja inspirador e transformador."""

def get_all_chapters_queries() -> List[tuple]:
    """
    Retorna lista de tuplas (chapter_name, query) para todos os capítulos.
    
    Returns:
        list: Lista de tuplas com nome do capítulo e query para agent
    """
    brd = load_brd()
    chapters = get_chapters()
    
    queries = []
    for chapter in chapters:
        query = get_chapter_query(chapter, brd)
        queries.append((chapter["name"], query))
    
    return queries