"""
Pipeline de geração de ebook usando LangChain 1.0+.

Padrão LangChain 1.0:
- Carrega BRD do YAML
- Cria queries dinamicamente para cada capítulo
- Executa agent.invoke() para cada query
- Salva resultado
"""

import time
import yaml
from pathlib import Path
from .agents_write import writer_agent

def load_brd():
    """Carrega BRD do arquivo specs/brd.yaml."""
    brd_path = Path(__file__).parent.parent.parent / "specs" / "brd.yaml"
    with open(brd_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_chapter_queries(brd):
    """
    Constrói queries para cada capítulo baseado no BRD.
    
    Returns:
        list: Lista de tuplas (chapter_name, query_text)
    """
    chapters = brd["content_structure"]["chapters"]
    writing_style = brd["writing_style"]
    project = brd["project"]
    
    queries = []
    for chapter in chapters:
        query = f"""Gere o capítulo "{chapter['name']}" do ebook sobre autoconhecimento e inteligência emocional.

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

Escreva o conteúdo seguindo as orientações. O texto deve ser inspirador, prático e transformador."""
        
        queries.append((chapter["name"], query))
    
    return queries

def generate_ebook():
    """Gera o ebook executando agente para cada capítulo."""
    brd = load_brd()
    chapters_queries = build_chapter_queries(brd)
    
    ebook = {
        "title": brd["project"]["name"],
        "description": brd["project"]["description"],
        "chapters": []
    }
    
    print("\n" + "="*70)
    print(f"Gerando ebook: {ebook['title']}")
    print(f"Capítulos: {len(chapters_queries)}")
    print("="*70)
    
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
    
    # Salva resultado
    output_path = save_ebook(ebook)
    
    print("\n" + "="*70)
    print("✓ Ebook gerado com sucesso!")
    print(f"✓ Salvo em: {output_path}")
    print(f"✓ Capítulos: {len(ebook['chapters'])}")
    print("="*70)