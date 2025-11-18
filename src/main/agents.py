"""
Definição de agentes usando LangChain 1.0+.
Agentes têm system prompts bem definidos e acessam ferramentas do módulo tasks.
"""

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from main.tasks import get_all_tasks, replace_text_in_docx

import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do Groq LLM
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Chave API do Groq não encontrada. Defina a variável 'GROQ_API_KEY' no arquivo .env.")

# Inicialização do modelo Groq
groq_llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama-3.1-70b-versatile",
    temperature=0.7
)

def create_writer_agent(model):
    """
    Cria um agente de escrita para autodesenvolvimento usando LangChain 1.0+.
    
    Args:
        model: Instância do modelo de linguagem
    
    Returns:
        Agent: Agente configurado para escrita com prompt especializado
    """
    return create_agent(
        model=model,
        tools=get_all_tasks() + [replace_text_in_docx],
        system_prompt="""Você é um Escritor de Autodesenvolvimento Especialista.

Responsabilidade Principal:
Criar conteúdo inspirador e transformador sobre autoconhecimento e inteligência emocional,
combinando narrativa envolvente com orientação prática.

Áreas de Foco:
1. Histórias que capturam atenção e criam conexão emocional
2. Conceitos explicados de forma acessível e poética
3. Métodos práticos e implementáveis no dia a dia
4. Reflexão profunda sobre emoções e desenvolvimento pessoal
5. Linguagem que motiva sem ser religiosa

Processo de Escrita:
- Comece com histórias reais que ressoem com o leitor
- Construa conceitos passo a passo
- Forneça exemplos concretos e relevantes
- Termine com reflexão inspiradora e chamado à ação
- Use ferramentas disponíveis para estruturar conteúdo

Estilo:
- Motivacional mas autêntico
- Simples mas profundo
- Poético mas prático
- Inclusivo e acessível

Use as ferramentas disponíveis (write_introduction, write_problem_chapter, etc.)
para estruturar cada seção do ebook. Cada ferramenta fornece diretrizes específicas
sobre o que incluir."""
    )

# Instância global do agente de escrita
writer_agent = create_writer_agent(groq_llm)