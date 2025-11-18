"""
Funções de guidance para cada etapa do pipeline de escrita usando LangChain 1.0+.
Estas funções retornam diretivas estruturadas para guiar o agente na geração de conteúdo.
NÃO são ferramentas LangChain - apenas funções Python que orientam a escrita.
"""

from typing import Dict

def get_introduction_guidance(topic: str, audience: str) -> str:
    """
    Retorna guidance estruturado para escrita da introdução.
    
    Args:
        topic: Tema principal do ebook
        audience: Público-alvo
    
    Returns:
        str: Guidance estruturado para o agente
    """
    return f"""
GUIDANCE PARA INTRODUÇÃO
========================

Tema: {topic}
Público-alvo: {audience}

Estrutura esperada:
1. Apresentar o tema central de forma envolvente
2. Mostrar o que o leitor pode esperar do conteúdo
3. Explicar a importância do autoconhecimento e inteligência emocional
4. Usar uma história breve e envolvente que capture a atenção
5. Criar conexão emocional desde o início

Tom: Motivacional, reflexivo, acessível mas profundo.
Comprimento estimado: 500-800 palavras.
"""

def get_problem_chapter_guidance(topic: str, context: str) -> str:
    """
    Retorna guidance para o capítulo sobre problemas/desafios.
    
    Args:
        topic: Tema do ebook
        context: Contexto ou informações adicionais
    
    Returns:
        str: Guidance estruturado para o agente
    """
    return f"""
GUIDANCE PARA CAPÍTULO: PROBLEMA
=================================

Tema: {topic}
Contexto: {context}

O que incluir:
1. Descrever o problema central que o livro aborda
2. Listar os desafios principais que as pessoas enfrentam
3. Explicar as consequências de não lidar adequadamente com emoções
4. Mostrar impacto na vida pessoal, profissional e relacionamentos
5. Incluir exemplos práticos e contemporâneos

Tom: Empático, realista mas não depressivo
Estrutura: Problema → Consequências → Exemplos práticos
Comprimento: 1000-1500 palavras
"""

def get_identification_chapter_guidance(author_stories: Dict[str, str]) -> str:
    """
    Retorna guidance para capítulo de identificação com histórias.
    
    Args:
        author_stories: Dicionário com histórias do autor
    
    Returns:
        str: Guidance estruturado para o agente
    """
    stories_list = "\n".join([f"  - {k}: {v[:60]}..." for k, v in author_stories.items()])
    return f"""
GUIDANCE PARA CAPÍTULO: IDENTIFICAÇÃO
======================================

Histórias disponíveis:
{stories_list}

Objetivo: Criar conexão emocional através de histórias pessoais

O que incluir:
1. Apresentar as histórias pessoais de forma envolvente
2. Mostrar os desafios pessoais superados
3. Conectar experiências com os leitores de forma relatable
4. Demonstrar lições aprendidas em cada história
5. Permitir que o leitor se veja nas situações descritas

Tom: Pessoal, autêntico, vulnerável mas empoderado
Estrutura: Situação → Desafio → Aprendizado → Lição
Comprimento: 1200-1800 palavras
"""

def get_solution_chapter_guidance(method_name: str, steps: list) -> str:
    """
    Retorna guidance para capítulo sobre a solução/método.
    
    Args:
        method_name: Nome do método apresentado
        steps: Passos/fases do método
    
    Returns:
        str: Guidance estruturado para o agente
    """
    steps_formatted = "\n".join([f"  {i+1}. {step}" for i, step in enumerate(steps)])
    return f"""
GUIDANCE PARA CAPÍTULO: SOLUÇÃO
================================

Método: {method_name}

Passos a apresentar:
{steps_formatted}

O que incluir:
1. Apresentar o método de forma clara e memorável
2. Criar um acrônimo fácil de lembrar (se aplicável)
3. Explicar CADA passo de forma detalhada
4. Fornecer exemplos práticos de como aplicar no dia a dia
5. Oferecer exercícios ou atividades práticas
6. Mostrar resultados esperados

Tom: Prático, instrutivo, motivador
Estrutura: Visão geral → Detalhamento de cada passo → Exemplos → Exercícios
Comprimento: 1500-2000 palavras
"""

def get_protection_chapter_guidance(risks: list) -> str:
    """
    Retorna guidance para capítulo sobre proteção/armadilhas.
    
    Args:
        risks: Lista de riscos ou armadilhas comuns
    
    Returns:
        str: Guidance estruturado para o agente
    """
    risks_formatted = "\n".join([f"  - {risk}" for risk in risks])
    return f"""
GUIDANCE PARA CAPÍTULO: PROTEÇÃO
=================================

Armadilhas comuns a abordar:
{risks_formatted}

O que incluir:
1. Alertar sobre comportamentos que prejudicam o progresso
2. Explicar as armadilhas mais comuns
3. Descrever sinais de quando você está caindo na armadilha
4. Oferecer estratégias concretas para evitá-las
5. Reforçar importância da autoconsciência

Tom: Advertência compassiva, não julgador
Estrutura: Armadilha → Sinais de alerta → Estratégias de prevenção
Comprimento: 1000-1300 palavras
"""

def get_permission_chapter_guidance(affirmations: list) -> str:
    """
    Retorna guidance para capítulo de permissão psicológica.
    
    Args:
        affirmations: Lista de afirmações inspiradoras
    
    Returns:
        str: Guidance estruturado para o agente
    """
    affirmations_formatted = "\n".join([f"  • {aff}" for aff in affirmations])
    return f"""
GUIDANCE PARA CAPÍTULO: PERMISSÃO
==================================

Afirmações centrais:
{affirmations_formatted}

O que incluir:
1. Dar permissão psicológica explícita ao leitor
2. Reforçar que o leitor merece ser feliz
3. Afirmar direito de buscar o melhor para si
4. Usar frases poderosas e empoderadoras
5. Encorajar crença no potencial de mudança
6. Criar espaço psicológico seguro para transformação

Tom: Empoderador, afetuoso, encorajador
Estrutura: Reconhecimento → Direitos do leitor → Encorajamento → Chamado à ação
Comprimento: 800-1200 palavras
"""

def get_power_chapter_guidance(celebration_elements: Dict[str, str]) -> str:
    """
    Retorna guidance para capítulo final de potência/celebração.
    
    Args:
        celebration_elements: Elementos a celebrar e reforçar
    
    Returns:
        str: Guidance estruturado para o agente
    """
    elements_formatted = "\n".join([f"  {k}: {v}" for k, v in celebration_elements.items()])
    return f"""
GUIDANCE PARA CAPÍTULO: POTÊNCIA
=================================

Elementos a celebrar:
{elements_formatted}

O que incluir:
1. Celebrar o progresso e aprendizados alcançados
2. Reforçar que o leitor está no caminho certo
3. Usar linguagem poderosa e energizante
4. Encorajar ação imediata e aplicação prática
5. Deixar leitor com sentimento de empoderamento
6. Inspirar determinação para jornada contínua
7. Oferecer visão de futuro transformado

Tom: Celebratório, energético, inspirador
Estrutura: Reconhecimento → Celebração → Visão → Chamado à ação
Comprimento: 900-1300 palavras
"""

def get_all_guidance_functions() -> dict:
    """
    Retorna dicionário com todas as funções de guidance disponíveis.
    
    Returns:
        dict: Mapa de nome da seção para função de guidance
    """
    return {
        "introduction": get_introduction_guidance,
        "problem": get_problem_chapter_guidance,
        "identification": get_identification_chapter_guidance,
        "solution": get_solution_chapter_guidance,
        "protection": get_protection_chapter_guidance,
        "permission": get_permission_chapter_guidance,
        "power": get_power_chapter_guidance
    }