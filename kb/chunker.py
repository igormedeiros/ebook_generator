"""
Reusable text chunking logic for Markdown documents.

This module provides utilities for splitting Markdown text into chunks
suitable for embedding and RAG operations. It supports:
- Heading-based splitting (respecting document structure)
- Token-aware chunking with configurable overlap
- Preservation of metadata and context
"""

import re
from typing import List, Dict, Any, Optional
import tiktoken


class MarkdownChunker:
    """Chunks Markdown documents intelligently based on structure and token limits."""
    
    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        encoding_name: str = "cl100k_base"
    ):
        """
        Initialize the chunker.
        
        Args:
            chunk_size: Target maximum tokens per chunk
            chunk_overlap: Number of tokens to overlap between chunks
            encoding_name: Tiktoken encoding to use for token counting
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        try:
            self.encoding = tiktoken.get_encoding(encoding_name)
        except Exception:
            # Fallback to a simple word-based approximation if tiktoken fails
            self.encoding = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self.encoding:
            return len(self.encoding.encode(text))
        else:
            # Rough approximation: 1 token ≈ 0.75 words
            return int(len(text.split()) * 1.33)
    
    def split_by_headings(self, text: str) -> List[Dict[str, Any]]:
        """
        Split Markdown text by headings, preserving hierarchy.
        
        Returns:
            List of sections with metadata including heading level and title
        """
        # Pattern to match markdown headings (# through ######)
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        
        sections = []
        current_section = {
            'level': 0,
            'title': '',
            'content': '',
            'start_pos': 0
        }
        
        lines = text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            match = heading_pattern.match(line)
            
            if match:
                # Save previous section if it has content
                if current_section['content'].strip():
                    sections.append(current_section.copy())
                
                # Start new section
                level = len(match.group(1))
                title = match.group(2).strip()
                current_section = {
                    'level': level,
                    'title': title,
                    'content': '',
                    'start_pos': i
                }
            else:
                # Add line to current section
                current_section['content'] += line + '\n'
            
            i += 1
        
        # Add final section
        if current_section['content'].strip():
            sections.append(current_section)
        
        # If no headings found, treat entire text as one section
        if not sections:
            sections.append({
                'level': 0,
                'title': '',
                'content': text,
                'start_pos': 0
            })
        
        return sections
    
    def chunk_section(
        self,
        section: Dict[str, Any],
        preserve_context: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Chunk a single section into token-sized pieces with overlap.
        
        Args:
            section: Section dict with 'content', 'title', 'level'
            preserve_context: Whether to prepend heading context to each chunk
            
        Returns:
            List of chunk dicts with content and metadata
        """
        content = section['content'].strip()
        
        # Build context prefix if requested
        context_prefix = ""
        if preserve_context and section['title']:
            context_prefix = f"{'#' * section['level']} {section['title']}\n\n"
        
        # Count tokens in context
        context_tokens = self.count_tokens(context_prefix) if context_prefix else 0
        available_tokens = self.chunk_size - context_tokens
        
        if available_tokens < 50:
            # Not enough room for content after context
            available_tokens = self.chunk_size
            context_prefix = ""
        
        chunks = []
        
        # Split content into paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        current_chunk = ""
        current_tokens = 0
        
        for para in paragraphs:
            para_tokens = self.count_tokens(para)
            
            # If single paragraph exceeds limit, split it further
            if para_tokens > available_tokens:
                # Save current chunk if not empty
                if current_chunk:
                    chunks.append({
                        'content': context_prefix + current_chunk,
                        'title': section['title'],
                        'level': section['level'],
                        'tokens': self.count_tokens(context_prefix + current_chunk)
                    })
                    current_chunk = ""
                    current_tokens = 0
                
                # Split large paragraph by sentences or words
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sentence in sentences:
                    sentence_tokens = self.count_tokens(sentence)
                    
                    if current_tokens + sentence_tokens > available_tokens:
                        if current_chunk:
                            chunks.append({
                                'content': context_prefix + current_chunk,
                                'title': section['title'],
                                'level': section['level'],
                                'tokens': self.count_tokens(context_prefix + current_chunk)
                            })
                        
                        # Start new chunk with overlap
                        if chunks and self.chunk_overlap > 0:
                            # Get last N tokens from previous chunk for overlap
                            overlap_text = self._get_last_tokens(current_chunk, self.chunk_overlap)
                            current_chunk = overlap_text + " " + sentence
                            current_tokens = self.count_tokens(overlap_text) + sentence_tokens
                        else:
                            current_chunk = sentence
                            current_tokens = sentence_tokens
                    else:
                        current_chunk += " " + sentence if current_chunk else sentence
                        current_tokens += sentence_tokens
            else:
                # Normal paragraph fits or can be added
                if current_tokens + para_tokens > available_tokens:
                    # Save current chunk
                    if current_chunk:
                        chunks.append({
                            'content': context_prefix + current_chunk,
                            'title': section['title'],
                            'level': section['level'],
                            'tokens': self.count_tokens(context_prefix + current_chunk)
                        })
                    
                    # Start new chunk with overlap
                    if chunks and self.chunk_overlap > 0:
                        overlap_text = self._get_last_tokens(current_chunk, self.chunk_overlap)
                        current_chunk = overlap_text + "\n\n" + para
                        current_tokens = self.count_tokens(overlap_text) + para_tokens
                    else:
                        current_chunk = para
                        current_tokens = para_tokens
                else:
                    current_chunk += "\n\n" + para if current_chunk else para
                    current_tokens += para_tokens
        
        # Add final chunk
        if current_chunk:
            chunks.append({
                'content': context_prefix + current_chunk,
                'title': section['title'],
                'level': section['level'],
                'tokens': self.count_tokens(context_prefix + current_chunk)
            })
        
        return chunks
    
    def _get_last_tokens(self, text: str, max_tokens: int) -> str:
        """Extract approximately the last N tokens from text."""
        if not text:
            return ""
        
        if self.encoding:
            tokens = self.encoding.encode(text)
            if len(tokens) <= max_tokens:
                return text
            overlap_tokens = tokens[-max_tokens:]
            return self.encoding.decode(overlap_tokens)
        else:
            # Word-based approximation
            words = text.split()
            approx_words = int(max_tokens * 0.75)
            return ' '.join(words[-approx_words:])
    
    def chunk_markdown(
        self,
        text: str,
        preserve_context: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Main method to chunk entire Markdown document.
        
        Args:
            text: Markdown text to chunk
            preserve_context: Whether to include heading context in chunks
            
        Returns:
            List of chunks with content and metadata
        """
        # Split by headings first
        sections = self.split_by_headings(text)
        
        # Chunk each section
        all_chunks = []
        for section in sections:
            section_chunks = self.chunk_section(section, preserve_context)
            all_chunks.extend(section_chunks)
        
        # Add sequential IDs
        for idx, chunk in enumerate(all_chunks):
            chunk['chunk_id'] = idx
        
        return all_chunks


def chunk_markdown_file(
    content: str,
    chunk_size: int = 512,
    chunk_overlap: int = 50,
    preserve_context: bool = True
) -> List[Dict[str, Any]]:
    """
    Convenience function to chunk a markdown file's content.
    
    Args:
        content: Markdown text content
        chunk_size: Target chunk size in tokens
        chunk_overlap: Overlap size in tokens
        preserve_context: Whether to preserve heading context
        
    Returns:
        List of chunk dictionaries
    """
    chunker = MarkdownChunker(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return chunker.chunk_markdown(content, preserve_context)
