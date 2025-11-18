#!/usr/bin/env python3
"""
Knowledge Base Markdown Ingestion Script

Scans kb/**/*.md files, chunks them, generates embeddings using OpenAI,
and upserts them into Supabase tables (rag_documents and rag_chunks).

Features:
- Duplicate detection via MD5 hashing
- Dry-run mode to preview without writing
- Limit mode to ingest only first N files
- Reindex mode to force regeneration of embeddings
- Clear logging output

Usage:
    python kb/ingest_md.py [--dry-run] [--limit N] [--reindex]
"""

import os
import sys
import glob
import hashlib
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Install with: pip install openai")
    sys.exit(1)

try:
    from supabase import create_client, Client
except ImportError:
    print("Error: supabase package not installed. Install with: pip install supabase")
    sys.exit(1)

# Import our chunker
try:
    from chunker import chunk_markdown_file
except ImportError:
    # Try relative import
    try:
        from .chunker import chunk_markdown_file
    except ImportError:
        print("Error: Could not import chunker module")
        sys.exit(1)


class KnowledgeBaseIngestor:
    """Handles ingestion of Markdown files into Supabase RAG tables."""
    
    def __init__(
        self,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        embedding_model: Optional[str] = None,
        embedding_dim: Optional[int] = None,
        dry_run: bool = False
    ):
        """
        Initialize the ingestor.
        
        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase API key
            openai_api_key: OpenAI API key
            embedding_model: OpenAI embedding model name
            embedding_dim: Embedding dimension
            dry_run: If True, only preview without writing
        """
        self.dry_run = dry_run
        
        # Load environment variables
        self.supabase_url = supabase_url or os.getenv('SUPABASE_URL')
        self.supabase_key = supabase_key or os.getenv('SUPABASE_KEY')
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.embedding_model = embedding_model or os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-small')
        self.embedding_dim = embedding_dim or int(os.getenv('RAG_EMBEDDING_DIM', '1536'))
        
        # Initialize clients
        if not self.dry_run:
            if not self.supabase_url or not self.supabase_key:
                raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required")
            
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Statistics
        self.stats = {
            'files_scanned': 0,
            'files_added': 0,
            'files_skipped': 0,
            'files_updated': 0,
            'chunks_created': 0,
            'errors': 0
        }
    
    def compute_file_hash(self, file_path: str) -> str:
        """Compute MD5 hash of file content."""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI."""
        if self.dry_run:
            # Return dummy embedding in dry-run mode
            return [0.0] * self.embedding_dim
        
        try:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")
    
    def document_exists(self, file_path: str, content_hash: str) -> Optional[Dict[str, Any]]:
        """Check if document already exists in database."""
        if self.dry_run:
            return None
        
        try:
            result = self.supabase.table('rag_documents').select('*').eq('source_path', file_path).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            print(f"Warning: Could not check document existence: {str(e)}")
            return None
    
    def upsert_document(
        self,
        file_path: str,
        content: str,
        content_hash: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Upsert document to rag_documents table.
        
        Returns:
            Document ID if successful, None otherwise
        """
        if self.dry_run:
            print(f"  [DRY-RUN] Would upsert document: {file_path}")
            return "dry-run-doc-id"
        
        try:
            doc_data = {
                'source_path': file_path,
                'content': content,
                'content_hash': content_hash,
                'metadata': metadata or {},
                'updated_at': datetime.utcnow().isoformat()
            }
            
            # Try to find existing document
            existing = self.document_exists(file_path, content_hash)
            
            if existing:
                # Update existing document
                result = self.supabase.table('rag_documents').update(doc_data).eq('id', existing['id']).execute()
                if result.data:
                    return result.data[0]['id']
            else:
                # Insert new document
                doc_data['created_at'] = datetime.utcnow().isoformat()
                result = self.supabase.table('rag_documents').insert(doc_data).execute()
                if result.data:
                    return result.data[0]['id']
            
            return None
        except Exception as e:
            raise Exception(f"Failed to upsert document: {str(e)}")
    
    def delete_document_chunks(self, document_id: str):
        """Delete all chunks for a document."""
        if self.dry_run:
            print(f"  [DRY-RUN] Would delete chunks for document: {document_id}")
            return
        
        try:
            self.supabase.table('rag_chunks').delete().eq('document_id', document_id).execute()
        except Exception as e:
            print(f"Warning: Could not delete old chunks: {str(e)}")
    
    def insert_chunk(
        self,
        document_id: str,
        chunk_index: int,
        content: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Insert a chunk into rag_chunks table."""
        if self.dry_run:
            print(f"  [DRY-RUN] Would insert chunk {chunk_index} ({len(content)} chars)")
            return
        
        try:
            chunk_data = {
                'document_id': document_id,
                'chunk_index': chunk_index,
                'content': content,
                'embedding': embedding,
                'metadata': metadata or {},
                'created_at': datetime.utcnow().isoformat()
            }
            
            self.supabase.table('rag_chunks').insert(chunk_data).execute()
        except Exception as e:
            raise Exception(f"Failed to insert chunk {chunk_index}: {str(e)}")
    
    def ingest_file(
        self,
        file_path: str,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        force_reindex: bool = False
    ) -> bool:
        """
        Ingest a single Markdown file.
        
        Args:
            file_path: Path to the markdown file
            chunk_size: Target chunk size in tokens
            chunk_overlap: Overlap size in tokens
            force_reindex: If True, regenerate embeddings even if file unchanged
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"\nProcessing: {file_path}")
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Compute hash
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            
            # Check if document already exists
            if not force_reindex:
                existing = self.document_exists(file_path, content_hash)
                if existing and existing.get('content_hash') == content_hash:
                    print(f"  ⏭️  Skipped (unchanged): {file_path}")
                    self.stats['files_skipped'] += 1
                    return True
            
            # Chunk the document
            print(f"  📄 Chunking document...")
            chunks = chunk_markdown_file(
                content,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                preserve_context=True
            )
            print(f"  ✂️  Created {len(chunks)} chunks")
            
            # Prepare metadata
            metadata = {
                'filename': os.path.basename(file_path),
                'relative_path': file_path,
                'chunk_count': len(chunks),
                'chunk_size': chunk_size,
                'chunk_overlap': chunk_overlap
            }
            
            # Upsert document
            print(f"  💾 Upserting document...")
            document_id = self.upsert_document(file_path, content, content_hash, metadata)
            if not document_id:
                print(f"  ❌ Failed to upsert document")
                self.stats['errors'] += 1
                return False
            
            # Delete old chunks if updating
            if not self.dry_run:
                self.delete_document_chunks(document_id)
            
            # Generate embeddings and insert chunks
            print(f"  🔢 Generating embeddings...")
            for idx, chunk in enumerate(chunks):
                try:
                    embedding = self.get_embedding(chunk['content'])
                    
                    chunk_metadata = {
                        'title': chunk.get('title', ''),
                        'level': chunk.get('level', 0),
                        'tokens': chunk.get('tokens', 0),
                        'chunk_id': chunk.get('chunk_id', idx)
                    }
                    
                    self.insert_chunk(
                        document_id,
                        idx,
                        chunk['content'],
                        embedding,
                        chunk_metadata
                    )
                    
                    if not self.dry_run and (idx + 1) % 10 == 0:
                        print(f"    Progress: {idx + 1}/{len(chunks)} chunks processed")
                
                except Exception as e:
                    print(f"  ⚠️  Error processing chunk {idx}: {str(e)}")
                    self.stats['errors'] += 1
            
            self.stats['chunks_created'] += len(chunks)
            
            if existing:
                print(f"  ✅ Updated: {file_path} ({len(chunks)} chunks)")
                self.stats['files_updated'] += 1
            else:
                print(f"  ✅ Added: {file_path} ({len(chunks)} chunks)")
                self.stats['files_added'] += 1
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {str(e)}")
            self.stats['errors'] += 1
            return False
    
    def ingest_directory(
        self,
        glob_pattern: str,
        limit: Optional[int] = None,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        force_reindex: bool = False
    ):
        """
        Ingest all markdown files matching the glob pattern.
        
        Args:
            glob_pattern: Glob pattern for finding files (e.g., 'kb/**/*.md')
            limit: Maximum number of files to process
            chunk_size: Target chunk size in tokens
            chunk_overlap: Overlap size in tokens
            force_reindex: If True, regenerate embeddings for all files
        """
        print(f"{'='*60}")
        print(f"Knowledge Base Ingestion")
        print(f"{'='*60}")
        print(f"Mode: {'DRY-RUN' if self.dry_run else 'LIVE'}")
        print(f"Pattern: {glob_pattern}")
        print(f"Embedding Model: {self.embedding_model}")
        print(f"Embedding Dimension: {self.embedding_dim}")
        print(f"Chunk Size: {chunk_size} tokens")
        print(f"Chunk Overlap: {chunk_overlap} tokens")
        if limit:
            print(f"Limit: {limit} files")
        if force_reindex:
            print(f"Force Reindex: Yes")
        print(f"{'='*60}\n")
        
        # Find all matching files
        files = sorted(glob.glob(glob_pattern, recursive=True))
        
        if not files:
            print(f"⚠️  No files found matching pattern: {glob_pattern}")
            return
        
        print(f"Found {len(files)} markdown files\n")
        
        # Apply limit if specified
        if limit and limit > 0:
            files = files[:limit]
            print(f"Processing first {len(files)} files due to --limit flag\n")
        
        # Process each file
        for file_path in files:
            self.stats['files_scanned'] += 1
            self.ingest_file(
                file_path,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                force_reindex=force_reindex
            )
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"Ingestion Summary")
        print(f"{'='*60}")
        print(f"Files scanned:  {self.stats['files_scanned']}")
        print(f"Files added:    {self.stats['files_added']}")
        print(f"Files updated:  {self.stats['files_updated']}")
        print(f"Files skipped:  {self.stats['files_skipped']}")
        print(f"Chunks created: {self.stats['chunks_created']}")
        print(f"Errors:         {self.stats['errors']}")
        print(f"{'='*60}\n")


def main():
    """Main entry point for the ingestion script."""
    parser = argparse.ArgumentParser(
        description='Ingest Markdown files into Supabase RAG knowledge base',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python kb/ingest_md.py
  python kb/ingest_md.py --dry-run
  python kb/ingest_md.py --limit 5
  python kb/ingest_md.py --reindex
  python kb/ingest_md.py --dry-run --limit 1

Environment Variables:
  SUPABASE_URL              Supabase project URL (required)
  SUPABASE_KEY              Supabase API key (required)
  OPENAI_API_KEY            OpenAI API key (required)
  OPENAI_EMBEDDING_MODEL    Embedding model (default: text-embedding-3-small)
  RAG_EMBEDDING_DIM         Embedding dimension (default: 1536)
  RAG_KB_MD_GLOB            Glob pattern for files (default: kb/**/*.md)
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be ingested without writing to database'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        metavar='N',
        help='Ingest only first N files (for testing)'
    )
    
    parser.add_argument(
        '--reindex',
        action='store_true',
        help='Force regeneration of embeddings for existing files'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=512,
        metavar='SIZE',
        help='Target chunk size in tokens (default: 512)'
    )
    
    parser.add_argument(
        '--chunk-overlap',
        type=int,
        default=50,
        metavar='SIZE',
        help='Chunk overlap in tokens (default: 50)'
    )
    
    parser.add_argument(
        '--pattern',
        type=str,
        metavar='GLOB',
        help='Glob pattern for files (default: from RAG_KB_MD_GLOB or kb/**/*.md)'
    )
    
    args = parser.parse_args()
    
    # Get glob pattern
    glob_pattern = args.pattern or os.getenv('RAG_KB_MD_GLOB', 'kb/**/*.md')
    
    try:
        # Initialize ingestor
        ingestor = KnowledgeBaseIngestor(dry_run=args.dry_run)
        
        # Run ingestion
        ingestor.ingest_directory(
            glob_pattern=glob_pattern,
            limit=args.limit,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
            force_reindex=args.reindex
        )
        
        # Exit with error code if there were errors
        if ingestor.stats['errors'] > 0:
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
