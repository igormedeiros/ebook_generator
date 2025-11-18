"""
Pipeline de geração de ebook usando LangChain 1.0+.

Arquitetura simples:
1. Carrega BRD do YAML
2. Para cada capítulo, constrói query baseada no BRD
3. Executa agent.invoke(query)
4. Compila resultado
"""

import time
from agents import writer_agent
from tasks import get_all_chapters_queries

def generate_ebook():
    """
    Gera o ebook de forma sequencial executando agente para cada capítulo.
    """
    ebook_content = {
        "title": "Autoconhecimento e Inteligência Emocional",
        "sections": []
    }
    
    # Obtém queries para todos os capítulos
    chapters_queries = get_all_chapters_queries()
    
    print("\n" + "="*60)
    print(f"Gerando {len(chapters_queries)} capítulos do ebook")
    print("="*60)
    
    for idx, (chapter_name, query) in enumerate(chapters_queries, 1):
        print(f"\n[{idx}/{len(chapters_queries)}] Gerando: {chapter_name}")
        print("-" * 60)
        
        # Executa agente com query baseada no BRD
        response = writer_agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        
        # Extrai conteúdo da resposta
        content = response.get("messages", [])
        if content and isinstance(content, list):
            # Última mensagem é a resposta do agent
            chapter_content = content[-1].get("content", str(content[-1]))
        else:
            chapter_content = str(response)
        
        ebook_content["sections"].append({
            "chapter": chapter_name,
            "content": chapter_content
        })
        
        print(f"✓ {chapter_name} concluída")
        
        if idx < len(chapters_queries):
            print("\nAguardando 2 segundos antes do próximo capítulo...")
            time.sleep(2)
    
    return ebook_content

def save_ebook(content: dict, output_path: str = "result/ebook.md"):
    """
    Salva o ebook gerado em formato Markdown.
    
    Args:
        content: Dicionário com conteúdo do ebook
        output_path: Caminho para salvar o arquivo
    """
    import os
    
    # Cria diretório se não existir
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# {content['title']}\n\n")
        
        for section in content["sections"]:
            f.write(f"## {section['chapter']}\n\n")
            f.write(f"{section['content']}\n\n")
    
    print(f"\n✓ Ebook salvo em: {output_path}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Gerando ebook com LangChain 1.0+")
    print("="*60)
    
    # Gera o ebook
    ebook = generate_ebook()
    
    # Salva resultado
    save_ebook(ebook)
    
    print("\n" + "="*60)
    print("Ebook gerado com sucesso!")
    print("="*60)
    print(f"\nCapítulos gerados: {len(ebook['sections'])}")
    for section in ebook["sections"]:
        print(f"  ✓ {section['chapter']}")