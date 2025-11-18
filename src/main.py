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
from pathlib import Path

try:
    # Quando executado como módulo (python -m src.main)
    from .agents import (
        writer_agent,
        research_agent,
        thematic_research_agent,
        create_document_spec_agent,
        create_ideation_agent,
        create_title_agent,
        create_structure_agent,
        create_deep_research_agent,
        create_chapter_agent,
        create_review_coordinator_agent,
        create_critical_reading_coordinator_agent,
        create_editing_agent,
        create_finalization_agent,
        create_publication_agent,
        create_technical_reviewer_agent,
        create_curious_beginner_agent,
        execute_agent,
        execute_review_personas,
    )
    from .config import (
        get_model,
        get_research_model,
        get_config,
        get_message,
        print_pipeline_start,
        print_stage_header,
        print_stage_complete,
        print_pipeline_complete,
        print_error_panel,
    )
    from .ui import (
        print_header, print_ebook_info, print_chapters_preview,
        get_confirmation, print_phase_header, print_research_start,
        print_research_saved, print_content_generation_start,
        print_content_generated, print_success_message, print_error_message,
        print_completion_summary, print_separator, print_info
    )
except ImportError:
    # Quando executado diretamente (python src/main.py)
    from src.agents import (
        writer_agent,
        research_agent,
        thematic_research_agent,
        create_document_spec_agent,
        create_ideation_agent,
        create_title_agent,
        create_structure_agent,
        create_deep_research_agent,
        create_chapter_agent,
        create_review_coordinator_agent,
        create_critical_reading_coordinator_agent,
        create_editing_agent,
        create_finalization_agent,
        create_publication_agent,
        create_technical_reviewer_agent,
        create_curious_beginner_agent,
        execute_agent,
        execute_review_personas,
    )
    from src.config import (
        get_model,
        get_research_model,
        get_config,
        get_message,
        print_pipeline_start,
        print_stage_header,
        print_stage_complete,
        print_pipeline_complete,
        print_error_panel,
    )
    from src.ui import (
        print_header, print_ebook_info, print_chapters_preview,
        get_confirmation, print_phase_header, print_research_start,
        print_research_saved, print_content_generation_start,
        print_content_generated, print_success_message, print_error_message,
        print_completion_summary, print_separator, print_info
    )

def load_brd():
    """Carrega BRD do arquivo specs/brd.yaml."""
    brd_path = Path(__file__).parent.parent / "specs" / "brd.yaml"
    with open(brd_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

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
    """
    Conduz pesquisa profunda sobre um capítulo usando research_agent.
    
    Aplica os requisitos de qualidade do deep_research do config.yaml:
    - Mínimo 2000 palavras
    - Mínimo 5 fontes confiáveis
    - Estrutura: Contexto → Problema → Solução → Aplicação → Ética
    
    Args:
        chapter_name: Nome do capítulo
        chapter_purpose: Propósito do capítulo
        chapter_elements: Elementos obrigatórios
        brd: Configuração BRD
    
    Returns:
        str: Conteúdo de research em Markdown
    """
    project = brd["project"]
    
    query = f"""Realize uma pesquisa profunda e contextualizada sobre o capítulo: "{chapter_name}"

CONTEXTO DO EBOOK:
Nome: {project['name']}
Descrição: {project['description']}
Público-alvo: {project['target_audience']}
Tópicos Obrigatórios: {', '.join(project.get('required_topics', []))}

ESPECIFICAÇÕES DO CAPÍTULO:
Propósito:
{chapter_purpose}

Elementos a cobrir:
{chr(10).join(f"• {elem}" for elem in chapter_elements)}

REQUISITOS DE QUALIDADE MANDATÓRIOS:
✓ Mínimo 2000 palavras de conteúdo substantivo
✓ Mínimo 5 fontes confiáveis e referências validadas
✓ Estrutura clara e lógica
✓ Profundidade técnica apropriada para o público-alvo
✓ Balanceamento entre teoria e prática

ESTRUTURA ESPERADA:
1. Resumo Executivo (150-200 palavras)
   - Overview do tópico
   - Relevância para o contexto clínico
   
2. Contexto e Fundamentação (300-500 palavras)
   - Histórico e evolução do tópico
   - Por que é importante agora
   - Conexão com LangChain e IA na saúde
   
3. Conceitos Fundamentais (400-600 palavras)
   - Definições e terminologia
   - Arquitetura e componentes
   - Princípios-chave
   
4. Melhores Práticas e Padrões (400-600 palavras)
   - Implementações comprovadas
   - Anti-padrões a evitar
   - Casos de uso bem-sucedidos
   
5. Considerações de Compliance e Ética (300-500 palavras)
   - Regulamentações aplicáveis (LGPD, normas clínicas)
   - Considerações éticas e de responsabilidade
   - Riscos e mitigações
   - Transparência e auditoria
   
6. Aplicação Prática (300-500 palavras)
   - Exemplos concretos e executáveis
   - Padrões de código LangChain (pseudocódigo ou sintaxe)
   - Fluxos de integração
   - Métricas de sucesso
   
7. Referências e Fontes (em seção separada)
   - Mínimo 5 fontes validadas
   - Mix de: papers científicos, documentação técnica, blogs especializados
   - Formato: [1] Título - Autor/Fonte - URL/DOI - Data de acesso

INSTRUÇÕES CRÍTICAS:
- Escreva em Markdown com formatação clara
- Use headings hierárquicos (#, ##, ###)
- Destaque pontos críticos em **negrito** e considerações em > blockquotes
- Inclua tabelas comparativas quando relevante
- Mantenha tom técnico mas acessível
- Sempre cite as fontes de informação
- Faça conexões explícitas com LangChain 1.0 e ambientes clínicos
- Se houver código, use blocos ```python ou ```
- Total de conteúdo: 2000+ palavras

Sua pesquisa será a base para a escrita do capítulo, então seja completo, fundamentado e práticável."""
    
    print(f"  🔍 Pesquisando: {chapter_name}...")
    response = research_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    
    content = response["messages"][-1].content
    
    # Se for lista com artifacts (Gemini format), extrai o texto
    if isinstance(content, list) and len(content) > 0:
        if isinstance(content[0], dict) and 'text' in content[0]:
            content = content[0]['text']
    
    return content if isinstance(content, str) else str(content)

def save_thematic_research_immediately(topic, content, brd):
    """
    Salva pesquisa temática em kb/ imediatamente após geração.
    
    Args:
        topic: Nome do tópico
        content: Conteúdo da pesquisa
        brd: Configuração BRD
    
    Returns:
        str: Caminho do arquivo salvo
    """
    kb_dir = Path(__file__).parent.parent / "kb"
    kb_dir.mkdir(exist_ok=True)
    
    # Normaliza nome do arquivo
    safe_name = topic.lower().replace(" ", "_").replace("(", "").replace(")", "")
    file_path = kb_dir / f"thematic_{safe_name}.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Pesquisa Temática: {topic}\n\n")
        f.write(f"Ebook: {brd['project']['name']}\n")
        f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Tipo: Pesquisa Temática Abrangente\n\n")
        f.write("---\n\n")
        f.write(content)
    
    return str(file_path)

def generate_thematic_research(brd):
    """
    Gera pesquisas temáticas abrangentes baseadas nos required_topics do BRD.
    
    Cada tópico obrigatório gera um documento independente de pesquisa que pode
    alimentar múltiplos capítulos. Diferente da pesquisa por capítulo, a pesquisa
    temática é mais abrangente e profunda.
    
    IMPORTANTE: Cada pesquisa é SALVA IMEDIATAMENTE após geração em kb/ de acordo
    com deep_research.thematic_research.save_immediately no config.yaml
    
    Args:
        brd: Configuração BRD com required_topics
    
    Returns:
        dict: {topic_name: file_path, ...} (paths dos arquivos salvos)
    """
    project = brd["project"]
    required_topics = project.get("required_topics", [])
    
    if not required_topics:
        print("⚠️ Nenhum tópico obrigatório encontrado no BRD")
        return {}
    
    thematic_research_paths = {}
    print(f"\n📚 Gerando pesquisas temáticas abrangentes para {len(required_topics)} tópicos...\n")
    print("   (Salvamento imediato ativado - cada tema é persistido em kb/ após geração)\n")
    
    for idx, topic in enumerate(required_topics, 1):
        print(f"  [{idx}/{len(required_topics)}] 🔍 Pesquisa temática: {topic}...")
        
        query = f"""Conduza uma pesquisa temática ABRANGENTE e PROFUNDA sobre: "{topic}"

CONTEXTO DO EBOOK:
Nome: {project['name']}
Descrição: {project['description']}
Público-alvo: {project['target_audience']}

INSTRUÇÕES CRÍTICAS:
Esta pesquisa é TEMÁTICA E INDEPENDENTE, não vinculada a um capítulo específico.
Deve ser um documento de referência COMPLETO que alimentará MÚLTIPLOS capítulos.

Portanto:
- Seja ABRANGENTE: cubra todas as dimensões do tema
- Seja APROFUNDADO: não superficial, mas com detalhes técnicos significativos
- Seja AUTOSSUFICIENTE: o documento deve ser inteligível por si só
- Seja REUTILIZÁVEL: estruturado para ser referenciado por vários capítulos

REQUISITOS DE QUALIDADE OBRIGATÓRIOS:
✓ Mínimo 3000 palavras (tema é denso e abrangente)
✓ Mínimo 7 fontes confiáveis (documentação oficial, papers, referências validadas)
✓ Hierarquia clara com no mínimo 8 seções temáticas
✓ Tabelas comparativas quando relevante
✓ Exemplos de código LangChain ou pseudocódigo comentado
✓ Diagramas textuais de arquitetura
✓ Glossário de termos técnicos do tema

REQUISITO ESPECIAL - EXEMPLOS DE CÓDIGO FONTE:
Se o tema for um FRAMEWORK, BIBLIOTECA ou TECNOLOGIA (ex: LangChain, RAG, EHRs):
  ✓ OBRIGATÓRIO incluir exemplos de código fonte prático
  ✓ Estrutura de código comentada e funcional
  ✓ Padrões de uso comum em Python
  ✓ Integração com LangChain quando aplicável
  ✓ Fluxo de execução com pseudocódigo
  ✓ Casos de uso clínicos reais com código
  ✓ Erros frequentes e como evitá-los (com exemplos)

Se o tema for CONCEITUAL (ex: Ética em IA, Compliance):
  ✓ Exemplos de código NÃO são necessários
  ✓ Foco em discussão, regulamentação, princípios
  ✓ Use tabelas e diagramas conceituais

ESTRUTURA ESPERADA:
1. Resumo Executivo (300-400 palavras)
   - O que é o tema
   - Por que é importante em contextos clínicos
   - Principais conceitos
   - Como se integra ao ecosistema LangChain

2. Histórico e Evolução (300-400 palavras)
   - Origem do conceito/tecnologia
   - Evolução no tempo
   - Estado-da-arte atual
   - Roadmap futuro

3. Conceitos Fundamentais e Arquitetura (500-700 palavras)
   - Definições precisas
   - Componentes principais
   - Arquitetura (com diagrama textual)
   - Fluxos de dados/controle
   - Padrões de design

4. Integração com LangChain 1.0 (400-500 palavras)
   - Como este tema se integra ao LangChain
   - APIs e métodos relevantes
   - Exemplos de código LangChain
   - Limitações e considerações

5. Melhores Práticas e Padrões Comprovados (400-600 palavras)
   - Implementações recomendadas
   - Padrões de design
   - Performance e otimizações
   - Escalabilidade
   - Monitoramento

6. Anti-padrões e Armadilhas Comuns (300-400 palavras)
   - Erros frequentes
   - Por que evitá-los
   - Consequências
   - Como detectar

7. Aplicabilidade em Ambientes Clínicos (400-600 palavras)
   - Requisitos clínicos específicos
   - Adaptações necessárias
   - Casos de uso clínicos reais
   - Desafios específicos da saúde

8. Compliance, Segurança e Ética (400-600 palavras)
   - Regulamentações aplicáveis (LGPD, HIPAA, normas clínicas)
   - Considerações de privacidade
   - Vieses e fairness
   - Auditoria e rastreabilidade
   - Transparência algorítmica

9. Implementação Prática com Exemplos (500-700 palavras)
   - Exemplos concretos de código
   - Pseudocódigo comentado
   - Guias passo-a-passo
   - Integrações com sistemas clínicos

10. Referências e Glossário (separado)
    - Mínimo 7 fontes com URLs/DOIs
    - Data de acesso
    - Glossário de 20+ termos técnicos do tema

FORMATAÇÃO:
- Use Markdown com hierarquia clara (# ## ###)
- Blocos de código: ```python ou ```
- Tabelas para comparações
- Blockquotes para destaques
- Listas numeradas e com bullets
- Ênfase em **bold** para conceitos-chave

RESULTADO FINAL:
Um documento denso, profundo, completo e pronto para ser referência compartilhada
por múltiplos capítulos do ebook. Não é resumido - é abrangente."""
        
        response = thematic_research_agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        
        content = response["messages"][-1].content
        
        # Se for lista com artifacts (Gemini format), extrai o texto
        if isinstance(content, list) and len(content) > 0:
            if isinstance(content[0], dict) and 'text' in content[0]:
                content = content[0]['text']
        
        research_content = content if isinstance(content, str) else str(content)
        
        # SALVAMENTO IMEDIATO após geração de cada tema
        file_path = save_thematic_research_immediately(topic, research_content, brd)
        thematic_research_paths[topic] = file_path
        print(f"  📝 Salvo imediatamente: {Path(file_path).name}\n")
    
    return thematic_research_paths

def save_research_to_kb(chapter_name, research_content, brd):
    """
    Salva research em kb/ como arquivo Markdown.
    
    Args:
        chapter_name: Nome do capítulo (usado para nome do arquivo)
        research_content: Conteúdo de research
        brd: Configuração BRD
    
    Returns:
        str: Caminho do arquivo salvo
    """
    kb_dir = Path(__file__).parent.parent / "kb"
    kb_dir.mkdir(exist_ok=True)
    
    # Normaliza nome do arquivo
    safe_name = chapter_name.lower().replace(" ", "_").replace(":", "")
    file_path = kb_dir / f"research_{safe_name}.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Research: {chapter_name}\n\n")
        f.write(f"Ebook: {brd['project']['name']}\n")
        f.write(f"Data: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
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
        research_content = generate_chapter_research(
            chapter['name'],
            chapter['purpose'],
            chapter['elements'],
            brd
        )
        research_data[chapter['name']] = research_content
        
        # Salva em kb/
        kb_path = save_research_to_kb(chapter['name'], research_content, brd)
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


def _prepare_prompt(template: str, **context) -> str:
    """Safely render prompt templates without raising on missing keys."""

    if not template:
        return ""
    try:
        return template.format(**context)
    except KeyError:
        return template


def _build_review_persona_agents(model, personas_config=None):
    """Instantiate review personas using the configured model."""

    return {
        "Technical Reviewer": create_technical_reviewer_agent(model)
    }


def _build_virtual_reader_agents(model, readers_config=None):
    """Instantiate virtual reader personas."""

    return {
        "Curious Beginner": create_curious_beginner_agent(model)
    }


def run_ebook_pipeline(
    topic: str,
    target_audience: str,
    word_count_target: int = 10000,
    transformation_promise: str | None = None,
    reading_level: str | None = None,
    run_all_stages: bool = True,
):
    """Execute the multi-stage ebook pipeline orchestrated via LangChain agents."""

    results = {}
    try:
        print_pipeline_start(topic, target_audience, word_count_target)
        get_message("pipeline_start")
        config = get_config()
        prompt_templates = config.get("agent_prompts", {})

        write_model = get_model()
        research_model = get_research_model()

        context = {
            "topic": topic,
            "target_audience": target_audience,
            "word_count_target": word_count_target,
            "transformation_promise": transformation_promise or "",
            "reading_level": reading_level or "",
        }

        # Stage 1 - Document Spec
        print_stage_header(1, "Document Spec", "Consolidação do BRD")
        doc_prompt = (
            f"Topic: {topic}\nTarget Audience: {target_audience}\n"
            f"Word Count Target: {word_count_target}\n"
            f"Transformation Promise: {transformation_promise or 'N/A'}\n"
            f"Reading Level: {reading_level or 'N/A'}"
        )
        stage_start = time.time()
        document_spec_agent = create_document_spec_agent(research_model)
        doc_output = execute_agent(document_spec_agent, doc_prompt)
        context["document_spec_output"] = doc_output
        results["stage_1_document_spec"] = doc_output
        print_stage_complete(1, time.time() - stage_start)

        if not run_all_stages:
            results["pipeline_status"] = "partial"
            return results

        # Stage 2 - Ideation
        print_stage_header(2, "Ideation", "Expansão criativa")
        ideation_prompt = _prepare_prompt(
            prompt_templates.get("ideation_prompt_template", "{topic}"),
            **context,
        )
        stage_start = time.time()
        ideation_agent = create_ideation_agent(write_model)
        ideation_output = execute_agent(ideation_agent, ideation_prompt)
        context["ideation_output"] = ideation_output
        results["stage_2_ideation"] = ideation_output
        print_stage_complete(2, time.time() - stage_start)

        # Stage 3 - Title
        print_stage_header(3, "Title", "Geração de títulos")
        title_prompt = _prepare_prompt(
            prompt_templates.get("title_prompt_template", "{ideation_output}"),
            **context,
        )
        stage_start = time.time()
        title_agent = create_title_agent(write_model)
        title_output = execute_agent(title_agent, title_prompt)
        context["title_output"] = title_output
        results["stage_3_title"] = title_output
        print_stage_complete(3, time.time() - stage_start)

        # Stage 4 - Structure
        print_stage_header(4, "Structure", "Construção de capítulos")
        structure_prompt = _prepare_prompt(
            prompt_templates.get("structure_prompt_template", "{topic}"),
            **context,
        )
        stage_start = time.time()
        structure_agent = create_structure_agent(write_model)
        structure_output = execute_agent(structure_agent, structure_prompt)
        context["structure_output"] = structure_output
        results["stage_4_structure"] = structure_output
        print_stage_complete(4, time.time() - stage_start)

        # Stage 5 - Deep Research
        print_stage_header(5, "Deep Research", "Pesquisa especializada")
        research_prompt = _prepare_prompt(
            prompt_templates.get("deep_research_prompt_template", "{structure_output}"),
            **context,
        )
        stage_start = time.time()
        deep_research_agent = create_deep_research_agent(research_model)
        deep_research_output = execute_agent(deep_research_agent, research_prompt)
        context["deep_research_output"] = deep_research_output
        results["stage_5_deep_research"] = deep_research_output
        print_stage_complete(5, time.time() - stage_start)

        # Stage 6 - Chapter Writing
        print_stage_header(6, "Chapter Writing", "Redação técnica")
        chapter_prompt = _prepare_prompt(
            prompt_templates.get("chapter_writing_prompt_template", "{structure_output}"),
            **context,
        )
        stage_start = time.time()
        chapter_agent = create_chapter_agent(write_model)
        chapter_output = execute_agent(chapter_agent, chapter_prompt)
        context["chapter_output"] = chapter_output
        results["stage_6_chapter_writing"] = chapter_output
        print_stage_complete(6, time.time() - stage_start)

        # Stage 7 - Specialized Review
        print_stage_header(7, "Review Personas", "Coordenação de revisores")
        review_agent = create_review_coordinator_agent(research_model)
        review_personas = _build_review_persona_agents(research_model)
        review_feedback = execute_review_personas(
            review_agent, chapter_output, review_personas
        )
        context["review_output"] = review_feedback
        results["stage_7_review"] = review_feedback
        print_stage_complete(7)

        # Stage 8 - Virtual Readers
        print_stage_header(8, "Virtual Readers", "Leitura crítica")
        critical_agent = create_critical_reading_coordinator_agent(research_model)
        virtual_readers = _build_virtual_reader_agents(write_model)
        critical_feedback = execute_review_personas(
            critical_agent, chapter_output, virtual_readers
        )
        context["critical_output"] = critical_feedback
        results["stage_8_critical_reading"] = critical_feedback
        print_stage_complete(8)

        # Stage 9 - Editing
        print_stage_header(9, "Editing", "Higienização editorial")
        editing_prompt = _prepare_prompt(
            prompt_templates.get("editing_prompt_template", "{critical_output}"),
            **context,
        )
        stage_start = time.time()
        editing_agent = create_editing_agent(write_model)
        editing_output = execute_agent(editing_agent, editing_prompt)
        context["editing_output"] = editing_output
        results["stage_9_editing"] = editing_output
        print_stage_complete(9, time.time() - stage_start)

        # Stage 10 - Finalization
        print_stage_header(10, "Finalization", "Materiais finais")
        final_prompt = _prepare_prompt(
            prompt_templates.get("finalization_prompt_template", "{editing_output}"),
            **context,
        )
        stage_start = time.time()
        finalization_agent = create_finalization_agent(write_model)
        finalization_output = execute_agent(finalization_agent, final_prompt)
        context["finalization_output"] = finalization_output
        results["stage_10_finalization"] = finalization_output
        print_stage_complete(10, time.time() - stage_start)

        # Stage 11 - Publication
        print_stage_header(11, "Publication", "Exportação e KDP")
        publication_prompt = _prepare_prompt(
            prompt_templates.get("publication_prompt_template", "{editing_output}"),
            **context,
        )
        stage_start = time.time()
        publication_agent = create_publication_agent(write_model)
        publication_output = execute_agent(publication_agent, publication_prompt)
        results["stage_11_publication"] = publication_output
        print_stage_complete(11, time.time() - stage_start)

        results["pipeline_status"] = "completed"
        results["summary"] = {
            "topic": topic,
            "target_audience": target_audience,
            "stages_completed": 11,
            "total_stages": 11,
            "final_ebook_path": None,
        }
        print_pipeline_complete(results)
        return results
    except Exception as exc:  # noqa: BLE001
        print_error_panel("Erro no Pipeline", str(exc))
        return {"pipeline_status": "error", "error": str(exc)}


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