#!/usr/bin/env python3
"""
Quick test: Ideation com sistema de fallback
"""

import sys
from src.agents import create_ideation_agent, execute_agent
from src.llm_fallback import get_llm_fallback
from src.config import get_logger, get_config

logger = get_logger(__name__)


def main():
    logger.info("=" * 70)
    logger.info("🚀 TESTE: IDEAÇÃO COM FALLBACK")
    logger.info("=" * 70)
    
    # Get fallback orchestrator
    fallback = get_llm_fallback()
    logger.info(f"\n✅ Orquestrador de fallback criado com {len(fallback.models)} modelos:")
    for idx, model in enumerate(fallback.models, 1):
        logger.info(f"   {idx}. {model['name']}: {model['description']}")
    
    # Try to get write model
    logger.info("\n📝 Tentando obter modelo de escrita...")
    try:
        write_model = fallback.get_write_model()
        logger.info(f"✅ Modelo obtido: {type(write_model).__name__}\n")
    except Exception as e:
        logger.error(f"❌ Falha: {e}")
        return
    
    # Create ideation agent
    logger.info("🤖 Criando agente de ideação...")
    ideation_agent = create_ideation_agent(write_model)
    logger.info("✅ Agente criado\n")
    
    # Build prompt
    logger.info("📋 Carregando template de prompt...")
    agent_prompts = get_config("agent_prompts")
    logger.info("✅ Template carregado\n")
    
    logger.info("🔧 Montando prompt...")
    topic = "AI Agents em Saúde"
    target_audience = "Desenvolvedores Python"
    word_count_target = 5000
    reading_level = "intermediate"
    promise_context = "Dominar desenvolvimento de agentes"
    
    ideation_prompt = agent_prompts["ideation_prompt_template"].format(
        topic=topic,
        target_audience=target_audience,
        word_count_target=word_count_target,
        reading_level=reading_level,
        promise_context=promise_context,
    )
    logger.info(f"✅ Prompt montado ({len(ideation_prompt)} chars)\n")
    
    # Execute with fallback
    logger.info("⏳ Executando ideação com fallback (pode usar até 3 modelos diferentes)...")
    logger.info("-" * 70)
    
    try:
        result = execute_agent(ideation_agent, ideation_prompt)
        logger.info("-" * 70)
        logger.info("\n✅ SUCESSO!\n")
        logger.info(f"📤 RESULTADO:\n{result}\n")
        logger.info("=" * 70)
    except Exception as e:
        logger.error(f"❌ FALHA: {e}")


if __name__ == "__main__":
    main()
