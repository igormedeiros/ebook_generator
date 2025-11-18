"""
Pipeline de geração de ebook usando LangChain 1.0+.

Orquestra a execução sequencial dos agentes com as ferramentas de tarefas
para gerar conteúdo de autodesenvolvimento.
"""

import time
from agents import writer_agent, groq_llm
from tasks import (
    write_introduction,
    write_problem_chapter,
    write_identification_chapter,
    write_solution_chapter,
    write_protection_chapter,
    write_permission_chapter,
    write_power_chapter
)

ebook_config_path = 'config/ebook_config.json'
ebook_template_path = '../templates/ebook_template.docx'

# Configuração das seções do ebook com seus parâmetros
EBOOK_SECTIONS = [
    {
        "name": "Introdução",
        "tool": write_introduction,
        "params": {
            "topic": "Autoconhecimento e Inteligência Emocional",
            "audience": "Iniciantes em desenvolvimento pessoal"
        }
    },
    {
        "name": "Problema",
        "tool": write_problem_chapter,
        "params": {
            "topic": "Gestão emocional e autoconhecimento",
            "context": "Desafios comuns no desenvolvimento pessoal"
        }
    },
    {
        "name": "Identificação",
        "tool": write_identification_chapter,
        "params": {
            "author_stories": {
                "Superação pessoal": "História de como superei meus limites",
                "Transformação": "Jornada de mudança e crescimento"
            }
        }
    },
    {
        "name": "Solução",
        "tool": write_solution_chapter,
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
        "tool": write_protection_chapter,
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
        "tool": write_permission_chapter,
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
        "tool": write_power_chapter,
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
    Gera uma seção específica do ebook usando a ferramenta correspondente.
    
    Args:
        section_config: Configuração da seção com tool e parâmetros
    
    Returns:
        dict: Resultado da seção com nome e conteúdo
    """
    section_name = section_config["name"]
    tool = section_config["tool"]
    params = section_config["params"]
    
    print(f"\n{'='*60}")
    print(f"Gerando: {section_name}")
    print(f"{'='*60}")
    
    # Chama a ferramenta com os parâmetros específicos
    tool_result = tool.invoke(params)
    
    # Executa o agente com o resultado da ferramenta
    query = f"Com base nesta estrutura:\n\n{tool_result}\n\nGere o conteúdo da seção '{section_name}'"
    agent_result = execute_agent(writer_agent, query)
    
    print(f"✓ {section_name} concluída")
    
    return {
        "section": section_name,
        "tool_guidance": tool_result,
        "content": agent_result
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