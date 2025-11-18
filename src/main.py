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
    from .agents import writer_agent, research_agent
except ImportError:
    # Quando executado diretamente (python src/main.py)
    from src.agents import writer_agent, research_agent

def load_brd():
    """Carrega BRD do arquivo specs/brd.yaml."""
    brd_path = Path(__file__).parent.parent / "specs" / "brd.yaml"
    with open(brd_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

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
    
    Args:
        chapter_name: Nome do capítulo
        chapter_purpose: Propósito do capítulo
        chapter_elements: Elementos obrigatórios
        brd: Configuração BRD
    
    Returns:
        str: Conteúdo de research em Markdown
    """
    project = brd["project"]
    
    query = f"""Faça uma pesquisa profunda e estruturada sobre o capítulo: "{chapter_name}"

Propósito do capítulo:
{chapter_purpose}

Elementos a cobrir:
{chr(10).join(f"• {elem}" for elem in chapter_elements)}

Contexto do ebook: {project['name']}
Público-alvo: {project['target_audience']}

Sua pesquisa deve incluir:
1. Conceitos fundamentais e contexto
2. Melhores práticas comprovadas
3. Considerações éticas e compliance
4. Exemplos práticos e casos reais
5. Riscos e mitigações
6. Referências e fontes

Estruture a resposta em Markdown com seções claras e profundidade técnica.
Esta pesquisa será a base para o conteúdo final do capítulo."""
    
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
    
    # Etapa 1: Gerar estrutura
    chapters = generate_chapter_structure(brd)
    
    if not chapters:
        print("Falha ao gerar estrutura. Abortando.")
        return None
    
    # Etapa 2: Preparar dados do ebook
    ebook = {
        "title": brd["project"]["name"],
        "description": brd["project"]["description"],
        "chapters": []
    }
    
    print("\n" + "="*70)
    print(f"EBOOK: {ebook['title']}")
    print("="*70)
    print(f"\nDescrição: {ebook['description']}\n")
    print(f"Público-alvo: {brd['project']['target_audience']}\n")
    
    # Mostrar capítulos gerados
    print("CAPÍTULOS A GERAR:")
    print("-"*70)
    for i, chapter in enumerate(chapters, 1):
        print(f"  [{i}] {chapter['name']}")
        print(f"      Propósito: {chapter['purpose']}")
    
    print("\n" + "="*70)
    
    # Pedir aprovação
    while True:
        response = input("Deseja prosseguir com a geração? (s/n): ").strip().lower()
        if response in ['s', 'sim']:
            break
        elif response in ['n', 'não', 'nao']:
            print("Geração cancelada.")
            return None
        else:
            print("Digite 's' ou 'n'")
    
    print("\n" + "="*70)
    print(f"Gerando ebook: {ebook['title']}")
    print(f"Capítulos: {len(chapters)}")
    print("="*70)
    
    # Etapa 3: Fazer research de cada capítulo e salvar em kb/
    print("\n📚 ETAPA 1: RESEARCH E SALVAMENTO EM KB/")
    print("-"*70)
    research_data = {}
    for idx, chapter in enumerate(chapters, 1):
        print(f"\n[{idx}/{len(chapters)}] {chapter['name']}")
        
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
        print(f"  ✓ Salvo em: {kb_path}")
        
        if idx < len(chapters):
            time.sleep(1)  # Pequeno delay entre requests
    
    print("\n✓ Todas as pesquisas foram salvas em kb/")
    print("\n📝 ETAPA 2: GERAÇÃO DE CONTEÚDO")
    print("-"*70)
    
    # Etapa 4: Gerar queries para cada capítulo (agora com research como contexto)
    chapters_queries = build_chapter_queries_with_research(chapters, research_data, brd)
    
    for idx, (chapter_name, query) in enumerate(chapters_queries, 1):
        print(f"\n[{idx}/{len(chapters_queries)}] Gerando: {chapter_name}")
        print("-" * 70)
        
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
            import json
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
        
        print(f"✓ {chapter_name} concluída")
        
        if idx < len(chapters_queries):
            print("\nAguardando 2 segundos...")
            time.sleep(2)
    
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
    # Gera ebook
    ebook = generate_ebook()
    
    # Verifica se foi cancelado
    if ebook is None:
        print("Nenhum ebook foi gerado.")
        exit(0)
    
    # Salva resultado
    output_path = save_ebook(ebook)
    
    print("\n" + "="*70)
    print("✓ Ebook gerado com sucesso!")
    print(f"✓ Salvo em: {output_path}")
    print(f"✓ Capítulos: {len(ebook['chapters'])}")
    print("="*70)