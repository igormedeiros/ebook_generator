#!/usr/bin/env python
"""
Script de teste para validar pipeline de research e salvamento em kb/
Executa apenas os primeiros 2 capítulos para teste rápido.
"""

import os
import sys

import pytest

sys.path.insert(0, '/home/igormedeiros/projects/ebook-generator')

if (
    os.getenv("PYTEST_CURRENT_TEST")
    or not os.getenv("GOOGLE_API_KEY")
    or os.getenv("GOOGLE_API_KEY") == "test-api-key"
):
    pytest.skip("Research integration test requires live credentials", allow_module_level=True)

from src.main import load_brd, generate_chapter_structure, generate_chapter_research, save_research_to_kb

def test_research():
    """Testa geração de research e salvamento em kb/"""
    brd = load_brd()
    
    # Gera estrutura
    chapters = generate_chapter_structure(brd)
    if not chapters:
        print("❌ Falha ao gerar estrutura")
        return
    
    print(f"✓ Estrutura gerada com {len(chapters)} capítulos")
    
    # Testa research nos 2 primeiros capítulos
    for i, chapter in enumerate(chapters[:2], 1):
        print(f"\n[{i}] Testando research: {chapter['name']}")
        
        # Gera research
        research = generate_chapter_research(
            chapter['name'],
            chapter['purpose'],
            chapter['elements'],
            brd
        )
        
        # Salva em kb/
        kb_path = save_research_to_kb(chapter['name'], research, brd)
        print(f"  ✓ Salvo em: {kb_path}")
        print(f"  Tamanho: {len(research)} caracteres")

if __name__ == "__main__":
    test_research()
