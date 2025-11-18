"""
Definição de agentes usando LangChain 1.0+.
Agentes simples com system prompt bem definido.
"""

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools import get_all_tools

import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do Gemini LLM
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("Chave API do Google não encontrada. Defina a variável 'GOOGLE_API_KEY' no arquivo .env.")

# Inicialização do modelo Gemini 2.5 Flash (escrita rápida e criativa)
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=google_api_key,
    temperature=0.7,
    top_p=0.95,
    top_k=40
)

# Criação do agente de escrita com system prompt especializado
writer_agent = create_agent(
    model=gemini_llm,
    tools=get_all_tools(),
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