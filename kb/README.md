# Knowledge Base (KB) Directory

This directory serves as a local knowledge base for RAG (Retrieval-Augmented Generation) operations. All Markdown (`.md`) files placed in this directory will be ingested into Supabase pgvector for semantic search and retrieval.

## How It Works

1. **Drop Markdown Files**: Place any `.md` files anywhere within the `kb/` directory or its subdirectories
2. **Run Ingestion**: Execute the ingestion script to process and index the files
3. **Automatic Processing**: The script will:
   - Scan all `.md` files in `kb/`
   - Split documents into chunks (preserving heading context)
   - Generate embeddings using OpenAI
   - Store in Supabase tables: `rag_documents` and `rag_chunks`
   - Track file changes via MD5 hashes to avoid duplicate processing

## Quick Start

### Prerequisites

1. Install required dependencies:
```bash
pip install openai supabase tiktoken
```

2. Set up environment variables in your `.env` file:
```bash
# Required
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_api_key
OPENAI_API_KEY=your_openai_api_key

# Optional (with defaults)
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
RAG_EMBEDDING_DIM=1536
RAG_KB_MD_GLOB=kb/**/*.md
```

### Basic Usage

Ingest all Markdown files in the kb/ directory:
```bash
python kb/ingest_md.py
```

### Command Line Options

#### Dry Run Mode
Preview what would be ingested without actually writing to the database:
```bash
python kb/ingest_md.py --dry-run
```

#### Limit Files
Process only the first N files (useful for testing):
```bash
python kb/ingest_md.py --limit 5
```

#### Force Reindex
Regenerate embeddings for all files, even if they haven't changed:
```bash
python kb/ingest_md.py --reindex
```

#### Custom Chunking
Adjust chunk size and overlap:
```bash
python kb/ingest_md.py --chunk-size 1000 --chunk-overlap 100
```

#### Custom Pattern
Use a different glob pattern:
```bash
python kb/ingest_md.py --pattern "docs/**/*.md"
```

#### Combined Options
```bash
python kb/ingest_md.py --dry-run --limit 1 --chunk-size 256
```

## Database Schema

The ingestion script expects two tables in Supabase:

### rag_documents
Stores the original documents and metadata.

```sql
CREATE TABLE rag_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_path TEXT NOT NULL UNIQUE,
    content TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### rag_chunks
Stores individual chunks with embeddings.

```sql
CREATE TABLE rag_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES rag_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536),  -- Adjust dimension as needed
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX ON rag_chunks USING ivfflat (embedding vector_cosine_ops);
```

## Chunking Strategy

The ingestion script uses intelligent chunking:

1. **Heading-Based Splitting**: Documents are first split by Markdown headings (`#`, `##`, etc.)
2. **Token-Aware Chunking**: Each section is further split to respect token limits
3. **Context Preservation**: Each chunk includes its heading context
4. **Overlap**: Chunks have configurable overlap to maintain continuity

Default settings:
- Chunk size: 512 tokens
- Overlap: 50 tokens
- Encoding: cl100k_base (GPT-3.5/4 tokenizer)

## Verifying Ingestion

After running the ingestion script, you can verify the data in Supabase:

### Check Documents
```sql
SELECT id, source_path, content_hash, metadata->>'chunk_count' as chunks, created_at
FROM rag_documents
ORDER BY created_at DESC;
```

### Check Chunks
```sql
SELECT d.source_path, c.chunk_index, c.metadata->>'title' as title, 
       LENGTH(c.content) as content_length, c.metadata->>'tokens' as tokens
FROM rag_chunks c
JOIN rag_documents d ON c.document_id = d.id
ORDER BY d.source_path, c.chunk_index;
```

### Count Statistics
```sql
SELECT 
    COUNT(DISTINCT id) as total_documents,
    (SELECT COUNT(*) FROM rag_chunks) as total_chunks,
    (SELECT AVG((metadata->>'chunk_count')::int) FROM rag_documents) as avg_chunks_per_doc
FROM rag_documents;
```

## Retrieval

To retrieve relevant chunks for a query, you can use the existing `rag/retrieve.py` script (if available) or create a simple retrieval function:

```python
from openai import OpenAI
from supabase import create_client
import os

# Initialize clients
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# Generate query embedding
query = "Your search query here"
response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)
query_embedding = response.data[0].embedding

# Search for similar chunks
result = supabase.rpc(
    'match_chunks',  # You'll need to create this function in Supabase
    {
        'query_embedding': query_embedding,
        'match_threshold': 0.7,
        'match_count': 5
    }
).execute()

# Display results
for chunk in result.data:
    print(f"Document: {chunk['source_path']}")
    print(f"Score: {chunk['similarity']}")
    print(f"Content: {chunk['content'][:200]}...")
    print("-" * 80)
```

## File Organization

You can organize your knowledge base files in any structure within `kb/`:

```
kb/
├── README.md (this file)
├── ingest_md.py (ingestion script)
├── chunker.py (chunking utilities)
├── .gitkeep (ensures kb/ exists in git)
├── product/
│   ├── features.md
│   └── roadmap.md
├── guides/
│   ├── quickstart.md
│   └── advanced.md
└── reference/
    └── api.md
```

## Duplicate Detection

The script uses MD5 hashing to detect when files have changed:

- **First Run**: All files are ingested
- **Subsequent Runs**: Only modified files are reprocessed
- **Force Reindex**: Use `--reindex` flag to reprocess all files

## Troubleshooting

### Missing Dependencies
```bash
pip install openai supabase tiktoken
```

### Environment Variables Not Set
Ensure your `.env` file contains all required variables, or set them explicitly:
```bash
export SUPABASE_URL="your_url"
export SUPABASE_KEY="your_key"
export OPENAI_API_KEY="your_key"
```

### Database Tables Don't Exist
Create the required tables using the SQL schema provided above.

### Embedding Dimension Mismatch
Ensure `RAG_EMBEDDING_DIM` matches your Supabase vector column dimension:
- text-embedding-3-small: 1536 dimensions (default)
- text-embedding-3-large: 3072 dimensions
- text-embedding-ada-002: 1536 dimensions

### Token Counting Issues
If `tiktoken` is not available, the chunker falls back to word-based approximation. For best results, install tiktoken:
```bash
pip install tiktoken
```

## Best Practices

1. **Organize by Topic**: Use subdirectories to organize related documents
2. **Use Clear Headings**: Markdown headings improve chunking quality
3. **Keep Chunks Focused**: Aim for 300-800 tokens per chunk for best retrieval
4. **Test First**: Use `--dry-run` to preview changes
5. **Incremental Updates**: The script automatically detects changes, no need to reindex everything
6. **Monitor Costs**: Each file generates OpenAI API calls for embeddings

## Example Workflow

1. Add a new markdown file:
```bash
echo "# API Documentation\n\nThis is my API documentation..." > kb/api-docs.md
```

2. Preview ingestion:
```bash
python kb/ingest_md.py --dry-run
```

3. Ingest the file:
```bash
python kb/ingest_md.py
```

4. Verify in Supabase or query via your RAG system

## Maintenance

### Removing Documents
To remove a document from the knowledge base:
1. Delete the markdown file from `kb/`
2. Manually delete from Supabase (chunks will cascade delete):
```sql
DELETE FROM rag_documents WHERE source_path = 'kb/path/to/file.md';
```

### Updating Documents
Simply edit the markdown file and rerun the ingestion script. The script will detect changes via MD5 hash and update the database automatically.

### Bulk Reindexing
If you change embedding models or dimensions, reindex all files:
```bash
python kb/ingest_md.py --reindex
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the command help: `python kb/ingest_md.py --help`
3. Check Supabase logs for database errors
4. Verify OpenAI API key and quota
