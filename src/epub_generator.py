"""EPUB Generator - Converts markdown to EPUB3 preserving full content.

This module provides functionality to convert Markdown files
to EPUB3 format with complete content and formatting preservation.
"""

import os
import re
import uuid
import zipfile
from pathlib import Path
from datetime import datetime

from ebooklib import epub

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False


def extract_chapters_from_markdown(markdown_content: str) -> list[dict]:
    """
    Extract chapters from markdown content split by h1 headers.
    
    Args:
        markdown_content: Full markdown text to extract chapters from
    
    Returns:
        list[dict]: List of chapters with title and content keys
    """
    chapters = []
    
    # Split by h1 headers (^# )
    parts = re.split(r'^# ', markdown_content, flags=re.MULTILINE)
    
    # First part is usually empty or preamble
    if parts and parts[0].strip():
        chapters.append({
            'title': 'Introduction',
            'content': parts[0].strip()
        })
    
    # Process remaining parts as chapters
    for part in parts[1:]:
        if not part.strip():
            continue
        
        lines = part.strip().split('\n', 1)
        title = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ''
        
        chapters.append({
            'title': title,
            'content': content
        })
    
    return chapters


def markdown_to_html(markdown_text: str) -> str:
    """
    Convert markdown text to HTML using markdown library.
    
    Args:
        markdown_text: Markdown formatted text
    
    Returns:
        str: HTML converted from markdown
    """
    if not HAS_MARKDOWN:
        # Fallback to simple conversion if markdown library not available
        return _simple_markdown_to_html(markdown_text)
    
    # Use markdown library with extensions for better formatting
    extensions = [
        'extra',        # Tables, footnotes, strikethrough
        'codehilite',   # Code highlighting
        'toc',          # Table of contents
        'nl2br',        # Newline to break
    ]
    
    html = markdown.markdown(markdown_text, extensions=extensions)
    return html


def _simple_markdown_to_html(text: str) -> str:
    """
    Fallback markdown to HTML conversion using regex.
    
    Args:
        text: Markdown text
    
    Returns:
        str: Basic HTML conversion
    """
    html = text
    
    # Code blocks
    html = re.sub(
        r'```(.*?)\n(.*?)\n```',
        r'<pre><code class="\1">\2</code></pre>',
        html,
        flags=re.DOTALL
    )
    
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Bold
    html = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', html)
    
    # Italic
    html = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', html)
    html = re.sub(r'_([^_]+)_', r'<em>\1</em>', html)
    
    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Lists
    html = re.sub(r'^\- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    
    # Line breaks
    html = html.replace('\n\n', '</p><p>')
    html = f'<p>{html}</p>'
    
    return html


def create_epub_chapter(title: str, content_html: str) -> epub.EpubHtml:
    """
    Create an EPUB chapter from HTML content.
    
    Args:
        title: Chapter title
        content_html: HTML content of chapter
    
    Returns:
        epub.EpubHtml: EPUB chapter object
    """
    chapter = epub.EpubHtml()
    chapter.title = title
    chapter.file_name = f'chap_{uuid.uuid4().hex[:8]}.xhtml'
    
    # Add title as h1 and then content
    chapter.content = f'<h1>{title}</h1>\n{content_html}'
    
    return chapter


def generate_epub_from_markdown(
    markdown_file_path: str,
    output_file_path: str,
    metadata: dict = None
) -> bool:
    """
    Generate EPUB file from markdown content.
    
    Args:
        markdown_file_path: Path to markdown file
        output_file_path: Path where EPUB will be saved
        metadata: Dictionary with title, author, etc.
    
    Returns:
        bool: True if successful, False otherwise
    """
    metadata = metadata or {}
    
    try:
        # Read markdown file
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Extract chapters
        chapters_data = extract_chapters_from_markdown(markdown_content)
        
        if not chapters_data:
            return False
        
        # Create EPUB book
        book = epub.EpubBook()
        
        # Set metadata
        book.set_identifier(metadata.get('identifier', str(uuid.uuid4())))
        book.set_title(metadata.get('title', 'Untitled'))
        book.set_language(metadata.get('language', 'pt-BR'))
        
        # Add author
        if 'author' in metadata:
            book.add_author(metadata['author'])
        
        # Convert chapters and add to book
        chapters = []
        for chapter_data in chapters_data:
            # Convert markdown to HTML
            chapter_html = markdown_to_html(chapter_data['content'])
            
            # Create EPUB chapter
            chapter = create_epub_chapter(
                chapter_data['title'],
                chapter_html
            )
            
            book.add_item(chapter)
            chapters.append(chapter)
        
        # Add navigation files
        book.spine = ['nav'] + chapters
        book.toc = chapters
        
        # Add required EPUB files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # Create directories if needed
        output_path = Path(output_file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write EPUB
        epub.write_epub(output_file_path, book, {})
        
        return True
    
    except Exception as e:
        print(f"Error generating EPUB: {str(e)}")
        return False


def validate_epub(epub_path: str) -> bool:
    """
    Validate that EPUB file is properly formatted.
    
    Args:
        epub_path: Path to EPUB file to validate
    
    Returns:
        bool: True if valid EPUB, False otherwise
    """
    try:
        with zipfile.ZipFile(epub_path, 'r') as zip_ref:
            # Check for required EPUB files
            required_files = ['mimetype', 'META-INF/container.xml']
            
            for required_file in required_files:
                if required_file not in zip_ref.namelist():
                    return False
        
        return True
    
    except (zipfile.BadZipFile, Exception):
        return False
