"""
EPUB Generator - Converte markdown para EPUB3.

Este módulo fornece funcionalidade para converter arquivos Markdown
em formato EPUB3 com metadata apropriada.
"""

import os
import re
import uuid
from pathlib import Path
from datetime import datetime

from ebooklib import epub


def extract_chapters_from_markdown(markdown_content: str) -> list[dict]:
    """
    Extrai capítulos do conteúdo markdown.
    
    Procura por títulos de nível 2 (##) como delimitadores de capítulos.
    
    Args:
        markdown_content: Conteúdo markdown completo
    
    Returns:
        list[dict]: Lista de capítulos com 'title' e 'content'
    """
    chapters = []
    
    # Divide por ## (títulos de nível 2)
    parts = re.split(r'^## ', markdown_content, flags=re.MULTILINE)
    
    # Primeira parte é pré-conteúdo (intro, dedicatória, etc)
    if parts[0].strip():
        chapters.append({
            'title': 'Introdução',
            'content': parts[0].strip()
        })
    
    # Processa capítulos
    for part in parts[1:]:
        lines = part.split('\n', 1)
        if len(lines) >= 1:
            title = lines[0].strip()
            content = lines[1].strip() if len(lines) > 1 else ''
            
            if title and content:
                chapters.append({
                    'title': title,
                    'content': content
                })
    
    return chapters


def markdown_to_html(markdown_text: str) -> str:
    """
    Converte markdown simples para HTML básico.
    
    Args:
        markdown_text: Texto em markdown
    
    Returns:
        str: Conteúdo em HTML
    """
    html = markdown_text
    
    # Títulos
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)
    
    # Italic
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.*?)_', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # Linhas de código inline
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # Listas com -
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    html = re.sub(r'</li>\n<li>', r'</li><li>', html)
    
    # Parágrafos
    paragraphs = html.split('\n\n')
    paragraphs = [
        f'<p>{p}</p>' if p.strip() and not p.startswith('<')
        else p
        for p in paragraphs
    ]
    html = '\n\n'.join(paragraphs)
    
    # Linhas horizontais
    html = re.sub(r'^---+$', r'<hr/>', html, flags=re.MULTILINE)
    
    return html


def create_epub_chapter(title: str, content: str, chapter_num: int) -> epub.EpubHtml:
    """
    Cria um capítulo EPUB a partir de conteúdo markdown.
    
    Args:
        title: Título do capítulo
        content: Conteúdo em markdown
        chapter_num: Número do capítulo
    
    Returns:
        epub.EpubHtml: Objeto de capítulo EPUB
    """
    chapter = epub.EpubHtml()
    chapter.file_name = f'chap_{chapter_num:02d}.xhtml'
    chapter.title = title
    
    # Converte markdown para HTML
    html_content = markdown_to_html(content)
    
    # Envolve em estrutura básica XHTML
    chapter.content = f'''
    <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            {html_content}
        </body>
    </html>
    '''
    
    return chapter


def generate_epub_from_markdown(
    markdown_file: str,
    output_dir: str = "dist/",
    metadata: dict = None,
    title: str = None,
    author: str = None,
    language: str = "pt-BR",
) -> str:
    """
    Gera arquivo EPUB a partir de markdown.
    
    Args:
        markdown_file: Caminho para arquivo markdown
        output_dir: Diretório de saída
        metadata: Dicionário com metadata completa
        title: Título do livro
        author: Autor do livro
        language: Código de idioma (padrão: pt-BR)
    
    Returns:
        str: Caminho para arquivo EPUB gerado
    
    Raises:
        FileNotFoundError: Se arquivo markdown não existir
        ValueError: Se título ou autor não fornecido
    """
    # Validação
    if not os.path.exists(markdown_file):
        raise FileNotFoundError(f"Arquivo markdown não encontrado: {markdown_file}")
    
    # Usa metadata dict se fornecido, senão cria novo
    if metadata is None:
        metadata = {}
    
    # Extrai valores
    title = title or metadata.get('title', 'Untitled')
    author = author or metadata.get('author', 'Unknown Author')
    
    if not title or not author:
        raise ValueError("Título e autor são obrigatórios")
    
    # Lê conteúdo markdown
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Cria estrutura EPUB
    book = epub.EpubBook()
    
    # Define metadata básica (obrigatória)
    book.set_identifier(metadata.get('identifier', str(uuid.uuid4())))
    book.set_title(title)
    book.set_language(language)
    book.add_author(author)
    
    # Não adiciona metadata extra que causa problemas com ebooklib
    # A metadata básica é suficiente para gerar um EPUB válido
    
    # Extrai capítulos
    chapters = extract_chapters_from_markdown(markdown_content)
    
    # Cria capítulos EPUB
    epub_chapters = []
    for i, chapter_data in enumerate(chapters, 1):
        chapter = create_epub_chapter(
            chapter_data['title'],
            chapter_data['content'],
            i
        )
        book.add_item(chapter)
        epub_chapters.append(chapter)
    
    # Cria tabela de conteúdos
    book.toc = [c for c in epub_chapters]
    
    # Add default NCX and Nav files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define spine (ordem de leitura)
    book.spine = ['nav'] + epub_chapters
    
    # Cria diretório de saída se não existir
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Gera nome do arquivo EPUB
    output_file = os.path.join(output_dir, 'ebook.epub')
    
    # Escreve arquivo EPUB
    epub.write_epub(output_file, book, {})
    
    return output_file


def validate_epub(epub_file: str) -> bool:
    """
    Valida se arquivo EPUB existe e tem tamanho mínimo.
    
    Args:
        epub_file: Caminho para arquivo EPUB
    
    Returns:
        bool: True se válido, False caso contrário
    """
    if not os.path.exists(epub_file):
        return False
    
    file_size = os.path.getsize(epub_file)
    # Arquivo EPUB mínimo é cerca de 1KB, máximo esperado 50MB
    return 1000 < file_size < 50 * 1024 * 1024
