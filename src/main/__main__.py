"""
Pipeline de geração de ebook usando LangChain 1.0+.

Orquestra a execução sequencial dos agentes para gerar conteúdo de autodesenvolvimento.
"""

import time
from agents import writer_agent, create_writer_agent, groq_llm
from tasks import (
    INTRODUCTION_PROMPT,
    PROBLEMA_PROMPT,
    IDENTIFICACAO_PROMPT,
    SOLUCAO_PROMPT,
    PROTECAO_PROMPT,
    PERMISSAO_PROMPT,
    POTENCIA_PROMPT
)

ebook_config_path = 'config/ebook_config.json'
ebook_template_path = '../templates/ebook_template.docx'

# Lista de prompts para cada seção do ebook
EBOOK_SECTIONS = [
    ("Introdução", INTRODUCTION_PROMPT),
    ("Problema", PROBLEMA_PROMPT),
    ("Identificação", IDENTIFICACAO_PROMPT),
    ("Solução", SOLUCAO_PROMPT),
    ("Proteção", PROTECAO_PROMPT),
    ("Permissão", PERMISSAO_PROMPT),
    ("Potência", POTENCIA_PROMPT)
]

def execute_agent(agent, query: str) -> str:
    """
    Executa um agente com uma query e retorna a resposta.
    
    Args:
        agent: Instância do agente LangChain
        query: Query para executar
    
    Returns:
        str: Resposta do agente
    """
    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return response.get("output", str(response))

def generate_ebook():
    """
    Gera o ebook de forma sequencial, criando conteúdo para cada seção.
    """
    ebook_content = {}
    
    for section_name, prompt in EBOOK_SECTIONS:
        print(f"\n{'='*60}")
        print(f"Gerando: {section_name}")
        print(f"{'='*60}")
        
        # Executa o agente com o prompt da seção
        result = execute_agent(writer_agent, prompt)
        ebook_content[section_name] = result
        
        print(f"✓ {section_name} concluída")
        print("\nAguardando 2 segundos antes da próxima seção...")
        time.sleep(2)
    
    return ebook_content

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Iniciando geração de ebook")
    print("="*60)
    
    # Gera o ebook
    content = generate_ebook()
    
    print("\n" + "="*60)
    print("Ebook gerado com sucesso!")
    print("="*60)
    print("\nSeções geradas:")
    for section in content:
        print(f"  ✓ {section}")