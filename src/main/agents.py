from crewai import Agent

from groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do Groq LLM
groq_api_key = os.getenv("GROQ_API_KEY")  # Substitua pela sua chave de API real

# Certifique-se de que a chave da API foi carregada corretamente
if not groq_api_key:
    raise ValueError("Chave API do Groq não encontrada. Defina a variável 'GROQ_API_KEY' no arquivo .env.")

# Configuração do Groq LLM
groq_llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-70b-versatile",  # Ou outro modelo disponível no Groq
    max_tokens=1024,
    temperature=0.7
)
# Definindo o agente inspirado por Roberto Shinyashiki e Pe. Fábio de Melo
writer_agent = Agent(
    role='Escritor de Autodesenvolvimento',
    goal=(
        "Criar um texto de autodesenvolvimento para iniciantes no autoconhecimento e na "
        "inteligência emocional, com uma abordagem prática e inspiradora."
    ),
    backstory=(
        "Escritor especialista em autodesenvolvimento, inspirado no estilo de escrita "
        "prático de Roberto Shinyashiki e na sensibilidade espiritual de Pe. Fábio de Melo, "
        "mas sem ser religioso. "
        "Sua missão é motivar, ensinar novas práticas e inspirar reflexão, usando uma linguagem "
        "simples, com um toque poético, explorando emoções e autoconhecimento."
    ),
    memory=True,
    verbose=True,
    llm=groq_llm
)