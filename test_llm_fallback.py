#!/usr/bin/env python3
"""
Test script to demonstrate LLM Fallback mechanism.
Tests the sequence: Gemini Pro -> Gemini Flash -> Groq
"""

import sys
from src.llm_fallback import get_llm_fallback
from src.config import get_logger

logger = get_logger(__name__)


def test_fallback_initialization():
    """Test LLM fallback initialization."""
    logger.info("=" * 70)
    logger.info("🧪 TESTE: MECANISMO DE FALLBACK DE LLM")
    logger.info("=" * 70)
    
    logger.info("\n📊 Inicializando orquestrador de fallback...")
    fallback = get_llm_fallback()
    logger.info(f"✅ Orquestrador criado com {len(fallback.models)} modelos")
    
    logger.info("\n📋 Modelos disponíveis em sequência:")
    for idx, model in enumerate(fallback.models, 1):
        logger.info(f"  {idx}. {model['name']}")
        logger.info(f"     {model['description']}")
    
    logger.info("\n" + "=" * 70)
    logger.info("🔄 TESTE 1: Obtendo modelo de pesquisa (com fallback)")
    logger.info("=" * 70)
    
    try:
        research_model = fallback.get_research_model()
        logger.info(f"\n✅ SUCESSO!")
        logger.info(f"   Modelo obtido: {type(research_model).__name__}")
        logger.info(f"   Tipo: {research_model}")
    except Exception as e:
        logger.error(f"\n❌ FALHA: {str(e)}")
    
    logger.info("\n" + "=" * 70)
    logger.info("🔄 TESTE 2: Obtendo modelo de escrita (com fallback)")
    logger.info("=" * 70)
    
    try:
        write_model = fallback.get_write_model()
        logger.info(f"\n✅ SUCESSO!")
        logger.info(f"   Modelo obtido: {type(write_model).__name__}")
        logger.info(f"   Tipo: {write_model}")
    except Exception as e:
        logger.error(f"\n❌ FALHA: {str(e)}")
    
    logger.info("\n" + "=" * 70)
    logger.info("✨ TESTES CONCLUÍDOS")
    logger.info("=" * 70)


if __name__ == "__main__":
    test_fallback_initialization()
