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
from functools import lru_cache
from pathlib import Path

try:
    # Quando executado como módulo (python -m src.main)
    from .agents import writer_agent, research_agent, thematic_research_agent
    from .ui import (
        print_header, print_ebook_info, print_chapters_preview,
        get_confirmation, print_phase_header, print_research_start,
        print_research_saved, print_content_generation_start,
        print_content_generated, print_success_message, print_error_message,
        print_completion_summary, print_separator, print_info
    )
except ImportError:
    # Quando executado diretamente (python src/main.py)
    from src.agents import writer_agent, research_agent, thematic_research_agent
    from src.ui import (
        print_header, print_ebook_info, print_chapters_preview,
        get_confirmation, print_phase_header, print_research_start,
        print_research_saved, print_content_generation_start,
        print_content_generated, print_success_message, print_error_message,
        print_completion_summary, print_separator, print_info
    )

try:
    from .config import get_config
except ImportError:
    from src.config import get_config

def load_brd():
    """Carrega BRD do arquivo specs/brd.yaml."""
    brd_path = Path(__file__).parent.parent / "specs" / "brd.yaml"
    with open(brd_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


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

def generate_chapter_structure(brd):
    """
    Gera a estrutura de capítulos usando o writer_agent.
    
    Returns:
        list: Lista de dicts com {name, purpose, elements}
    """
    writing_style = brd["writing_style"]
    project = brd["project"]
    content_cfg = brd["content_structure"]
    
    # Parâmetros dinâmicos do project
    number_chapters = project.get("number_chapters", 7)
    target_word_count = project.get("target_word_count", 10000)
    required_topics = project.get("required_topics", [])
    main_use_case = project.get("main_use_case", {})
    
    topics_list = "\n".join(f"  - {topic}" for topic in required_topics) if required_topics else ""
    use_case_desc = main_use_case.get("description", "") if main_use_case else ""
    use_case_features = "\n".join(f"  • {feat}" for feat in main_use_case.get("features", [])) if main_use_case else ""
    
    query = f"""Para o ebook "{project['name']}", crie uma estrutura de {number_chapters} capítulos, cada um com nome, propósito e elementos obrigatórios a incluir.

REQUISITOS:
- Total de aproximadamente {target_word_count} palavras distribuídas nos {number_chapters} capítulos
- Cada capítulo deve ter aproximadamente {target_word_count // number_chapters} palavras
- {content_cfg['structure_prompt']}

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
        
        # Se começar com [, é JSON direto
        if content.strip().startswith('['):
            try:
                chapters = json.loads(content)
                return chapters
            except (json.JSONDecodeError, ValueError) as e:
                print(f"❌ Erro ao parsear como JSON array: {e}")
    
    print("❌ Não foi possível gerar estrutura de capítulos")
    return []

def generate_chapter_research(chapter_name, chapter_purpose, chapter_elements, brd):
    """Conduz pesquisa profunda sobre um capítulo usando research_agent."""

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
- Estruture o texto seguindo as seções do template principal (Resumo Executivo → Introdução → Corpo Técnico → Desafios → Tendências).
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

def generate_thematic_research(brd):
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

    for idx, topic in enumerate(required_topics, 1):
        print(f"  [{idx}/{len(required_topics)}] 🔍 Pesquisa temática: {topic}...")

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
            print(f"    ⚠️ Conteúdo de '{topic}' possui {word_count} palavras (mínimo recomendado: {min_words}).")
        else:
            print(f"    🧮 Contagem aproximada: {word_count} palavras.")

        # SALVAMENTO IMEDIATO após geração de cada tema
        file_path = save_thematic_research_immediately(topic, research_content, brd, word_count=word_count)
        thematic_research_paths[topic] = file_path
        print(f"  📝 Salvo imediatamente: {Path(file_path).name}\n")

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
    writing_style = brd["writing_style"]
    project = brd["project"]
    
    # Calcula palavras por capítulo
    target_word_count = project.get("target_word_count", 10000)
    number_chapters = len(chapters)
    words_per_chapter = target_word_count // number_chapters
    
    queries = []
    for idx, chapter in enumerate(chapters, 1):
        research_context = research_data.get(chapter['name'], "")
        
        query = f"""Gere o capítulo {idx}/{number_chapters} "{chapter['name']}" do ebook: {project['name']}

REQUISITOS:
- Aproximadamente {words_per_chapter} palavras
- Este é o capítulo {idx} de {number_chapters}

CONTEXTO DE RESEARCH (use como base):
{research_context[:2000]}...

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

Escreva o conteúdo em Markdown puro, baseado no research fornecido. Foco em prático, educativo e ético. O conteúdo deve ter aproximadamente {words_per_chapter} palavras."""
        
        queries.append((chapter["name"], query))
    
    return queries

def generate_ebook():
    """Gera o ebook executando agente para estrutura e depois para cada capítulo."""
    brd = load_brd()
    
    # Header
    print_header(
        "📚 Gerador de Ebook Técnico",
        "LangChain 1.0 na Saúde Clínica"
    )
    
    # Etapa 1: Gerar estrutura
    print_info("Gerando estrutura de capítulos...")
    chapters = generate_chapter_structure(brd)
    
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
    if not get_confirmation():
        return None
    
    print_separator()
    
    # FASE 1: Pesquisa Temática Abrangente (baseada em required_topics)
    print_phase_header(1, "PESQUISA TEMÁTICA", "Pesquisas abrangentes sobre tópicos obrigatórios")
    
    # Verificar se pesquisas temáticas já existem
    existing_thematic = check_existing_thematic_research(brd)
    perform_thematic = ask_perform_thematic_research(len(existing_thematic), len(brd["project"].get("required_topics", [])))
    
    thematic_research_paths = {}
    if perform_thematic:
        thematic_research_paths = generate_thematic_research(brd)
        if thematic_research_paths:
            print_separator()
            print(f"  ✅ {len(thematic_research_paths)} pesquisas temáticas geradas e salvas imediatamente em kb/")
            print_separator()
    else:
        thematic_research_paths = existing_thematic
        print_separator()
        print(f"  ℹ️  Usando {len(existing_thematic)} pesquisas temáticas já existentes em kb/")
        print_separator()
    
    # Pergunta sobre armazenamento RAG
    rag_storage = ask_rag_storage_method()
    
    print_separator()
    if rag_storage == 'supabase':
        print("  📤 RAG será armazenado em Supabase (implementação futura)")
    else:
        print("  📁 RAG será armazenado localmente em kb/")
    print_separator()
    
    # FASE 2: Pesquisa por Capítulo (usando as temáticas como base)
    print_phase_header(2, "RESEARCH E SALVAMENTO", "Pesquisa profunda e salvamento em kb/")
    
    research_data = {}
    for idx, chapter in enumerate(chapters, 1):
        print_research_start(chapter['name'], idx, len(chapters))
        
        # Gera research
        research_content, research_word_count = generate_chapter_research(
            chapter['name'],
            chapter['purpose'],
            chapter['elements'],
            brd
        )
        research_data[chapter['name']] = research_content

        # Salva em kb/
        kb_path = save_research_to_kb(
            chapter['name'], research_content, brd, word_count=research_word_count
        )
        print_research_saved(kb_path, len(research_content))
        
        if idx < len(chapters):
            time.sleep(0.5)  # Pequeno delay entre requests
    
    print_separator()
    print_success_message("Todas as pesquisas foram salvas em kb/")
    print_separator()
    
    # FASE 3: Geração de conteúdo
    print_phase_header(3, "GERAÇÃO DE CONTEÚDO", "Geração de conteúdo final baseado em research")
    
    # Gerar queries para cada capítulo (agora com research como contexto)
    chapters_queries = build_chapter_queries_with_research(chapters, research_data, brd)
    
    words_per_chapter = brd['project'].get('target_word_count', 10000) // len(chapters)
    
    for idx, (chapter_name, query) in enumerate(chapters_queries, 1):
        print_content_generation_start(chapter_name, idx, len(chapters_queries), words_per_chapter)
        
        # Executa agent com query
        response = writer_agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        
        # Extrai conteúdo
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
        
        # Se o conteúdo for uma lista JSON (começa com '['), extrai o texto
        if isinstance(content, str) and content.strip().startswith('['):
            try:
                content_list = json.loads(content)
                if isinstance(content_list, list) and len(content_list) > 0:
                    # Extrai o texto do primeiro item
                    if isinstance(content_list[0], dict):
                        content = content_list[0].get('text', content)
                    elif isinstance(content_list[0], str):
                        content = content_list[0]
            except:
                pass  # Mantém o conteúdo original se falhar
        
        ebook["chapters"].append({
            "name": chapter_name,
            "content": content
        })
        
        print_content_generated(len(content))
        
        if idx < len(chapters_queries):
            time.sleep(0.5)
    
    print_separator()
    return ebook

def save_ebook(ebook, output_file="result/ebook.md"):
    """Salva ebook em formato Markdown."""
    import os
    
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# {ebook['title']}\n\n")
        f.write(f"{ebook['description']}\n\n")
        f.write("---\n\n")
        
        for chapter in ebook["chapters"]:
            f.write(f"## {chapter['name']}\n\n")
            f.write(f"{chapter['content']}\n\n")
            f.write("---\n\n")
    
    return output_file


if __name__ == "__main__":
    try:
        # Gera ebook
        ebook = generate_ebook()
        
        # Verifica se foi cancelado
        if ebook is None:
            exit(0)
        
        # Salva resultado
        print_info("Salvando ebook em Markdown...")
        output_path = save_ebook(ebook)
        
        print_separator()
        
        # Exibe resumo final
        print_completion_summary(
            ebook['title'],
            len(ebook['chapters']),
            output_path
        )
        
        print_separator()
        print_success_message("Pipeline concluído com sucesso!")
        
    except KeyboardInterrupt:
        print_separator()
        print_error_message("Pipeline interrompido pelo usuário")
        exit(1)
    except Exception as e:
        print_separator()
        print_error_message(f"Erro durante execução: {str(e)}")
        exit(1)