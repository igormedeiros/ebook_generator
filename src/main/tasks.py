"""
Definições de ferramentas customizadas para o pipeline de escrita usando LangChain 1.0+.
Cada ferramenta implementa uma etapa específica do processo de geração de ebook.
"""

from langchain.tools import tool
from typing import Dict

@tool
def write_introduction(topic: str, audience: str) -> str:
    """
    Gera a introdução do ebook sobre autoconhecimento e inteligência emocional.
    
    Args:
        topic: Tema principal do ebook
        audience: Público-alvo
    
    Returns:
        str: Introdução motivacional e reflexiva com história envolvente
    """
    return f"""
    Ferramentas necessárias para escrever a introdução:
    - Tema: {topic}
    - Público: {audience}
    
    A introdução deve:
    1. Apresentar o tema central
    2. Mostrar o que o leitor pode esperar
    3. Explicar a importância do autoconhecimento e inteligência emocional
    4. Usar uma história breve e envolvente que capture a atenção
    5. Criar conexão emocional desde o início
    """

@tool
def write_problem_chapter(topic: str, context: str) -> str:
    """
    Escreve o capítulo sobre o problema que o livro se propõe a resolver.
    
    Args:
        topic: Tema do ebook
        context: Contexto ou informações adicionais
    
    Returns:
        str: Explicação detalhada dos problemas relacionados ao tema
    """
    return f"""
    Ferramentas para escrever o capítulo 'Problema':
    - Tema: {topic}
    - Contexto: {context}
    
    Este capítulo deve:
    1. Abordar o problema central do livro
    2. Descrever os desafios que as pessoas enfrentam
    3. Discutir consequências de não lidar com as emoções adequadamente
    4. Mostrar impacto na vida pessoal e profissional
    5. Incluir exemplos práticos e relevantes
    """

@tool
def write_identification_chapter(author_stories: Dict[str, str]) -> str:
    """
    Escreve o capítulo de identificação com histórias pessoais.
    
    Args:
        author_stories: Dicionário com histórias do autor relacionadas ao tema
    
    Returns:
        str: Histórias que criam conexão emocional com o leitor
    """
    stories_summary = ", ".join([f"{k}: {v[:50]}..." for k, v in author_stories.items()])
    return f"""
    Ferramentas para escrever o capítulo 'Identificação':
    - Histórias disponíveis: {stories_summary}
    
    Este capítulo deve:
    1. Utilizar histórias pessoais para criar conexão emocional
    2. Compartilhar experiências que ressoem com o leitor
    3. Demonstrar como lidar com emoções
    4. Mostrar desafios pessoais superados
    5. Permitir que o leitor se identifique com as experiências
    """

@tool
def write_solution_chapter(method_name: str, steps: list) -> str:
    """
    Escreve o capítulo sobre a solução proposta no ebook.
    
    Args:
        method_name: Nome do método apresentado
        steps: Passos do método
    
    Returns:
        str: Método prático com instruções passo a passo
    """
    steps_text = "\n".join([f"   {i+1}. {step}" for i, step in enumerate(steps)])
    return f"""
    Ferramentas para escrever o capítulo 'Solução':
    - Método: {method_name}
    - Passos:
{steps_text}
    
    Este capítulo deve:
    1. Apresentar um método prático para os leitores
    2. Dar um nome memorável ao método
    3. Criar um acrônimo fácil de lembrar
    4. Explicar passo a passo como aplicar no cotidiano
    5. Incluir exemplos práticos e implementáveis
    6. Oferecer ferramentas concretas para trabalho pessoal
    """

@tool
def write_protection_chapter(risks: list) -> str:
    """
    Escreve o capítulo sobre comportamentos prejudiciais a evitar.
    
    Args:
        risks: Lista de riscos ou armadilhas comuns
    
    Returns:
        str: Análise de armadilhas e dicas de como evitá-las
    """
    risks_text = "\n".join([f"   - {risk}" for risk in risks])
    return f"""
    Ferramentas para escrever o capítulo 'Proteção':
    - Armadilhas comuns:
{risks_text}
    
    Este capítulo deve:
    1. Alertar sobre comportamentos que prejudicam progresso
    2. Discutir armadilhas comuns
    3. Explicar como evitá-las
    4. Conscientizar sobre autossabotagem
    5. Fornecer dicas claras de manutenção do foco
    6. Destacar importância de manter consciência
    """

@tool
def write_permission_chapter(affirmations: list) -> str:
    """
    Escreve o capítulo de permissão psicológica para o leitor.
    
    Args:
        affirmations: Lista de afirmações inspiradoras
    
    Returns:
        str: Mensagens inspiradoras e de incentivo
    """
    affirmations_text = "\n".join([f"   • {aff}" for aff in affirmations])
    return f"""
    Ferramentas para escrever o capítulo 'Permissão':
    - Afirmações:
{affirmations_text}
    
    Este capítulo deve:
    1. Fornecer permissão psicológica aos leitores
    2. Reforçar que merecem ser felizes
    3. Afirmar direito de buscar o melhor para si
    4. Usar frases inspiradoras e empoderadoras
    5. Encorajar a crença no potencial de mudança
    6. Criar espaço seguro para transformação
    """

@tool
def write_power_chapter(celebration_elements: Dict[str, str]) -> str:
    """
    Escreve o capítulo final de celebração e empoderamento.
    
    Args:
        celebration_elements: Elementos a celebrar e reforçar
    
    Returns:
        str: Texto motivacional final com linguagem empoderada
    """
    elements_text = "\n".join([f"   {k}: {v}" for k, v in celebration_elements.items()])
    return f"""
    Ferramentas para escrever o capítulo 'Potência':
    - Elementos de celebração:
{elements_text}
    
    Este capítulo deve:
    1. Celebrar o progresso e aprendizados
    2. Motivar abraçar a mudança
    3. Usar linguagem poderosa e energizante
    4. Encorajar ação e aplicação prática
    5. Reforçar ideia de estar no caminho certo
    6. Deixar leitor com sentimento de empoderamento
    7. Inspirar determinação para jornada contínua
    """

def get_all_tasks() -> list:
    """
    Retorna lista com todas as ferramentas de tarefas disponíveis.
    
    Returns:
        list: Lista de ferramentas do LangChain
    """
    return [
        write_introduction,
        write_problem_chapter,
        write_identification_chapter,
        write_solution_chapter,
        write_protection_chapter,
        write_permission_chapter,
        write_power_chapter
    ]