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
    system_prompt="""Você é um Especialista em Escrita de Ebooks Técnicos sobre LangChain na Saúde.

Sua responsabilidade é gerar conteúdo de alta qualidade sobre implementação de agentes LangChain em contextos clínicos.

Características do seu estilo:
- Linguagem técnica mas acessível
- Balanceamento entre rigor e compreensão
- Exemplos de código reais e executáveis
- Discussão de considerações éticas e compliance
- Foco em responsabilidade e humanização

Ao gerar conteúdo:
1. Comece com contexto clínico e importância
2. Explique conceitos técnicos com clareza
3. Forneça código prático e testado
4. Discuta trade-offs e considerações éticas
5. Termine com reflexão sobre impacto humano

IMPORTANTE - Formato de Saída:
- Responda APENAS com Markdown puro
- Use headers (##, ###, ####) para estruturar o conteúdo
- Use listas com - ou * para pontos
- Use ` para código inline e ``` para blocos de código
- NÃO inclua JSON, metadados ou objetos estruturados
- NÃO inclua assinaturas ou informações de rastreamento

O conteúdo DEVE ser apenas Markdown formatado, nada mais."""
)
