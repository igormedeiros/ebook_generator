"""
Pipeline de geração de ebook usando LangChain 1.0+.

Orquestra a execução sequencial dos agentes com guidance estruturado
para gerar conteúdo de autodesenvolvimento.
"""

import time
from agents import writer_agent
from tasks import (
    get_introduction_guidance,
    get_problem_chapter_guidance,
    get_identification_chapter_guidance,
    get_solution_chapter_guidance,
    get_protection_chapter_guidance,
    get_permission_chapter_guidance,
    get_power_chapter_guidance
)

ebook_config_path = 'config/ebook_config.json'
ebook_template_path = '../templates/ebook_template.docx'

# Configuração das seções do ebook com seus parâmetros e funções de guidance
EBOOK_SECTIONS = [
    {
        "name": "Introdução",
        "guidance_fn": get_introduction_guidance,
        "params": {
            "topic": "Autoconhecimento e Inteligência Emocional",
            "audience": "Iniciantes em desenvolvimento pessoal"
        }
    },
    {
        "name": "Problema",
        "guidance_fn": get_problem_chapter_guidance,
        "params": {
            "topic": "Gestão emocional e autoconhecimento",
            "context": "Desafios comuns no desenvolvimento pessoal"
        }
    },
    {
        "name": "Identificação",
        "guidance_fn": get_identification_chapter_guidance,
        "params": {
            "author_stories": {
                "Superação pessoal": "História de como superei meus limites",
                "Transformação": "Jornada de mudança e crescimento"
            }
        }
    },
    {
        "name": "Solução",
        "guidance_fn": get_solution_chapter_guidance,
        "params": {
            "method_name": "Método de Inteligência Emocional",
            "steps": [
                "Reconhecer emoções",
                "Compreender origem",
                "Integrar aprendizado",
                "Aplicar na vida"
            ]
        }
    },
    {
        "name": "Proteção",
        "guidance_fn": get_protection_chapter_guidance,
        "params": {
            "risks": [
                "Autossabotagem e dúvida de si",
                "Influências externas negativas",
                "Falta de consistência"
            ]
        }
    },
    {
        "name": "Permissão",
        "guidance_fn": get_permission_chapter_guidance,
        "params": {
            "affirmations": [
                "Você merece ser feliz",
                "Você tem direito de crescer",
                "Sua transformação é possível"
            ]
        }
    },
    {
        "name": "Potência",
        "guidance_fn": get_power_chapter_guidance,
        "params": {
            "celebration_elements": {
                "Progresso": "Celebrar avanços realizados",
                "Potencial": "Reconhecer capacidade de transformação"
            }
        }
    }
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

def generate_ebook_section(section_config: dict) -> dict:
    """
    Gera uma seção específica do ebook usando guidance estruturado.
    
    Args:
        section_config: Configuração da seção com guidance_fn e parâmetros
    
    Returns:
        dict: Resultado da seção com nome e conteúdo
    """
    section_name = section_config["name"]
    guidance_fn = section_config["guidance_fn"]
    params = section_config["params"]
    
    print(f"\n{'='*60}")
    print(f"Gerando: {section_name}")
    print(f"{'='*60}")
    
    # Obtém guidance estruturado para a seção
    guidance = guidance_fn(**params)
    
    # Executa o agente com o guidance
    query = f"{guidance}\n\nGere o conteúdo desta seção agora."
    content = execute_agent(writer_agent, query)
    
    print(f"✓ {section_name} concluída")
    
    return {
        "section": section_name,
        "guidance": guidance,
        "content": content
    }

def generate_ebook() -> dict:
    """
    Gera o ebook completo de forma sequencial.
    
    Returns:
        dict: Dicionário com conteúdo de todas as seções
    """
    ebook_content = {
        "title": "Autoconhecimento e Inteligência Emocional",
        "sections": []
    }
    
    for section_config in EBOOK_SECTIONS:
        section_result = generate_ebook_section(section_config)
        ebook_content["sections"].append(section_result)
        
        print("\nAguardando 2 segundos antes da próxima seção...")
        time.sleep(2)
    
    return ebook_content

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Iniciando geração de ebook com LangChain 1.0+")
    print("="*60)
    
    # Gera o ebook
    content = generate_ebook()
    
    print("\n" + "="*60)
    print("Ebook gerado com sucesso!")
    print("="*60)
    print("\nSeções geradas:")
    for section in content["sections"]:
        print(f"  ✓ {section['section']}")
    
    print(f"\nTotal: {len(content['sections'])} seções concluídas")