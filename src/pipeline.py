"""
Pipeline de geração de ebook usando LangChain 1.0+.

Padrão LangChain 1.0:
- Carrega BRD do YAML
- Gera estrutura de capítulos via agent
- Faz deep research de cada capítulo
- Salva research em kb/ como .md
- Gera conteúdo final baseado no research
- Salva resultado final em result/
- Upload para Supabase (future)
"""

import time
import yaml
import json
import os
import sys
import ast
import shutil
import json_repair
from functools import lru_cache
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

if __name__ == "__main__" and (__package__ is None or __package__ == ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

from .agents import (
    create_chapter_agent,
    create_critical_reading_coordinator_agent,
    create_deep_research_agent,
    create_document_spec_agent,
    create_editing_agent,
    create_finalization_agent,
    create_ideation_agent,
    create_publication_agent,
    create_review_coordinator_agent,
    create_structure_agent,
    create_title_agent,
    create_technical_reviewer_agent,
    create_curious_beginner_agent,
    execute_agent,
    execute_review_personas,
    research_agent,
    thematic_research_agent,
    writer_agent,
)
from .config import (
    get_config,
    get_message,
    get_model,
    get_research_model,
    print_error_panel,
    print_pipeline_complete,
    print_pipeline_start,
    print_stage_complete,
    print_stage_header,
)
from .ui import (
    print_header, print_ebook_info, print_chapters_preview,
    get_confirmation, print_phase_header, print_research_start,
    print_research_saved, print_content_generation_start,
    print_content_generated, print_success_message, print_error_message,
    print_completion_summary, print_separator, print_info
)

# Import get_confirmation from ui explicitly to avoid circular import issues if any
from .ui import get_confirmation

def load_brd():
    """Carrega BRD do arquivo specs/brd.yaml."""
    brd_path = Path(__file__).parent.parent / "specs" / "brd.yaml"
    with open(brd_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_writing_style(brd):
    """
    Carrega o estilo de escrita do arquivo referenciado no BRD.
    
    Args:
        brd: Configuração BRD
    
    Returns:
        dict: Estilo de escrita com as chaves esperadas
    """
    writing_style_config = brd.get("writing_style", {})
    
    if isinstance(writing_style_config, dict) and "file" in writing_style_config:
        # Carregar do arquivo
        style_file = Path(__file__).parent.parent / writing_style_config["file"]
        if style_file.exists():
            with open(style_file, "r", encoding="utf-8") as f:
                content = f.read()
            # Parse markdown para extrair informações estruturadas
            # Por enquanto, retorna formato que o código espera
            return {
                "file_path": str(style_file),
                "content": content,
                "tone": "Técnico, inspirador e responsável",
                "approach": "Prático e educativo",
                "inspiration": ["LangChain", "Saúde Clínica", "Ética em IA"],
                "characteristics": [
                    "Técnico e acessível",
                    "Exemplos práticos de código",
                    "Foco em compliance LGPD",
                    "Ético e responsável",
                    "Balanceado entre teoria e prática"
                ]
            }
    
    # Fallback: retorna dict padrão se não encontrar arquivo
    return {
        "tone": "Técnico",
        "approach": "Prático",
        "inspiration": ["LangChain"],
        "characteristics": [
            "Técnico",
            "Prático",
            "Ético"
        ]
    }


def count_words(text: str) -> int:
    """Retorna contagem aproximada de palavras para texto Markdown."""
    if not text:
        return 0
    return len(str(text).split())


@lru_cache(maxsize=1)
def get_deep_research_config_cached():
    """Carrega configuração deep_research com cache simples."""
    return get_config("deep_research") or {}


def get_deep_research_requirement(doc_type: str, field: str, default: int = 0):
    """Obtém requisito específico (ex: mínimo de palavras) para o tipo de pesquisa."""
    config = get_deep_research_config_cached()
    requirements = config.get("requirements", {})
    doc_requirements = requirements.get(doc_type, {})
    return doc_requirements.get(field, default)


def should_include_word_count_in_header() -> bool:
    """Informa se cabeçalho dos arquivos deve mostrar contagem de palavras."""
    config = get_deep_research_config_cached()
    return bool(config.get("include_word_count_in_header"))


def build_deep_research_prompt(topic: str, project: dict, minimum_words: int) -> str:
    """Monta prompt parametrizado definido no config.yaml."""
    config = get_deep_research_config_cached()
    template = (config.get("prompt_template") or "").strip()
    if not template:
        return ""

    required_topics = project.get("required_topics", [])
    required_topics_block = "\n".join(
        f"- {topic_name}" for topic_name in required_topics
    ) if required_topics else "- (Nenhum tópico obrigatório definido)"

    return template.format(
        topic=topic,
        ebook_name=project.get("name", ""),
        ebook_description=project.get("description", ""),
        target_audience=project.get("target_audience", ""),
        required_topics_list=required_topics_block,
        minimum_words=minimum_words,
    )

def check_existing_thematic_research(brd):
    """
    Verifica se pesquisas temáticas já existem em kb/.
    
    Returns:
        dict: {topic_name: file_path} dos arquivos existentes
    """
    kb_dir = Path(__file__).parent.parent / "kb"
    required_topics = brd["project"].get("required_topics", [])
    
    existing = {}
    for topic in required_topics:
        safe_name = topic.lower().replace(" ", "_").replace("(", "").replace(")", "")
        file_path = kb_dir / f"thematic_{safe_name}.md"
        if file_path.exists():
            existing[topic] = str(file_path)
    
    return existing

def ask_perform_thematic_research(existing_count, total_count):
    """
    Pergunta se deve realizar pesquisa temática.
    
    Args:
        existing_count: Número de pesquisas temáticas já existentes
        total_count: Total de pesquisas temáticas necessárias
    
    Returns:
        bool: True se deve fazer a pesquisa, False caso contrário
    """
    if existing_count > 0:
        print(f"\n⚠️  Encontradas {existing_count}/{total_count} pesquisas temáticas já salvas em kb/\n")
        print("Opções:")
        print("  [s] Sim, fazer nova pesquisa (sobrescrever existentes)")
        print("  [n] Não, usar pesquisas existentes")
        
        while True:
            choice = input("\nDeseja fazer a pesquisa temática? (s/n): ").strip().lower()
            if choice in ['s', 'n']:
                return choice == 's'
            print("Resposta inválida. Digite 's' ou 'n'")
    
    return True

def ask_rag_storage_method():
    """
    Pergunta onde o RAG deve ser armazenado.
    
    Returns:
        str: 'supabase' ou 'local'
    """
    print("\n🗂️  Onde armazenar o RAG (contexto de pesquisa)?\n")
    print("Opções:")
    print("  [s] Supabase (recomendado para produção, requer credenciais)")
    print("  [l] Local (pasta kb/, sem dependências externas)")
    
    while True:
        choice = input("\nEscolha o armazenamento: (s/l): ").strip().lower()
        if choice == 's':
            return 'supabase'
        elif choice == 'l':
            return 'local'
        print("Resposta inválida. Digite 's' ou 'l'")

def initialize_ebook_file(brd, output_file="result/ebook.md"):
    """Cria o arquivo ebook.md inicial usando o template."""
    import os
    import datetime

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    
    template_path = Path(__file__).parent.parent / "template" / "template.md"
    template_content = ""
    
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
    else:
        # Fallback template if file missing
        template_content = "# <<titulo_do_livro>>\n\n[Capitulos]"

    # Substitui placeholders iniciais
    final_content = template_content.replace("<<titulo_do_livro>>", brd['project']['name'])
    final_content = final_content.replace("<<data de lançamento>>", datetime.date.today().strftime("%d/%m/%Y"))
    final_content = final_content.replace("<<numero do ASIN>>", "PENDENTE")
    final_content = final_content.replace("<<link da amazon>>", "https://amazon.com.br/dp/PENDENTE")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print(f"  📄 Arquivo inicial criado: {output_file}")
    return output_file

def generate_introduction(brd, chapters, test_mode=False):
    """
    Gera o capítulo de introdução do ebook.
    
    Args:
        brd: Configuração BRD
        chapters: Lista de capítulos gerados
        test_mode: Se True, retorna conteúdo mockado
    
    Returns:
        str: Conteúdo da introdução em Markdown
    """
    if test_mode:
        return "# Introdução\n\nEsta é uma introdução mockada para teste do pipeline."
    
    project = brd["project"]
    writing_style = load_writing_style(brd)
    
    # Lista os capítulos para contextualizar
    chapters_list = "\n".join([f"- {ch['name']}: {ch['purpose']}" for ch in chapters])
    
    intro_prompt = f"""Escreva uma INTRODUÇÃO envolvente e informativa para o ebook "{project['name']}".

DESCRIÇÃO DO EBOOK:
{project['description']}

PÚBLICO-ALVO:
{project['target_audience']}

CAPÍTULOS DO EBOOK:
{chapters_list}

TÓPICOS OBRIGATÓRIOS A ABORDAR:
{chr(10).join(f"- {topic}" for topic in project.get('required_topics', []))}

ESTILO DE ESCRITA:
- Tom: {writing_style['tone']}
- Abordagem: {writing_style['approach']}

INSTRUÇÕES:
1. Comece explicando o CONTEXTO e a RELEVÂNCIA do tema no cenário atual
2. Apresente o PROBLEMA ou DESAFIO que o ebook aborda
3. Explique O QUE o leitor vai APRENDER e como isso vai TRANSFORMÁ-LO
4. Dê uma VISÃO GERAL dos capítulos (sem entrar em detalhes)
5. Termine com uma CHAMADA À AÇÃO motivadora

EXTENSÃO: Aproximadamente 800-1200 palavras.
FORMATO: Markdown puro, sem título de seção (o título "Introdução" já estará no template).
TOM: Inspirador, técnico mas acessível, prático.

**IMPORTANTE - FORMATO DE SAÍDA:**
- Retorne APENAS o conteúdo da introdução em Markdown puro
- NÃO retorne JSON, NÃO retorne listas, NÃO retorne objetos
- NÃO inclua o título "Introdução" (ele já será adicionado automaticamente)
- Comece diretamente com o conteúdo
- Use formatação Markdown: ##, ###, **negrito**, *itálico*, listas, etc.

Retorne APENAS o conteúdo da introdução em Markdown."""
    
    from .agents import writer_agent
    
    response = writer_agent.invoke({
        "messages": [{"role": "user", "content": intro_prompt}]
    })
    
    # Extrai conteúdo
    messages = response.get("messages", [])
    if messages and isinstance(messages, list) and len(messages) > 0:
        last_msg = messages[-1]
        if hasattr(last_msg, 'content'):
            content = last_msg.content
        elif isinstance(last_msg, dict):
            content = last_msg.get("content", str(last_msg))
        else:
            content = str(last_msg)
    else:
        content = str(response)
    
    # Se o conteúdo for uma lista JSON, extrai o texto
    if isinstance(content, str) and content.strip().startswith('['):
        try:
            content_list = json.loads(content)
            if isinstance(content_list, list) and len(content_list) > 0:
                if isinstance(content_list[0], dict):
                    content = content_list[0].get('text', content)
                elif isinstance(content_list[0], str):
                    content = content_list[0]
        except:
            pass
    
    return content if isinstance(content, str) else str(content)

def generate_conclusion(brd, chapters, test_mode=False):
    """
    Gera o capítulo de conclusão/palavras finais do ebook.
    
    Args:
        brd: Configuração BRD
        chapters: Lista de capítulos gerados
        test_mode: Se True, retorna conteúdo mockado
    
    Returns:
        str: Conteúdo da conclusão em Markdown
    """
    if test_mode:
        return "# Palavras Finais\n\nEsta é uma conclusão mockada para teste do pipeline."
    
    project = brd["project"]
    writing_style = load_writing_style(brd)
    
    # Lista os capítulos para contextualizar
    chapters_list = "\n".join([f"- {ch['name']}" for ch in chapters])
    
    conclusion_prompt = f"""Escreva PALAVRAS FINAIS inspiradoras e motivadoras para o ebook "{project['name']}".

DESCRIÇÃO DO EBOOK:
{project['description']}

PÚBLICO-ALVO:
{project['target_audience']}

CAPÍTULOS ABORDADOS:
{chapters_list}

TÓPICOS PRINCIPAIS:
{chr(10).join(f"- {topic}" for topic in project.get('required_topics', []))}

ESTILO DE ESCRITA:
- Tom: {writing_style['tone']}
- Abordagem: {writing_style['approach']}

INSTRUÇÕES:
1. Faça uma RECAPITULAÇÃO dos principais aprendizados (sem repetir conteúdo)
2. Reforce a TRANSFORMAÇÃO que o leitor alcançou ao completar o ebook
3. Dê PRÓXIMOS PASSOS práticos e acionáveis
4. INSPIRE o leitor a aplicar o conhecimento adquirido
5. Termine com uma mensagem MOTIVADORA e EMPOLGANTE sobre o futuro

EXTENSÃO: Aproximadamente 600-800 palavras.
FORMATO: Markdown puro, sem título de seção (o título "Palavras Finais" já estará no template).
TOM: Inspirador, empoderador, prático, otimista.

**IMPORTANTE - FORMATO DE SAÍDA:**
- Retorne APENAS o conteúdo das palavras finais em Markdown puro
- NÃO retorne JSON, NÃO retorne listas, NÃO retorne objetos
- NÃO inclua o título "Palavras Finais" (ele já será adicionado automaticamente)
- Comece diretamente com o conteúdo
- Use formatação Markdown: ##, ###, **negrito**, *itálico*, listas, etc.

Retorne APENAS o conteúdo das palavras finais em Markdown."""
    
    from .agents import writer_agent
    
    response = writer_agent.invoke({
        "messages": [{"role": "user", "content": conclusion_prompt}]
    })
    
    # Extrai conteúdo
    messages = response.get("messages", [])
    if messages and isinstance(messages, list) and len(messages) > 0:
        last_msg = messages[-1]
        if hasattr(last_msg, 'content'):
            content = last_msg.content
        elif isinstance(last_msg, dict):
            content = last_msg.get("content", str(last_msg))
        else:
            content = str(last_msg)
    else:
        content = str(response)
    
    # Se o conteúdo for uma lista JSON, extrai o texto
    if isinstance(content, str) and content.strip().startswith('['):
        try:
            content_list = json.loads(content)
            if isinstance(content_list, list) and len(content_list) > 0:
                if isinstance(content_list[0], dict):
                    content = content_list[0].get('text', content)
                elif isinstance(content_list[0], str):
                    content = content_list[0]
        except:
            pass
    
    return content if isinstance(content, str) else str(content)

def generate_glossary(ebook, test_mode=False):
    """
    Gera glossário baseado nos capítulos do ebook.
    
    Args:
        ebook: Dicionário com dados do ebook (incluindo chapters)
        test_mode: Se True, retorna conteúdo mockado
    
    Returns:
        str: Conteúdo do glossário em Markdown
    """
    if test_mode:
        return "# Glossário\n\nEste é um glossário mockado para teste do pipeline."
    
    # Extrai conteúdo de todos os capítulos
    all_chapters_content = "\n\n".join([
        f"## {ch['name']}\n{ch['content'][:2000]}..." 
        for ch in ebook.get("chapters", [])
    ])
    
    glossary_prompt = f"""Crie um GLOSSÁRIO COMPLETO E ORGANIZADO para o ebook "{ebook.get('title', '')}".

INSTRUÇÕES:
1. Analise o conteúdo dos capítulos abaixo
2. Identifique TODOS os termos técnicos, acrônimos e conceitos importantes
3. Para cada termo, forneça uma definição clara e concisa
4. Organize em ORDEM ALFABÉTICA
5. Use o formato: **Termo**: Definição.

CONTEÚDO DOS CAPÍTULOS (AMOSTRA):
{all_chapters_content[:5000]}

FORMATO DE SAÍDA:
- Markdown puro
    
    from .agents import writer_agent
    
    response = writer_agent.invoke({
        "messages": [{"role": "user", "content": glossary_prompt}]
    })
    
    # Extrai conteúdo
    messages = response.get("messages", [])
    if messages and isinstance(messages, list) and len(messages) > 0:
        last_msg = messages[-1]
        if hasattr(last_msg, 'content'):
            content = last_msg.content
        elif isinstance(last_msg, dict):
            content = last_msg.get("content", str(last_msg))
        else:
            content = str(last_msg)
    else:
        content = str(response)
    
    # Se o conteúdo for uma lista JSON, extrai o texto
    if isinstance(content, str) and content.strip().startswith('['):
        try:
            content_list = json.loads(content)
            if isinstance(content_list, list) and len(content_list) > 0:
                if isinstance(content_list[0], dict):
                    content = content_list[0].get('text', content)
                elif isinstance(content_list[0], str):
                    content = content_list[0]
        except:
            pass
    
    return content if isinstance(content, str) else str(content)

def generate_bibliography(ebook, test_mode=False):
    """
    Gera referências bibliográficas baseadas nos capítulos do ebook.
    
    Args:
        ebook: Dicionário com dados do ebook (incluindo chapters)
        test_mode: Se True, retorna conteúdo mockado
    
    Returns:
        str: Conteúdo das referências em Markdown
    """
    if test_mode:
        return "# Referências Bibliográficas\n\nEstas são referências mockadas para teste do pipeline."
    
    # Extrai conteúdo de todos os capítulos
    all_chapters_content = "\n\n".join([
        f"## {ch['name']}\n{ch['content'][:2000]}..." 
        for ch in ebook.get("chapters", [])
    ])
    
    bibliography_prompt = f"""Crie uma seção de REFERÊNCIAS BIBLIOGRÁFICAS para o ebook "{ebook.get('title', '')}".

INSTRUÇÕES:
1. Analise o conteúdo dos capítulos abaixo
2. Identifique TODAS as fontes, frameworks, documentações e referências mencionadas
3. Organize as referências em categorias:
   - Documentação Oficial
   - Artigos e Papers
   - Livros
   - Recursos Online
4. Use formato de citação acadêmico quando aplicável
5. Inclua URLs quando disponíveis

CONTEÚDO DOS CAPÍTULOS (AMOSTRA):
{all_chapters_content[:5000]}

FORMATO DE SAÍDA:
- Markdown puro
- Sem título de seção (já estará no template)
- Organizado por categorias
- Formato de lista numerada ou bullets
- Inclua URLs quando possível

**IMPORTANTE - FORMATO DE SAÍDA:**
- Retorne APENAS as referências em Markdown puro
- NÃO retorne JSON, NÃO retorne listas Python, NÃO retorne objetos
- Use formatação Markdown com ## para categorias e listas numeradas

EXEMPLO:

## Documentação Oficial
1. LangChain Documentation. Disponível em: https://python.langchain.com/
2. Google Gemini API Reference. Disponível em: https://ai.google.dev/

## Artigos e Papers
1. Smith, J. et al. (2024). "Retrieval-Augmented Generation in Healthcare". Journal of AI Medicine.

Retorne APENAS as referências em Markdown."""
    
    from .agents import writer_agent
    
    response = writer_agent.invoke({
        "messages": [{"role": "user", "content": bibliography_prompt}]
    })
    
    # Extrai conteúdo
    messages = response.get("messages", [])
    if messages and isinstance(messages, list) and len(messages) > 0:
        last_msg = messages[-1]
        if hasattr(last_msg, 'content'):
            content = last_msg.content
        elif isinstance(last_msg, dict):
            content = last_msg.get("content", str(last_msg))
        else:
            content = str(last_msg)
    else:
        content = str(response)
    
    # Se o conteúdo for uma lista JSON, extrai o texto
    if isinstance(content, str) and content.strip().startswith('['):
        try:
            content_list = json.loads(content)
            if isinstance(content_list, list) and len(content_list) > 0:
                if isinstance(content_list[0], dict):
                    content = content_list[0].get('text', content)
                elif isinstance(content_list[0], str):
                    content = content_list[0]
        except:
            pass
    
    return content if isinstance(content, str) else str(content)

def validate_template_placeholders(output_file="result/ebook.md"):
    """
    Valida se todos os placeholders do template foram preenchidos.
    
    Returns:
        tuple: (bool, list) - (is_valid, list_of_unfilled_placeholders)
    """
    import re
    
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Procura por placeholders no formato <<PLACEHOLDER_NAME>>
    placeholders = re.findall(r'<<([A-Z_]+)>>', content)
    
    # Retorna todos os placeholders encontrados como não preenchidos
    unfilled = list(set(placeholders))  # Remove duplicatas
    
    return len(unfilled) == 0, unfilled


def generate_chapter_structure(brd):
    """
    Gera a estrutura de capítulos usando o writer_agent.
    
    Returns:
        list: Lista de dicts com {name, purpose, elements}
    """
    writing_style = load_writing_style(brd)
    project = brd["project"]
    content_cfg = brd["content_structure"]
    
    # Parâmetros dinâmicos do project
    number_chapters = project.get("number_chapters", 7)
    print(f"DEBUG: number_chapters from BRD = {number_chapters}") # Debug print
    target_word_count = project.get("target_word_count", 10000)
    required_topics = project.get("required_topics", [])
    main_use_case = project.get("main_use_case", {})
    
    # Prepara o prompt de estrutura substituindo placeholders
    structure_prompt_cfg = content_cfg.get('structure_prompt', '')
    structure_prompt_cfg = structure_prompt_cfg.replace('<num_chapters>', str(number_chapters))
    structure_prompt_cfg = structure_prompt_cfg.replace('<target_word_count>', str(target_word_count))
    structure_prompt_cfg = structure_prompt_cfg.replace('<chapter_structure>', str(content_cfg.get('chapter_structure', '')))

    topics_list = "\n".join(f"  - {topic}" for topic in required_topics) if required_topics else ""
    use_case_desc = main_use_case.get("description", "") if main_use_case else ""
    use_case_features = "\n".join(f"  • {feat}" for feat in main_use_case.get("features", [])) if main_use_case else ""
    
    query = f"""Para o ebook "{project['name']}", crie uma estrutura de {number_chapters} capítulos, cada um com nome, propósito e elementos obrigatórios a incluir.

REQUISITOS:
- Total de aproximadamente {target_word_count} palavras distribuídas nos {number_chapters} capítulos
- Cada capítulo deve ter aproximadamente {target_word_count // number_chapters} palavras
- {structure_prompt_cfg}

TÓPICOS OBRIGATÓRIOS que devem ser cobertos:
{topics_list}

CASO DE USO PRINCIPAL:
{use_case_desc}

Funcionalidades principais do caso de uso:
{use_case_features}

Tom e estilo esperado:
- Tone: {writing_style['tone']}
- Abordagem: {writing_style['approach']}
- Características: {', '.join(writing_style['characteristics'])}

Público-alvo: {project['target_audience']}

Retorne APENAS um JSON array com {number_chapters} objetos, cada um com as chaves: "name" (string), "purpose" (string), "elements" (array de strings).
Os elementos devem cobrir os tópicos obrigatórios de forma distribuída entre os capítulos.
Exemplo formato:
[{{"name": "Introdução", "purpose": "...", "elements": ["elem1", "elem2"]}}, ...]"""
    
    print(f"\n🔄 Gerando estrutura de {number_chapters} capítulos com tópicos obrigatórios ({target_word_count} palavras)...")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"  ⚠️ Tentativa {attempt + 1}/{max_retries} de gerar estrutura...")
                
            response = writer_agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })
            
            content = response["messages"][-1].content
            
            # Se for lista com artifacts (Gemini format), extrai o texto
            if isinstance(content, list) and len(content) > 0:
                if isinstance(content[0], dict) and 'text' in content[0]:
                    # Extrai o texto do primeiro artifact
                    content = content[0]['text']
            
            # Se for string, tenta extrair JSON
            if isinstance(content, str):
                # Se começar com `, procura pelo JSON dentro
                if '```json' in content:
                    start = content.find('[')
                    end = content.rfind(']') + 1
                    if start >= 0 and end > start:
                        content = content[start:end]
                elif '```' in content: # Tenta achar qualquer bloco de código
                     start = content.find('[')
                     end = content.rfind(']') + 1
                     if start >= 0 and end > start:
                        content = content[start:end]

                # Limpeza básica
                content = content.strip()
                if content.startswith('```json'): content = content[7:]
                if content.endswith('```'): content = content[:-3]
                content = content.strip()
                
                # Tenta parsear com json_repair (mais robusto)
                try:
                    chapters = json_repair.loads(content)
                    if isinstance(chapters, list):
                        return chapters
                except Exception as e:
                    print(f"  ❌ Erro ao parsear JSON com json_repair (tentativa {attempt + 1}): {e}")
                    print(f"  📄 Conteúdo problemático (início): {content[:200]}...")
                    
                # Fallback antigo (apenas se json_repair falhar ou não retornar lista)
                if content.startswith('['):
                    try:
                        chapters = json.loads(content)
                        return chapters
                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"  ❌ Erro ao parsear JSON nativo (tentativa {attempt + 1}): {e}")
                        
                        # Tenta ast.literal_eval como último recurso
                        try:
                            chapters = ast.literal_eval(content)
                            if isinstance(chapters, list):
                                return chapters
                        except Exception as ast_e:
                            print(f"  ❌ Erro no fallback AST: {ast_e}")
                            pass
        except Exception as e:
            print(f"  ❌ Erro na execução do agente (tentativa {attempt + 1}): {e}")
            
    print("❌ Não foi possível gerar estrutura de capítulos após várias tentativas")
    return []

def generate_chapter_research(chapter_name, chapter_purpose, chapter_elements, brd, skip_prompt=False):
    """Conduz pesquisa profunda sobre um capítulo usando research_agent."""
    
    # Check if we should skip research based on user preference
    from .ui import get_confirmation
    
    if not skip_prompt:
        print(f"\n  🔍 Preparando pesquisa para: {chapter_name}")
        should_research = get_confirmation(
            f"Deseja realizar pesquisa profunda (Deep Research) para o capítulo '{chapter_name}'?",
            default=True,
            phase="deep_research"
        )
        
        if not should_research:
            print(f"  ⏩ Pulando pesquisa para '{chapter_name}'. Usando apenas conhecimento interno e contexto existente.")
            return f"# Pesquisa ignorada para {chapter_name}\n\nO usuário optou por pular a etapa de pesquisa profunda para este capítulo.", 0

    project = brd["project"]
    min_words = get_deep_research_requirement("chapter", "minimum_word_count", 2000)
    min_sources = get_deep_research_requirement("chapter", "minimum_sources", 5)

    base_prompt = build_deep_research_prompt(
        topic=f"{chapter_name} (capítulo do ebook {project.get('name', '')})",
        project=project,
        minimum_words=min_words,
    )

    elements_md = "\n".join(
        f"- {elem}" for elem in (chapter_elements or [])
    ) or "- (Sem elementos adicionais definidos)"

    chapter_specific_instructions = f"""# 🧩 Diretrizes Específicas do Capítulo
- Nome do capítulo: {chapter_name}
- Propósito central: {chapter_purpose}
- Elementos mandatórios que precisam aparecer na narrativa:
{elements_md}

## 🧭 Escopo e Conexões
- Garanta alinhamento explícito com os tópicos obrigatórios do BRD listados acima.
- Adapte a análise para profissionais técnicos atuando em saúde/neurologia.
- Quando aplicável, inclua fluxos de implementação com LangChain, agentes e integrações clínicas.

## 📚 Fontes e Confiabilidade
- Cite pelo menos {min_sources} fontes confiáveis ao final do documento.
- Priorize documentação oficial, regulações governamentais, padrões industriais e papers revisados por pares.
- Para cada referência inclua URL/DOI e data de acesso.

## 🧮 Quantidade e Cabeçalho
- Gere no mínimo {min_words} palavras de conteúdo substancial.
- Informe a contagem aproximada de palavras logo após o título do documento.

## ✅ Checklist Obrigatório
- Estruture o texto seguindo as seções do template principal (Resumo Executivo -> Introdução -> Corpo Técnico -> Desafios -> Tendências).
- Cada parágrafo deve conter apenas uma ideia e pode ser convertido em chunk RAG sem perda de contexto.
- Destaque riscos de segurança de dados clínicos, implicações éticas e comparações com abordagens alternativas.
- Inclua exemplos de código Python/LangChain quando o capítulo abordar tecnologias, frameworks ou agentes."""

    query_blocks = [base_prompt.strip(), chapter_specific_instructions.strip()]
    query = "\n\n".join(block for block in query_blocks if block).strip()

    print(f"  🔍 Pesquisando: {chapter_name}...")
    response = research_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    content = response["messages"][-1].content

    # Se for lista com artifacts (Gemini format), extrai o texto
    if isinstance(content, list) and len(content) > 0:
        if isinstance(content[0], dict) and 'text' in content[0]:
            content = content[0]['text']

    research_content = content if isinstance(content, str) else str(content)
    word_count = count_words(research_content)

    if word_count < min_words:
        print(f"    ⚠️ Conteúdo de '{chapter_name}' possui {word_count} palavras (mínimo recomendado: {min_words}).")

    return research_content, word_count

def save_thematic_research_immediately(topic, content, brd, word_count=None):
    """
    Salva pesquisa temática em kb/ imediatamente após geração.

    Args:
        topic: Nome do tópico
        content: Conteúdo da pesquisa
        brd: Configuração BRD
        word_count: Contagem de palavras já calculada (opcional)

    Returns:
        str: Caminho do arquivo salvo
    """
    kb_dir = Path(__file__).parent.parent / "kb"
    kb_dir.mkdir(exist_ok=True)

    actual_word_count = word_count if word_count is not None else count_words(content)
    include_word_count = should_include_word_count_in_header()

    # Normaliza nome do arquivo
    safe_name = topic.lower().replace(" ", "_").replace("(", "").replace(")", "")
    file_path = kb_dir / f"thematic_{safe_name}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Pesquisa Temática: {topic}\n\n")
        f.write(f"Ebook: {brd['project']['name']}\n")
        f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Tipo: Pesquisa Temática Abrangente\n\n")
        if include_word_count:
            f.write(f"Palavras: {actual_word_count}\n\n")
        f.write("---\n\n")
        f.write(content)

    return str(file_path)

def generate_thematic_research(brd, progress=None):
    """Gera pesquisas temáticas abrangentes baseadas nos required_topics do BRD."""

    project = brd["project"]
    required_topics = project.get("required_topics", [])
    config = get_deep_research_config_cached()
    thematic_cfg = config.get("thematic_research", {})

    min_words = get_deep_research_requirement("thematic", "minimum_word_count", 3000)
    min_sources = get_deep_research_requirement("thematic", "minimum_sources", 7)

    if not required_topics:
        print("⚠️ Nenhum tópico obrigatório encontrado no BRD")
        return {}

    thematic_research_paths = {}
    print(f"\n📚 Gerando pesquisas temáticas abrangentes para {len(required_topics)} tópicos...\n")
    print("   (Salvamento imediato ativado - cada tema é persistido em kb/ após geração)\n")

    # Configura o gerenciador de progresso
    if progress is None:
        progress_ctx = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        )
        progress_ctx.start()
    else:
        progress_ctx = progress

    try:
        task = progress_ctx.add_task("[cyan]Pesquisando temas...", total=len(required_topics))

        for idx, topic in enumerate(required_topics, 1):
            progress_ctx.update(task, description=f"[cyan]Pesquisando tema ({idx}/{len(required_topics)}): {topic}")

            base_prompt = build_deep_research_prompt(topic=topic, project=project, minimum_words=min_words)

            thematic_instructions = f"""# 🔬 Diretrizes Complementares para Temas Obrigatórios
- Esta pesquisa é independente de capítulos e servirá como fonte canônica reutilizável.
- Gere no mínimo {min_words} palavras em formato Markdown altamente estruturado.
- Cite pelo menos {min_sources} fontes confiáveis priorizando documentação oficial, órgãos reguladores e papers revisados por pares.
- Indique a contagem aproximada de palavras logo após o título do documento.
- Inclua glossário técnico, tabelas comparativas, diagramas textuais e exemplos de código Python/LangChain sempre que o tema for tecnológico.
- Trate riscos, limitações, trade-offs, métricas de performance e implicações éticas especificamente para saúde.
"""

            optional_blocks = []
            for field in ("technical_depth_description", "technical_guidelines", "code_examples_requirement"):
                block = thematic_cfg.get(field)
                if block:
                    optional_blocks.append(block.strip())

            query_blocks = [base_prompt.strip(), thematic_instructions.strip()] + optional_blocks
            query = "\n\n".join(block for block in query_blocks if block).strip()

            response = thematic_research_agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })

            content = response["messages"][-1].content

            # Se for lista com artifacts (Gemini format), extrai o texto
            if isinstance(content, list) and len(content) > 0:
                if isinstance(content[0], dict) and 'text' in content[0]:
                    content = content[0]['text']

            research_content = content if isinstance(content, str) else str(content)
            word_count = count_words(research_content)

            if word_count < min_words:
                # print(f"    ⚠️ Conteúdo de '{topic}' possui {word_count} palavras (mínimo recomendado: {min_words}).")
                pass
            else:
                # print(f"    🧮 Contagem aproximada: {word_count} palavras.")
                pass

            # SALVAMENTO IMEDIATO após geração de cada tema
            file_path = save_thematic_research_immediately(topic, research_content, brd, word_count=word_count)
            thematic_research_paths[topic] = file_path
            # print(f"  📝 Salvo imediatamente: {Path(file_path).name}\n")
            
            progress_ctx.advance(task)

    finally:
        if progress is None:
            progress_ctx.stop()
        else:
            progress_ctx.remove_task(task)

    return thematic_research_paths

def save_research_to_kb(chapter_name, research_content, brd, word_count=None):
    """
    Salva research em kb/ como arquivo Markdown.

    Args:
        chapter_name: Nome do capítulo (usado para nome do arquivo)
        research_content: Conteúdo de research
        brd: Configuração BRD
        word_count: Contagem de palavras já calculada (opcional)

    Returns:
        str: Caminho do arquivo salvo
    """
    kb_dir = Path(__file__).parent.parent / "kb"
    kb_dir.mkdir(exist_ok=True)

    actual_word_count = word_count if word_count is not None else count_words(research_content)
    include_word_count = should_include_word_count_in_header()

    # Normaliza nome do arquivo
    safe_name = chapter_name.lower().replace(" ", "_").replace(":", "")
    file_path = kb_dir / f"research_{safe_name}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Research: {chapter_name}\n\n")
        f.write(f"Ebook: {brd['project']['name']}\n")
        f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("Tipo: Pesquisa por Capítulo\n")
        if include_word_count:
            f.write(f"Palavras: {actual_word_count}\n")
        f.write("\n")
        f.write("---\n\n")
        f.write(research_content)

    return str(file_path)

def build_chapter_queries_with_research(chapters, research_data, brd):
    """
    Constrói queries para cada capítulo com base no research realizado.
    
    Args:
        chapters: Lista de dicts com estrutura de capítulos
        research_data: Dict com research por capítulo {chapter_name: research_content}
        brd: Configuração BRD
    
    Returns:
        list: Lista de tuplas (chapter_name, query_text)
    """
    writing_style = load_writing_style(brd)
    project = brd["project"]
    
    # Calcula palavras por capítulo
    target_word_count = project.get("target_word_count", 10000)
    number_chapters = len(chapters)
    words_per_chapter = target_word_count // number_chapters
    
    queries = []
    for idx, chapter in enumerate(chapters, 1):
        research_context = research_data.get(chapter['name'], "")
        
        # Detecta se a pesquisa foi pulada
        skipped_research = research_context.startswith("# Pesquisa ignorada")
NÃO invente fatos técnicos. Use as ferramentas para embasar o conteúdo."""
        else:
            context_instruction = f"""CONTEXTO DE RESEARCH (use como base):
{research_context[:3000]}..."""

        query = f"""Gere o capítulo {idx}/{number_chapters} "{chapter['name']}" do ebook: {project['name']}

REQUISITOS:
- Aproximadamente {words_per_chapter} palavras
- Este é o capítulo {idx} de {number_chapters}

{context_instruction}

Propósito do capítulo:
{chapter['purpose']}

Elementos obrigatórios a incluir:
{chr(10).join(f"• {elem}" for elem in chapter['elements'])}

Tom e estilo:
- Tom: {writing_style['tone']}
- Abordagem: {writing_style['approach']}
- Inspirações literárias: {', '.join(writing_style['inspiration'])}

Características do estilo de escrita:
{chr(10).join(f"✓ {char}" for char in writing_style['characteristics'])}

Público-alvo: {project['target_audience']}
Idioma: {project['language']}

**IMPORTANTE - FORMATO DE SAÍDA:**
- Retorne APENAS o conteúdo do capítulo em Markdown puro
- NÃO retorne JSON, NÃO retorne listas, NÃO retorne objetos
- NÃO inclua o título do capítulo (ele já será adicionado automaticamente)
- Comece diretamente com o conteúdo do capítulo
- Use formatação Markdown: ##, ###, **negrito**, *itálico*, listas, código, etc.
- O conteúdo deve ter aproximadamente {words_per_chapter} palavras

Escreva o conteúdo em Markdown puro. Foco em prático, educativo e ético."""
        
        queries.append((chapter["name"], query))
    
    return queries


def _build_review_persona_agents(model):
    """
    Constrói agentes revisores especializados para feedback técnico.
    
    Returns:
        dict: Dicionário com agentes revisores por persona
    """
    from .agents import create_technical_reviewer_agent
    
    # Por enquanto, retorna apenas o technical reviewer
    # Pode ser expandido com mais personas
    return {
        "technical_reviewer": create_technical_reviewer_agent(model)
    }


def _build_virtual_reader_agents(model):
    """
    Constrói agentes leitores virtuais para feedback de UX/clareza.
    
    Returns:
        dict: Dicionário com agentes leitores por persona
    """
    from .agents import create_curious_beginner_agent
    
    # Por enquanto, retorna apenas o curious beginner
    # Pode ser expandido com mais personas
    return {
        "curious_beginner": create_curious_beginner_agent(model)
    }


def execute_review_personas(content, personas):
    """
    Executa um conjunto de personas e coleta feedback.
    
    Args:
        content: Conteúdo a revisar
        personas: Dict de agentes {persona_name: agent}
    
    Returns:
        dict: Feedback consolidado {persona_name: feedback}
    """
    from .agents import execute_agent
    
    feedback = {}
    for persona_name, persona_agent in personas.items():
        prompt = f"[{persona_name}] Revise e forneça feedback especializado:\n\n{content}"
        feedback[persona_name] = execute_agent(persona_agent, prompt)
    return feedback


def generate_ebook(test_mode: bool = False):
    """Gera o ebook executando agente para estrutura e depois para cada capítulo."""
    brd = load_brd()
    
    # Header
    print_header(
        "📚 Gerador de Ebook Técnico",
        "LangChain 1.0 na Saúde Clínica"
    )
    
    # Inicializa barra de progresso global
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
    ) as global_progress:
        
        # Define etapas principais
        total_stages = 5 # Estrutura, Temática, Deep Research, Conteúdo, Revisão
        overall_task = global_progress.add_task("[bold blue]Progresso Total do Ebook", total=total_stages)
        
        # Etapa 1: Gerar estrutura
        print_info("Gerando estrutura de capítulos...")
        struct_task = global_progress.add_task("[cyan]Gerando estrutura...", total=None)
        if test_mode:
            print_info("🧪 MODO TESTE ATIVADO: Gerando estrutura de 10 capítulos mockados.")
            chapters = [
                {"name": "Capítulo 1: Introdução à IA na Saúde", "purpose": "Contextualizar o papel da IA em ambientes clínicos modernos", "elements": ["Fundamentos de IA", "Aplicações em saúde", "Desafios iniciais"]},
                {"name": "Capítulo 2: Fundamentos do LangChain 1.0", "purpose": "Explorar os conceitos básicos e a arquitetura do LangChain", "elements": ["Agentes", "Ferramentas", "Prompts"]},
                {"name": "Capítulo 3: RAG para Dados Clínicos", "purpose": "Aprender a implementar Retrieval Augmented Generation em contexto clínico", "elements": ["Arquitetura RAG", "Vetorização de dados", "Similaridade semântica"]},
                {"name": "Capítulo 4: Memory em LangChain", "purpose": "Gerenciar contexto e memória em conversas com agentes", "elements": ["Buffer de memória", "Resumo de contexto", "Limpeza de histórico"]},
                {"name": "Capítulo 5: Compliance em Saúde", "purpose": "Garantir conformidade com regulamentações de saúde", "elements": ["LGPD", "Auditoria", "Rastreabilidade"]},
                {"name": "Capítulo 6: Ética em IA", "purpose": "Abordar questões éticas na implementação de IA clínica", "elements": ["Viés algorítmico", "Transparência", "Responsabilidade"]},
                {"name": "Capítulo 7: Arquitetura de Agentes RAG", "purpose": "Projetar e implementar arquiteturas robustas de agentes RAG", "elements": ["Design de agentes", "Integração de ferramentas", "Fluxo de decisão"]},
                {"name": "Capítulo 8: Registros Eletrônicos (EHRs)", "purpose": "Trabalhar com dados de registros eletrônicos de saúde", "elements": ["Estrutura de EHRs", "Privacidade de dados", "Integração com RAG"]},
                {"name": "Capítulo 9: UI com Chainlit", "purpose": "Criar interfaces de usuário intuitivas com Chainlit", "elements": ["Componentes Chainlit", "Fluxo de chat", "Personalização"]},
                {"name": "Capítulo 10: Implantação e Futuro", "purpose": "Estratégias de implantação e tendências futuras em IA clínica", "elements": ["Deploy em produção", "Monitoramento", "Roadmap futuro"]}
            ]
            brd["project"]["word_count_target"] = 10000
        else:
            chapters = generate_chapter_structure(brd)
            
        global_progress.remove_task(struct_task)
        global_progress.advance(overall_task)
        
        if not chapters:
            print_error_message("Falha ao gerar estrutura de capítulos")
            return None
        
        print_separator()
        
        # Etapa 2: Preparar dados do ebook
        ebook = {
            "title": brd["project"]["name"],
            "description": brd["project"]["description"],
            "chapters": []
        }
        
        # Exibir informações do ebook
        print_ebook_info(
            ebook['title'],
            ebook['description'],
            brd['project']['target_audience']
        )
        print_separator()
        
        # Exibir preview dos capítulos
        print_chapters_preview(chapters)
        print_separator()
        
        # Pedir aprovação
        global_progress.stop()
        try:
            if not test_mode and not get_confirmation("Deseja prosseguir com a geração do Ebook?"):
                return None
        finally:
            global_progress.start()
        
        # Inicializa arquivo do ebook imediatamente
        initialize_ebook_file(brd)
        
        # Gera introdução
        print_info("Gerando introdução do ebook...")
        intro_content = generate_introduction(brd, chapters, test_mode=test_mode)
        
        # Substitui placeholder <<INTRODUÇÃO>>
        with open("result/ebook.md", "r", encoding="utf-8") as f:
            ebook_content = f.read()
        ebook_content = ebook_content.replace("<<INTRODUÇÃO>>", intro_content)
        with open("result/ebook.md", "w", encoding="utf-8") as f:
            f.write(ebook_content)
        
        print_separator()
        
        # FASE 1: Deep Research de Todos os Capítulos e Salvamento
        print_phase_header(1, "DEEP RESEARCH DE TODOS OS CAPÍTULOS E SALVAMENTO", "Pesquisa profunda e salvamento em kb/")
        
        # Pergunta se deve realizar Deep Research
        global_progress.stop()
        try:
            if test_mode:
                perform_deep_research = True
            else:
                perform_deep_research = get_confirmation("Deseja realizar DEEP RESEARCH para TODOS os capítulos?", default=True)
        finally:
            global_progress.start()
        
        
        research_data = {}
        task = global_progress.add_task("[cyan]Processando pesquisa...", total=len(chapters))
        
        for idx, chapter in enumerate(chapters, 1):
            global_progress.update(task, description=f"[cyan]Pesquisando ({idx}/{len(chapters)}): {chapter['name']}")
            
            if perform_deep_research:
                if test_mode:
                    research_content = f"# Pesquisa Mockada para {chapter['name']}\n\nConteúdo de teste gerado automaticamente."
                    research_word_count = 100
                else:
                    # Gera research real
                    research_content, research_word_count = generate_chapter_research(
                        chapter['name'],
                        chapter['purpose'],
                        chapter['elements'],
                        brd,
                        skip_prompt=True # Novo parâmetro para pular o prompt individual
                    )
            else:
                # Pula research
                # print(f"  ⏩ Pulando pesquisa para '{chapter['name']}'. Usando apenas conhecimento interno e contexto existente.")
                research_content = f"# Pesquisa ignorada para {chapter['name']}\n\nO usuário optou por pular a etapa de pesquisa profunda para este capítulo."
                research_word_count = 0

            research_data[chapter['name']] = research_content

            # Salva em kb/
            kb_path = save_research_to_kb(
                chapter['name'], research_content, brd, word_count=research_word_count
            )
            # print_research_saved(kb_path, len(research_content))
            
            global_progress.advance(task)
            if idx < len(chapters):
                time.sleep(0.5)  # Pequeno delay entre requests
        
        global_progress.remove_task(task)
        global_progress.advance(overall_task)
        
        print_separator()
        print_success_message("Todas as pesquisas foram salvas em kb/")
        print_separator()
        
        # Pergunta sobre upload para Supabase
        if not test_mode and perform_deep_research:
            global_progress.stop()
            try:
                upload_to_supabase = get_confirmation("Deseja fazer upload e vetorizar no Supabase?", default=False)
                if upload_to_supabase:
                    print_info("📤 Upload para Supabase será implementado em breve.")
            finally:
                global_progress.start()
            print_separator()
        
        # FASE 2: Geração de conteúdo
        print_phase_header(2, "GERAÇÃO DE CONTEÚDO", "Geração de conteúdo final baseado em research")
        
        # Pergunta se deve gerar conteúdo
        global_progress.stop()
        try:
            if test_mode:
                perform_generation = True
            else:
                perform_generation = get_confirmation(
                    "Deseja prosseguir com a GERAÇÃO DE CONTEÚDO?",
                    default=True,
                    phase="content_generation"
                )
        finally:
            global_progress.start()
        
        if not perform_generation:
            print_info("Geração de conteúdo cancelada. Encerrando pipeline.")
            return None
        
        # Gerar queries para cada capítulo (agora com research como contexto)
        chapters_queries = build_chapter_queries_with_research(chapters, research_data, brd)
        
        words_per_chapter = brd['project'].get('target_word_count', 10000) // len(chapters)
        
        task = global_progress.add_task("[green]Gerando conteúdo...", total=len(chapters_queries))
        
        for idx, (chapter_name, query) in enumerate(chapters_queries, 1):
            global_progress.update(task, description=f"[green]Gerando ({idx}/{len(chapters_queries)}): {chapter_name}")
            
            # Executa agent com query
            if test_mode:
                response = {"messages": [{"content": f"# Conteúdo Mockado - {chapter_name}\n\nEste é um texto gerado em modo de teste para validar o fluxo."}]}
                time.sleep(0.1)
            else:
                response = writer_agent.invoke({
                    "messages": [{"role": "user", "content": query}]
                })
            
            # Extrai conteúdo com lógica melhorada para Gemini
            messages = response.get("messages", [])
            if messages and isinstance(messages, list) and len(messages) > 0:
                last_msg = messages[-1]
                # Verifica se é AIMessage (tem .content) ou dict
                if hasattr(last_msg, 'content'):
                    content = last_msg.content
                elif isinstance(last_msg, dict):
                    content = last_msg.get("content", str(last_msg))
                else:
                    content = str(last_msg)
            else:
                content = str(response)
            
            # Gemini às vezes retorna lista de dicts com 'text' key
            if isinstance(content, list) and len(content) > 0:
                if isinstance(content[0], dict) and 'text' in content[0]:
                    content = content[0]['text']
                elif isinstance(content[0], str):
                    content = content[0]
            
            # Se o conteúdo for uma string JSON, extrai o texto
            if isinstance(content, str) and content.strip().startswith('['):
                try:
                    content_list = json.loads(content)
                    if isinstance(content_list, list) and len(content_list) > 0:
                        if isinstance(content_list[0], dict) and 'text' in content_list[0]:
                            content = content_list[0]['text']
                        elif isinstance(content_list[0], str):
                            content = content_list[0]
                except (json.JSONDecodeError, ValueError):
                    # Se falhar o parse JSON, tenta ast.literal_eval
                    try:
                        content_list = ast.literal_eval(content)
                        if isinstance(content_list, list) and len(content_list) > 0:
                            if isinstance(content_list[0], dict) and 'text' in content_list[0]:
                                content = content_list[0]['text']
                            elif isinstance(content_list[0], str):
                                content = content_list[0]
                    except:
                        # Se tudo falhar, usa o conteúdo como está
                        pass
            
            # Garante que content é string
            if not isinstance(content, str):
                content = str(content)
            
            ebook["chapters"].append({
                "name": chapter_name,
                "content": content
            })
            
            # Salva incrementalmente se não for fazer revisão
            if not get_confirmation(
                "Deseja realizar a REVISÃO E REFINAMENTO?",
                default=True,
                skip_prompt=True,
                phase="review_refinement"
            ):
                 append_chapter_to_ebook(chapter_name, content)
            
            # print_content_generated(len(content))
            global_progress.advance(task)
            
            if idx < len(chapters_queries):
                time.sleep(0.5)
        
        global_progress.remove_task(task)
        global_progress.advance(overall_task)
        
        print_separator()
        
        # FASE 3: Revisão e Refinamento
        print_phase_header(3, "REVISÃO E REFINAMENTO", "Revisão técnica, leitura crítica e edição final")
        
        # Pergunta se deve realizar a revisão
        global_progress.stop()
        try:
            if test_mode:
                perform_review = True
            else:
                perform_review = get_confirmation(
                    "Deseja realizar a REVISÃO E REFINAMENTO?",
                    default=True,
                    phase="review_refinement"
                )
        finally:
            global_progress.start()
        
        if perform_review:
            write_model = get_model()
            research_model = get_research_model()
            
            # Inicializa agentes
            review_agent = create_review_coordinator_agent(research_model)
            review_personas = _build_review_persona_agents(research_model)
            
            critical_agent = create_critical_reading_coordinator_agent(research_model)
            virtual_readers = _build_virtual_reader_agents(write_model)
            
            editing_agent = create_editing_agent(write_model)
            
            task = global_progress.add_task("[magenta]Revisando e Editando...", total=len(ebook["chapters"]))
            
            for idx, chapter in enumerate(ebook["chapters"], 1):
                original_content = chapter["content"]

                # 1. Revisão Técnica
                global_progress.update(task, description=f"[magenta]Revisão Técnica ({idx}/{len(ebook['chapters'])}): {chapter['name']}")
                if test_mode:
                    review_results = {"Technical Reviewer": "Aprovado (Mock)"}
                else:
                    review_results = execute_review_personas(
                        original_content, review_personas
                    )
                review_text = "\n\n".join([f"### {k}\n{v}" for k, v in review_results.items()])
                
                # 2. Leitura Crítica
                global_progress.update(task, description=f"[magenta]Leitura Crítica ({idx}/{len(ebook['chapters'])}): {chapter['name']}")
                if test_mode:
                    critical_results = {"Curious Beginner": "Interessante (Mock)"}
                else:
                    critical_results = execute_review_personas(
                        original_content, virtual_readers
                    )
                critical_text = "\n\n".join([f"### {k}\n{v}" for k, v in critical_results.items()])
                
                # 3. Edição e Refinamento
                global_progress.update(task, description=f"[magenta]Editando ({idx}/{len(ebook['chapters'])}): {chapter['name']}")
                editing_prompt = f"""Refine o seguinte capítulo do ebook com base nos feedbacks recebidos.
                
CAPÍTULO: {chapter['name']}
CONTEÚDO ORIGINAL:
{original_content}

FEEDBACK TÉCNICO:
{review_text}

FEEDBACK LEITURA CRÍTICA:
{critical_text}

INSTRUÇÕES DE EDIÇÃO:
- Melhore a clareza e fluidez.
- Corrija imprecisões técnicas apontadas.
- Torne o texto mais acessível conforme sugerido pela leitura crítica.
- Mantenha o formato Markdown.
- Retorne APENAS o conteúdo refinado do capítulo.
"""
                if test_mode:
                    response = {"messages": [{"content": f"{original_content}\n\n(Refinado em modo teste)"}]}
                else:
                    response = editing_agent.invoke({
                        "messages": [{"role": "user", "content": editing_prompt}]
                    })
                
                last_msg = response["messages"][-1]
                if hasattr(last_msg, 'content'):
                    refined_content = last_msg.content
                else:
                    refined_content = last_msg.get('content', str(last_msg))
                
                # Limpeza básica se vier como lista/json
                if isinstance(refined_content, str) and refined_content.strip().startswith('['):
                    try:
                        content_list = json.loads(refined_content)
                    except json.JSONDecodeError:
                        try:
                            content_list = ast.literal_eval(refined_content)
                        except:
                            content_list = None

                    if isinstance(content_list, list) and len(content_list) > 0:
                        if isinstance(content_list[0], dict):
                            refined_content = content_list[0].get('text', refined_content)
                        elif isinstance(content_list[0], str):
                            refined_content = content_list[0]
                
                chapter["content"] = refined_content
                
                # Salva incrementalmente o capítulo revisado
                append_chapter_to_ebook(chapter['name'], refined_content)
                
                global_progress.advance(task)
                if idx < len(ebook["chapters"]):
                    time.sleep(0.5)
            
            global_progress.remove_task(task)
            
            print_separator()
            print_success_message("Revisão e refinamento concluídos!")
            print_separator()
        
        global_progress.advance(overall_task)

    return ebook

def append_chapter_to_ebook(chapter_name, content, output_file="result/ebook.md"):
    """Adiciona um capítulo ao arquivo do ebook, substituindo o placeholder <<CAPÍTULOS>> ou anexando."""
    import os
    
    if not os.path.exists(output_file):
        return False
        
    with open(output_file, "r", encoding="utf-8") as f:
        current_content = f.read()
    
    new_chapter_block = f"## {chapter_name}\n\n{content}\n\n---\n\n"
    
    if "<<CAPÍTULOS>>" in current_content:
        # Substitui o placeholder pelo capítulo + novo placeholder para o próximo
        updated_content = current_content.replace(
            "<<CAPÍTULOS>>", 
            f"{new_chapter_block}<<CAPÍTULOS>>"
        )
    else:
        # Se não tiver placeholder, anexa ao final
        updated_content = current_content + "\n\n" + new_chapter_block
        
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    return True

def finalize_ebook_file(output_file="result/ebook.md"):
    """Remove o placeholder <<CAPÍTULOS>> restante."""
    import os
    if not os.path.exists(output_file):
        return
        
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    final_content = content.replace("<<CAPÍTULOS>>", "")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_content)


def extract_epub_metadata(ebook: dict, brd: dict) -> dict:
    """
    Extrai metadata para geração de EPUB a partir de ebook e BRD.
    
    Args:
        ebook: Dicionário com dados do ebook gerado
        brd: Configuração BRD
    
    Returns:
        dict: Metadata para EPUB com title, author, language, copyright, etc.
    """
    from datetime import datetime
    
    project = brd.get("project", {})
    
    metadata = {
        "title": ebook.get("title", project.get("name", "Untitled")),
        "author": project.get("author", "Igor Medeiros"),
        "language": project.get("language", "pt-BR"),
        "description": project.get("description", ""),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "copyright": "© 2025 Igor Medeiros. Todos os direitos reservados.",
        "publisher": "Igor Medeiros - IA na Prática",
        "subject": ["IA", "LangChain", "Desenvolvimento", "Tecnologia"],
    }
    
    return metadata


def save_ebook(ebook, output_file="result/ebook.md", test_mode=False):
    """Finaliza o arquivo do ebook gerando todos os materiais front matter e validando."""
    from .ui import print_info, print_success_message, print_error_message
    
    brd = load_brd()
    chapters = [{"name": ch["name"], "purpose": ""} for ch in ebook.get("chapters", [])]
    
    # Gera Agradecimentos
    print_info("Gerando agradecimentos...")
    acknowledgments_content = generate_acknowledgments(brd, test_mode=test_mode)
    
    # Gera Prefácio
    print_info("Gerando prefácio...")
    preface_content = generate_preface(brd, test_mode=test_mode)
    
    # Gera Sumário
    print_info("Gerando sumário...")
    toc_content = generate_toc(ebook, test_mode=test_mode)
    
    # Gera conclusão
    print_info("Gerando conclusão do ebook...")
    conclusion_content = generate_conclusion(brd, chapters, test_mode=test_mode)
    
    # Gera glossário
    print_info("Gerando glossário...")
    glossary_content = generate_glossary(ebook, test_mode=test_mode)
    
    # Gera bibliografia
    print_info("Gerando referências bibliográficas...")
    bibliography_content = generate_bibliography(ebook, test_mode=test_mode)
    
    # Substitui todos os placeholders
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("<<AGRADECIMENTOS>>", acknowledgments_content)
    content = content.replace("<<PREFÁCIO>>", preface_content)
    content = content.replace("<<SUMÁRIO>>", toc_content)
    content = content.replace("<<PALAVRAS_FINAIS>>", conclusion_content)
    content = content.replace("<<GLOSSÁRIO>>", glossary_content)
    content = content.replace("<<REFERÊNCIAS_BIBLIOGRÁFICAS>>", bibliography_content)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    # Finaliza removendo placeholders restantes
    finalize_ebook_file(output_file)
    
    # Valida se todos os placeholders foram preenchidos
    print_info("Validando template...")
    is_valid, unfilled = validate_template_placeholders(output_file)
    
    if not is_valid:
        print_error_message(f"⚠️ Atenção: {len(unfilled)} placeholder(s) não preenchido(s): {', '.join(unfilled)}")
    else:
        print_success_message("✓ Todos os placeholders foram preenchidos!")
    
    # Gera arquivo .pub com metadata de publicação
    print_info("Gerando metadata de publicação...")
    metadata = extract_epub_metadata(ebook, brd)
    pub_data = {
        "title": metadata["title"],
        "author": metadata["author"],
        "language": metadata["language"],
        "description": metadata["description"],
        "date_generated": metadata["date"],
        "copyright": metadata["copyright"],
        "publisher": metadata["publisher"],
        "subjects": metadata["subject"],
        "chapters": len(ebook.get("chapters", [])),
        "word_count": count_words(content),
        "formats": {
            "markdown": output_file,
            "epub": output_file.replace(".md", ".epub")
        }
    }
    
    pub_file = output_file.replace(".md", ".pub")
    with open(pub_file, "w", encoding="utf-8") as f:
        json.dump(pub_data, f, ensure_ascii=False, indent=2)
    print_success_message(f"✓ Metadata de publicação salvo: {pub_file}")
    
    print_info("Gerando EPUB...")
    try:
        from .epub_generator import generate_epub_from_markdown, validate_epub
        
        epub_output_path = output_file.replace(".md", ".epub")
        success = generate_epub_from_markdown(
            markdown_file_path=output_file,
            output_file_path=epub_output_path,
            metadata=metadata
        )
        
        if success and validate_epub(epub_output_path):
            print_success_message(f"✓ EPUB gerado: {epub_output_path}")
        else:
            print_error_message("⚠️ Erro ao gerar EPUB")
    except Exception as e:
        print_error_message(f"⚠️ Erro ao gerar EPUB: {str(e)}")
    
    return output_file


def generate_acknowledgments(brd, test_mode=False):
    """
    Gera a seção de Agradecimentos do ebook em primeira pessoa.
    
    Args:
        brd: Configuração BRD
        test_mode: Se True, retorna conteúdo mockado
    
    Returns:
        str: Conteúdo dos agradecimentos em Markdown
    """
    if test_mode:
        return "Agradecimentos sinceros a todos que contribuíram para este projeto."
    
    project = brd["project"]
    author_name = project.get("author_name", "Autor")
    author_bio = project.get("author_bio", "")
    
    ack_prompt = f"""Escreva uma seção de AGRADECIMENTOS emocionante e sincera para o ebook "{project['name']}".

AUTOR: {author_name}
BIO DO AUTOR: {author_bio}
DESCRIÇÃO DO EBOOK: {project['description']}

INSTRUÇÕES:
1. Escreva na primeira pessoa (voz do autor).
2. Agradeça à comunidade de tecnologia e saúde.
3. Agradeça aos mentores e inspirações (se houver menção na bio).
4. Agradeça aos leitores pelo apoio.
5. Mantenha um tom humilde, grato e inspirador.

EXTENSÃO: Aproximadamente 300-500 palavras.
FORMATO: Markdown puro, sem título de seção (o título "Agradecimentos" já estará no template).

Retorne APENAS o conteúdo dos agradecimentos em Markdown."""
    
    from .agents import writer_agent
    
    response = writer_agent.invoke({
        "messages": [{"role": "user", "content": ack_prompt}]
    })
    
    # Extrai conteúdo (mesma lógica dos outros)
    messages = response.get("messages", [])
    if messages and isinstance(messages, list) and len(messages) > 0:
        last_msg = messages[-1]
        if hasattr(last_msg, 'content'):
            content = last_msg.content
        elif isinstance(last_msg, dict):
            content = last_msg.get("content", str(last_msg))
        else:
            content = str(last_msg)
    else:
        content = str(response)
    
    # Se o conteúdo for uma lista JSON, extrai o texto
    if isinstance(content, str) and content.strip().startswith('['):
        try:
            content_list = json.loads(content)
            if isinstance(content_list, list) and len(content_list) > 0:
                if isinstance(content_list[0], dict):
                    content = content_list[0].get('text', content)
                elif isinstance(content_list[0], str):
                    content = content_list[0]
        except:
            pass
        
    return content if isinstance(content, str) else str(content)


def generate_preface(brd, test_mode=False):
    """
    Gera a seção de Prefácio do ebook.
    
    Args:
        brd: Configuração BRD
        test_mode: Se True, retorna conteúdo mockado
    
    Returns:
        str: Conteúdo do prefácio em Markdown
    """
    if test_mode:
        return "Bem-vindo a este livro. Aqui começamos uma jornada de aprendizado e transformação."
    
    project = brd["project"]
    target_audience = project.get("target_audience", "Leitores")
    
    preface_prompt = f"""Escreva um PREFÁCIO cativante para o ebook "{project['name']}".

DESCRIÇÃO DO EBOOK: {project['description']}
PÚBLICO-ALVO: {target_audience}

INSTRUÇÕES:
1. Estabeleça o cenário atual e a necessidade deste livro.
2. Fale diretamente com o leitor sobre o que esperar.
3. Explique a filosofia por trás do livro (por que foi escrito).
4. Convide o leitor para a jornada.
5. Mantenha um tom acolhedor e visionário.

EXTENSÃO: Aproximadamente 500-800 palavras.
FORMATO: Markdown puro, sem título de seção (o título "Prefácio" já estará no template).

Retorne APENAS o conteúdo do prefácio em Markdown."""
    
    from .agents import writer_agent
    
    response = writer_agent.invoke({
        "messages": [{"role": "user", "content": preface_prompt}]
    })
    
    # Extrai conteúdo
    messages = response.get("messages", [])
    if messages and isinstance(messages, list) and len(messages) > 0:
        last_msg = messages[-1]
        if hasattr(last_msg, 'content'):
            content = last_msg.content
        elif isinstance(last_msg, dict):
            content = last_msg.get("content", str(last_msg))
        else:
            content = str(last_msg)
    else:
        content = str(response)
    
    # Se o conteúdo for uma lista JSON, extrai o texto
    if isinstance(content, str) and content.strip().startswith('['):
        try:
            content_list = json.loads(content)
            if isinstance(content_list, list) and len(content_list) > 0:
                if isinstance(content_list[0], dict):
                    content = content_list[0].get('text', content)
                elif isinstance(content_list[0], str):
                    content = content_list[0]
        except:
            pass
        
    return content if isinstance(content, str) else str(content)


def generate_toc(ebook, test_mode=False):
    """
    Gera o Sumário (Table of Contents) do ebook.
    
    Args:
        ebook: Dicionário com dados do ebook (incluindo chapters)
        test_mode: Se True, retorna conteúdo mockado
    
    Returns:
        str: Conteúdo do sumário em Markdown com links para os capítulos
    """
    if test_mode:
        return "- [Capítulo Teste 1](#capitulo-teste-1)\n- [Capítulo Teste 2](#capitulo-teste-2)"
    
    chapters = ebook.get("chapters", [])
    toc_lines = []
    
    for idx, chapter in enumerate(chapters, 1):
        # Cria um slug simples para o link markdown
        title = chapter['name']
        # Converte para slug: minúsculas, replace spaces com hífen, remove caracteres especiais
        slug = title.lower().replace(" ", "-").replace(".", "").replace(",", "").replace(":", "").replace("(", "").replace(")", "")
        toc_lines.append(f"- [{title}](#{slug})")
        
    return "\n".join(toc_lines)


