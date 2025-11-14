#!/usr/bin/env python3
"""
Test script to demonstrate Stage 1: Ideation with full logging.
"""

import sys
from src.agents import create_ideation_agent, execute_agent
from src.config import get_logger, get_model, get_config

logger = get_logger(__name__)


def test_ideation():
    """Test ideation stage with full output."""
    logger.info("=" * 70)
    logger.info("🚀 TESTE: ESTÁGIO 1 - IDEAÇÃO")
    logger.info("=" * 70)
    
    # Get model
    logger.info("📊 Carregando modelo Gemini 2.5 Flash...")
    write_model = get_model()
    logger.info(f"✅ Modelo carregado: {type(write_model).__name__}")
    
    # Create agent
    logger.info("\n🤖 Criando agente de ideação...")
    ideation_agent = create_ideation_agent(write_model)
    logger.info(f"✅ Agente criado com sucesso")
    
    # Load template
    logger.info("\n📋 Carregando template de prompt...")
    agent_prompts = get_config("agent_prompts")
    logger.info(f"✅ Template carregado")
    
    # Build prompt
    logger.info("\n🔧 Montando prompt de ideação...")
    topic = "Desenvolvimento de agentes de Inteligência Artificial na Saúde com LangChain 1.0"
    target_audience = "Profissionais de TI e Desenvolvedores Python"
    word_count_target = 15000
    reading_level = "intermediate"
    promise_context = "Dominar desenvolvimento de agentes de IA para aplicações em saúde"
    
    ideation_prompt = agent_prompts["ideation_prompt_template"].format(
        topic=topic,
        target_audience=target_audience,
        word_count_target=word_count_target,
        reading_level=reading_level,
        promise_context=promise_context,
    )
    logger.info(f"✅ Prompt montado ({len(ideation_prompt)} caracteres)")
    logger.info(f"\n📋 PROMPT:\n{'-' * 70}\n{ideation_prompt}\n{'-' * 70}\n")
    
    # Execute agent
    logger.info("\n⏳ Executando agente de ideação (Gemini 2.5 Flash)...")
    logger.info("Aguardando resposta da IA...\n")
    
    try:
        ideation_output = execute_agent(ideation_agent, ideation_prompt)
        
        logger.info(f"\n{'=' * 70}")
        logger.info("✅ IDEAÇÃO CONCLUÍDA COM SUCESSO!")
        logger.info(f"{'=' * 70}")
        
        logger.info(f"\n📤 RESULTADO COMPLETO DA IDEAÇÃO:")
        logger.info(f"{'-' * 70}")
        logger.info(f"\n{ideation_output}\n")
        logger.info(f"{'-' * 70}")
        
        logger.info(f"\n📊 ESTATÍSTICAS:")
        logger.info(f"  • Comprimento da resposta: {len(ideation_output)} caracteres")
        logger.info(f"  • Número de palavras: ~{len(ideation_output.split())} palavras")
        logger.info(f"  • Número de linhas: {len(ideation_output.splitlines())} linhas")
        
        return ideation_output
        
    except Exception as e:
        logger.error(f"❌ ERRO na execução: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    test_ideation()
