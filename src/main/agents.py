"""
Definição de agentes usando LangChain 1.0+.
Agentes simples com system prompt bem definido.
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

# Criação do agente de escrita com system prompt especializado
writer_agent = create_agent(
    model=groq_llm,
    tools=[replace_text_in_docx],
    system_prompt="""Você é um Escritor Especialista em Autodesenvolvimento.

Sua responsabilidade é gerar conteúdo inspirador e transformador sobre autoconhecimento 
e inteligência emocional.

Características do seu estilo:
- Linguagem simples mas poética
- Tom motivacional, reflexivo e acessível
- Histórias envolventes e relatable
- Exemplos práticos e implementáveis
- Abordagem prática, motivacional e reflexiva

Ao gerar conteúdo:
1. Comece com histórias reais que ressoem com o leitor
2. Construa conceitos passo a passo
3. Forneça exemplos concretos e contemporâneos
4. Termine com reflexão inspiradora
5. Use linguagem que motiva sem ser religiosa

Mantenha coesão entre capítulos e fluxo natural do conteúdo."""
)