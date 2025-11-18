"""
Pipeline de geração de ebook usando LangChain 1.0+.

Padrão LangChain 1.0:
- Carrega BRD do YAML
- Gera estrutura de capítulos via agent
- Gera conteúdo para cada capítulo
- Salva resultado
"""

import time
import yaml
import json
from pathlib import Path

try:
    # Quando executado como módulo (python -m src.main)
    from .agents import writer_agent
except ImportError:
    # Quando executado diretamente (python src/main.py)
    from src.agents import writer_agent

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
    
    # Prepara contexto com tópicos obrigatórios e casos de uso
    required_topics = project.get("required_topics", [])
    main_use_case = project.get("main_use_case", {})
    
    topics_list = "\n".join(f"  - {topic}" for topic in required_topics) if required_topics else ""
    use_case_desc = main_use_case.get("description", "") if main_use_case else ""
    use_case_features = "\n".join(f"  • {feat}" for feat in main_use_case.get("features", [])) if main_use_case else ""
    
    query = f"""Para o ebook "{project['name']}", {content_cfg['structure_prompt']}

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

Retorne APENAS um JSON array com 7 objetos, cada um com as chaves: "name" (string), "purpose" (string), "elements" (array de strings).
Os elementos devem cobrir os tópicos obrigatórios de forma distribuída entre os capítulos.
Exemplo formato:
[{{"name": "Introdução", "purpose": "...", "elements": ["elem1", "elem2"]}}, ...]"""
    
    print("\n🔄 Gerando estrutura de capítulos com tópicos obrigatórios...")
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

def build_chapter_queries(chapters, brd):
    """
    Constrói queries para cada capítulo já gerado.
    
    Args:
        chapters: Lista de dicts com estrutura de capítulos
        brd: Configuração BRD
    
    Returns:
        list: Lista de tuplas (chapter_name, query_text)
    """
    writing_style = brd["writing_style"]
    project = brd["project"]
    
    queries = []
    for chapter in chapters:
        query = f"""Gere o capítulo "{chapter['name']}" do ebook: {project['name']}

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

Escreva o conteúdo em Markdown puro, seguindo as orientações. Foco em prático, educativo e ético."""
        
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
    
    # Etapa 3: Gerar queries para cada capítulo
    chapters_queries = build_chapter_queries(chapters, brd)
    
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