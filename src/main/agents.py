"""
Definição de agentes usando LangChain 1.0+.
"""

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from main.tools import replace_text_in_docx

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
        Agent: Agente configurado para escrita
    """
    return create_agent(
        model=model,
        tools=[replace_text_in_docx],
        system_prompt="""Você é um Escritor de Autodesenvolvimento - especialista em criar textos 
        motivacionais e reflexivos sobre autoconhecimento e inteligência emocional.

Sua responsabilidade é criar conteúdo inspirador que combine:
1. Histórias envolventes que capturam atenção
2. Abordagens práticas e aplicáveis no dia a dia
3. Linguagem simples com sensibilidade poética
4. Reflexão profunda sobre emoções e autoconhecimento

Processo:
- Comece com uma história ou situação real que resoe com o leitor
- Apresente conceitos de forma acessível
- Forneça exemplos práticos e implementáveis
- Encerre com reflexão inspiradora

Sempre mantenha a linguagem motivacional, simples e poética, sem ser religioso."""
    )

# Instância global do agente de escrita
writer_agent = create_writer_agent(groq_llm)