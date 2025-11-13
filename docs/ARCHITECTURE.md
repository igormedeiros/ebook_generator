# Technical Architecture – Automated eBook Generator

**Ebook Generator 1.0 - Technical Architecture Specification**

**Version**: 1.0  
**Last Updated**: November 12, 2025  

---

## 1. Stack and Integrations

### Backend
- **Language**: Python 3.11+
- **AI Orchestration**: LangChain 1.0+
- **AI Models**: 
  - Gemini 2.5 Flash (fast writing, temperature 0.7)
  - Gemini 2.5 Pro (deep research/RAG, temperature 0.3)

### Storage and Vectorization
- **Database**: Supabase
- **Vectorization**: pgvector extension
- **Retriever**: LangChain Retriever

### Conversion and Export
- **Markdown → HTML/DOCX/EPUB**: Pandoc 3.0+
- **Cover Generation**: API Integration (Banana or similar)
- **Publication**: Assistant for KDP (Kindle Direct Publishing)

---

## 2. Architectural Components

### 2.1 Configuration System (`specs/` and `input/`)

All pipeline parameters are externalized to YAML configuration files:

```
specs/
├── pipeline.yaml         # 9-stage parameter definitions (defaults + constraints)
├── config.yaml           # Portuguese strings, messages, labels
├── models.yaml           # Gemini model configuration
├── personas.yaml         # 10 review personas + 5 virtual readers
├── tools.yaml            # 30+ tool specifications
├── book.yaml             # Generated from input validation (gitignore)
└── README.md             # Configuration documentation

input/
└── book_input.yaml       # User-provided book specification
```

**Key Files**:

1. **input/book_input.yaml** - User-provided specification:
   - Mandatory: `topic`, `target_audience`, `word_count_target`
   - Optional: `transformation_promise`, `reading_level`, `stage_overrides`
   - Validated at pipeline start
   - User prompted interactively for missing/invalid fields
   
2. **specs/book.yaml** - Generated from input validation:
   - Merges `input/book_input.yaml` with `specs/pipeline.yaml` defaults
   - Applies stage-specific overrides
   - Ready for pipeline execution
   - Not committed (regenerated on each run)

3. **pipeline.yaml** - Parameters for each of 9 stages:
   - Word count targets, outline depth, persona activation, iteration cycles, export formats
   - Each stage has configurable parameters with types, defaults, ranges
   
4. **config.yaml** - Centralized Portuguese content:
   - 100+ messages (pipeline events, agent operations, validation results)
   - System prompts for agents
   - Table titles and icons
   
3. **models.yaml** - AI model configuration:
   - Gemini 2.5 Flash (0.7 temperature) for creative writing
   - Gemini 2.5 Pro (0.3 temperature) for research/RAG
   - API configuration and token limits
   
4. **personas.yaml** - Reviewer specifications:
   - 10 review personas with expertise areas and evaluation criteria
   - 5 virtual readers with focus areas
   - Feedback aggregation strategies and iteration settings
   
5. **tools.yaml** - Tool definitions:
   - 9 categories across 9 pipeline stages
   - 30+ tool specifications with parameters
   - Default values and constraints

### 2.2 Input Validator (`src/input_validator.py`)

Validates and converts user input to pipeline configuration:

```python
from src.input_validator import (
    validate_book_input,          # Validate input/book_input.yaml
    prompt_missing_fields,        # Prompt user for missing fields
    generate_book_config          # Generate specs/book.yaml
)
```

**Validation Flow**:

1. Load `input/book_input.yaml` (user-provided)
2. Check mandatory fields: `topic`, `target_audience`, `word_count_target`
3. Validate field types against `specs/pipeline.yaml` definitions
4. Validate ranges (e.g., word_count_target min/max)
5. If missing/invalid fields:
   - Display error message with field requirements
   - Prompt user interactively to provide missing values
   - Validate input again
6. Merge validated input with defaults from `specs/pipeline.yaml`
7. Generate `specs/book.yaml` (merged configuration)
8. Return validated config ready for pipeline execution

**Example Interactive Prompt**:

```
❌ Validação falhou - campos obrigatórios faltando:

📋 Campos Obrigatórios:
  • topic (string): Tópico principal do ebook
    Exemplo: "Python para Análise de Dados"
    
  • target_audience (string): Público-alvo
    Exemplo: "Cientistas de dados iniciantes"
    
  • word_count_target (integer): Contagem de palavras
    Range: 5000 - 100000
    Padrão: 15000

🔧 Preencha os campos abaixo:
topic: _
```

### 2.3 Configuration Module (`src/config.py`)

Provides unified interface for loading and accessing all configurations:

```python
from src.config import (
    get_config,              # Load any config section
    get_message,             # Load Portuguese messages
    get_pipeline_config,     # Load pipeline parameters
    get_models_config,       # Load model configuration
    get_personas_config,     # Load personas
    get_tools_config,        # Load tools
    get_logger,              # Get configured logger
    console,                 # Rich console for output
    print_panel,             # Display formatted panels
    print_table,             # Display formatted tables
    print_progress,          # Display progress bars
    setup_logging            # Configure logging with Rich
)
```

**Usage Examples**:

```python
# Get pipeline parameters
config = get_pipeline_config()
ideation_params = config['stages']['stage_1_ideation']['parameters']

# Get Portuguese message
msg = get_message('pipeline_start')  # "🚀 Iniciando pipeline..."

# Validate input and run pipeline
from src.input_validator import validate_book_input
book_config = validate_book_input()
result = run_ebook_pipeline(**book_config)

# Logging with Rich
logger = get_logger('my_module')
logger.info("Iniciando processamento")
logger.error("Erro detectado")

# Output with Rich
print_panel(
    title="Resultado",
    content="Conteúdo formatado",
    style="cyan"
)
```

### 2.4 MD Input Parser
```
Function: Interpret and validate .md file with specifications
Input: .md file with mandatory fields
  - numero_palavras: int
  - estilo_linguagem: str (empathetic, technical, informal)
  - nome_autor: str
  - publico_alvo: str (optional)
  - tom: str (optional)
  - complexidade: str (optional)
Output: Validated global configurations
Responsibility: Propagate configurations throughout the pipeline
```

### 2.5 Main Agents (9 + 10 Reviewers + 5 Virtual Readers + 1 Coordinator)

#### 1. Agent: Central Idea
- **Responsibility**: Generate book essence according to input/parameters
- **Input**: Topic, target audience, word count goal
- **Output**: Central idea, problem definition, transformation promise
- **Tools**: Knowledge base search, RAG context

#### 2. Agent: Title/Subtitle
- **Responsibility**: Research best-sellers and suggest winning title
- **Input**: Central idea, target audience
- **Output**: 3 Amazon-optimized title options
- **Tools**: Market research, SEO validation

#### 3. Agent: Structurer
- **Responsibility**: Create book template + chapters/sections
- **Input**: Central idea, title, word count goal
- **Output**: Hierarchical index with word distribution
- **Tools**: Outline generation, word count calculation

#### 4. Agent: Writer
- **Responsibility**: Write chapters with deep research context
- **Input**: Outline, chapter definitions, vectorized research from rag_external
- **Output**: Didactic chapters with research-backed content
- **Tools**: 
  - retrieve_rag_external_research() - Query vectorized research
  - retrieve_author_stories() - Query author narratives (already in DB)
  - retrieve_author_positioning() - Query author positioning (already in DB)
  - retrieve_author_vision() - Query author vision (already in DB)
  - format_markdown()
  - validate_content_quality()

#### 4A. Agent: Deep Research (NEW - Runs BEFORE Writer)
- **Responsibility**: Perform deep research for each chapter and vectorize results
- **Input**: Chapter definitions from Structure Agent
- **Output**: Vectorized research stored in rag_external table
- **Process**:
  1. For each chapter: Extract topic and learning objectives
  2. Query Context7 MCP Server for relevant knowledge bases
  3. Perform deep research using Gemini 2.5 Pro
  4. Generate embeddings using Gemini embeddings model
  5. Store vectorized results in rag_external with chapter_id and topic
- **Tools**:
  - query_context7_mcp() - Retrieve knowledge bases from Context7
  - perform_deep_research() - Use Gemini 2.5 Pro for analysis
  - vectorize_research() - Create embeddings with Gemini
  - store_in_rag_external() - Persist vectorized research
- **Execution**: Runs sequentially before Writer Agent in Stage 4

#### 5. Agent: Multiple Review
- **Responsibility**: Simulate specialized review personas (10 personas)
- **Personas**:
  - Editorial: Clarity, tone, flow
  - Technical: Code quality, conceptual precision
  - Empathy: Accessibility, emotional connection
  - Humor/Engagement: Lightness, interest
  - Compliance: LGPD, HIPAA, KDP
  - Stories & Didactics: Balances author narratives with pedagogy
  - Positioning: Validates author authority and market positioning
  - Vision & Opinions: Reviews author vision and opinions coherence
  - Examples & Exercises Code Reviewer (NEW): Executes and collects code for GitHub
  - Research & References Validator (NEW): Validates scientific credibility of sources
- **Input**: Raw chapters with embedded code examples and citations
- **Output**: Structured feedback by persona (10 perspectives)
- **RAG Integration**:
  - RAG Author Stories (for narrative balance evaluation)
  - RAG Positioning (for authority validation)
  - RAG Vision & Opinions (for philosophical coherence)
- **Code Review Process**:
  - Examples & Exercises Code Reviewer executes all code examples
  - Tests for errors and validates functionality
  - Collects working code to GitHub repository structure
  - Generates GitHub links for book references
- **Research Validation Process**:
  - Research & References Validator cross-checks all cited sources
  - Validates academic credibility and peer-review status
  - Checks data freshness and scientific consensus alignment
  - Flags and replaces non-credible sources
- **Loop**: Review cycle critical based on target audience, style, author identity, code execution, and research credibility

#### 6. Agent: Code
- **Responsibility**: Validate Python blocks in the book
- **Input**: Code blocks extracted from chapters
- **Output**: Validation report, correction suggestions
- **Tools**: Code execution, linter, formatter

#### 7. Agent: Style Editor
- **Responsibility**: Refine styles, headings, links, Markdown template
- **Input**: Reviewed chapters
- **Output**: Document with standardized formatting
- **Validations**: Heading hierarchy, consistency, accessibility

#### 8. Agent: Summary/Cover
- **Responsibility**: Generate dynamic summary and create cover
- **Input**: Final chapters, theme, target audience
- **Output**: 
  - Updated summary
  - Generated cover via API
  - Cover inserted in document
- **Tools**: Cover generation, design API

---

## 3. RAG Pipeline (Architecture)

### 3.1 Author Knowledge Base (Pre-loaded in Supabase)
```
Status: Already available in Supabase tables
- rag_author_stories: Personal narratives, experiences, memories
- rag_author_positioning: Market positioning, authority, niche differentiation
- rag_author_vision: Values, philosophy, worldview, opinions

These tables contain pre-ingested author knowledge and are referenced by:
- Writer: To incorporate author narratives organically
- Author Stories Reviewer: To validate narrative balance
- Author Positioning Reviewer: To validate positioning clarity
- Author Vision Reviewer: To validate philosophical coherence
```

### 3.2 External RAG - Deep Research Pipeline with Scientific Sources
```
Execution Flow:
1. Stage 3: Structure Agent creates hierarchical outline
   └─ Defines chapters and sections to be written

2. Stage 4A: Deep Research Agent (NEW - runs BEFORE writing)
   ├─ For each chapter: Query Context7 MCP Server
   ├─ Retrieve academic papers, books, studies, frameworks
   ├─ Sources include: peer-reviewed research, scientific data, authoritative texts
   ├─ Perform deep research using Gemini 2.5 Pro
   ├─ Vectorize research results with Gemini embeddings model
   └─ Tag with source metadata (credibility, publication date, author expertise)

3. Stage 4B: Vector Storage & Validation
   ├─ Store vectorized research in rag_external table
   ├─ Tag with chapter_id, topic, source, credibility metrics
   └─ Research & References Validator (Stage 5) verifies source quality

4. Stage 4C: Chapter Writing
   ├─ Writer Agent queries rag_external (vectorized research)
   ├─ Integrates research-backed content naturally into chapters
   ├─ Includes citations for all sources
   └─ Maintains author's voice while enhancing with verified research

5. Stage 5: Research & References Validator Review
   ├─ Cross-validates all cited sources
   ├─ Checks academic credibility and peer-review status
   ├─ Verifies scientific consensus alignment
   ├─ Flags outdated or non-credible sources
   └─ Suggests replacements for failed sources

Context7 MCP Server Integration:
- Provides semantic search across multiple vetted knowledge bases
- Returns top-k relevant documents with source metadata per chapter topic
- Retrieves: academic papers, books, data, industry reports, case studies
- Includes: author credentials, publication status, peer-review indicators
- Runs independently (not dependent on VS Code or Copilot)
- Executed directly by the Ebook Generator pipeline
```

### 3.3 Author RAG vs Research RAG (Clear Distinction)
```
AUTHOR RAG (rag_author_stories, rag_author_positioning, rag_author_vision)
- Pre-loaded: Ingested before pipeline execution
- Content: Author personal stories, positioning, vision & opinions
- Usage: By reviewers to validate author authenticity
- Retrieved by: Direct table queries (no vectorization needed)

EXTERNAL RESEARCH RAG (rag_external with scientific sources)
- Generated: During pipeline execution (Stage 4A)
- Content: Academic papers, books, studies, scientific data, frameworks
- Sources: Peer-reviewed research, authoritative texts, verified data
- Validation: Research & References Validator ensures credibility
- Retrieved by: Semantic vector search (vectorized with Gemini embeddings)
- Usage: By Writer Agent to enrich chapters with research-backed content
- Traceability: All sources cited in document with credibility indicators
```

### 3.4 Supabase Configuration
```sql
-- Table: rag_external (Research knowledge - vectorized during pipeline)
CREATE TABLE rag_external (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  embedding vector(1536),
  chapter_id VARCHAR(100),
  topic VARCHAR(255),
  source VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table: rag_author_stories (Pre-loaded - author personal narratives)
CREATE TABLE rag_author_stories (
  id BIGSERIAL PRIMARY KEY,
  story TEXT NOT NULL,
  embedding vector(1536),
  category VARCHAR(100),
  tags TEXT[],
  author_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table: rag_author_positioning (Pre-loaded - market positioning)
CREATE TABLE rag_author_positioning (
  id BIGSERIAL PRIMARY KEY,
  positioning_statement TEXT NOT NULL,
  embedding vector(1536),
  aspect VARCHAR(100),
  author_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table: rag_author_vision (Pre-loaded - values and philosophy)
CREATE TABLE rag_author_vision (
  id BIGSERIAL PRIMARY KEY,
  vision_or_opinion TEXT NOT NULL,
  embedding vector(1536),
  category VARCHAR(100),
  principle VARCHAR(255),
  author_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for vector search
CREATE INDEX ON rag_external USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON rag_author_stories USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON rag_author_positioning USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON rag_author_vision USING ivfflat (embedding vector_cosine_ops);
```

---

## 4. Execution Sequence (Flowchart)

```
```
InputMD 
  ↓
MD Parser (validation and configuration propagation)
  ↓
Central Idea (essence + promise)
  ↓
Title Subtitle (research + 3 options)
  ↓
Structurer (outline + word distribution + chapter definitions)
  ↓
Deep Research Agent (Stage 4A)
  ├─ For each chapter: Query Context7 MCP Server
  ├─ Retrieve academic papers, books, studies, scientific data
  ├─ Deep research using Gemini 2.5 Pro
  ├─ Vectorize results with Gemini embeddings model
  └─ Store in rag_external table with source metadata
  ↓
Writer (Stage 4B - chapters with research-backed content)
  ├─ Query rag_external (vectorized research)
  ├─ Integrate author narratives from rag_author_* tables
  ├─ Include citations for all sources
  ├─ Markdown formatting
  └─ Synthesis of research + author voice
  ↓
Multiple Review (10 personas)
  ├─ Editorial (clarity, tone, flow)
  ├─ Technical (code quality, precision)
  ├─ Empathy (accessibility, connection)
  ├─ Engagement (lightness, interest)
  ├─ Compliance (LGPD, HIPAA, KDP)
  ├─ Author Stories & Didactics (narrative balance)
  ├─ Author Positioning (authority, positioning)
  ├─ Author Vision & Opinions (values, philosophy)
  ├─ Examples & Exercises Code Reviewer (executes and collects code)
  └─ Research & References Validator (validates source credibility)
  ↓
═══════════════════════════════════════════════════════════
  CRITICAL READING & ITERATIVE REVISION (3 Cycles)
═══════════════════════════════════════════════════════════
  ↓
ITERATION 1: Critical Reading & Initial Revisions
  ├─ Curious Beginner (clarity, accessibility feedback)
  ├─ Technical Professional (technical accuracy feedback)
  ├─ Didactic Educator (pedagogical structure feedback)
  ├─ Domain Specialist (cross-disciplinary coherence feedback)
  ├─ Reflective Reader (emotional impact feedback)
  ├─ Feedback Aggregation & Prioritization (critical → nice-to-have)
  ├─ Revision: Address critical issues (comprehension, accuracy)
  ├─ Coordinator Validation: Confirm improvement quality
  └─ Output: Improved content (Iteration 1)
  ↓
ITERATION 2: Validation & Secondary Improvements
  ├─ Curious Beginner (verify clarity improvements)
  ├─ Technical Professional (confirm technical fixes)
  ├─ Didactic Educator (validate pedagogy enhancements)
  ├─ Domain Specialist (check domain coherence)
  ├─ Reflective Reader (assess engagement improvements)
  ├─ Feedback Aggregation: Secondary issues and refinements
  ├─ Revision: Address engagement and secondary improvements
  ├─ Coordinator Validation: Confirm progressive improvement
  └─ Output: Further improved content (Iteration 2)
  ↓
ITERATION 3: Final Polish & Publication Readiness
  ├─ Curious Beginner (final clarity validation)
  ├─ Technical Professional (final accuracy verification)
  ├─ Didactic Educator (final pedagogical validation)
  ├─ Domain Specialist (final coherence check)
  ├─ Reflective Reader (final engagement validation)
  ├─ Feedback Aggregation: Final polish and verification
  ├─ Revision: Address remaining refinements
  ├─ Coordinator Validation: Approve for publication
  └─ Output: Publication-ready content (Iteration 3)
  ↓
═══════════════════════════════════════════════════════════
  ↓
Code Agent (Python code block validation)
  ↓
Style Editor (Markdown formatting)
  ↓
Summary Cover (dynamic + design API)
  ↓
Final Converter (format export)
  ├─ HTML
  ├─ DOCX
  ├─ EPUB
  └─ JSON (metadata)
  ↓
Publication Agent (KDP compilation)```
  ├─ Metadata
  ├─ Synopsis
  ├─ Catalog sheet
  └─ Final files
  ↓
OUTPUT (eBook ready for KDP)
```

---

## 5. Gemini Model Roles

### Gemini 2.5 Flash (Fast Writing)
- **Temperature**: 0.7 (balanced creativity)
- **Primary Usage**:
  - Chapter writing
  - Reviews (all 8 personas)
  - Summary generation
  - Short and fast prompts
- **Characteristics**: Fast, creative, balanced

### Gemini 2.5 Pro (Deep Research)
- **Temperature**: 0.3 (focus on precision)
- **Primary Usage**:
  - External research (External RAG)
  - Author story/opinion ingestion
  - Author content vectorization
  - Factual validation
- **Characteristics**: Precise, deep, contextual

---

## 6. Token Flow and Optimization

### Strategy to Minimize Tokens
1. **Query Caching**: RAG results cached locally
2. **Deduplication**: Same query = same stored result
3. **Summaries**: Use summaries instead of full content
4. **Reduced Top-k**: top_k=3 instead of 10 for RAG
5. **Optimized Prompts**: Concise prompts without unnecessary information

### Usage Estimate
- **Per Chapter**: 500-1000 tokens
- **Multi-Persona Review**: 300-500 tokens
- **External RAG**: 200-400 tokens
- **Complete Pipeline (10 chapters)**: 10,000-20,000 tokens

---

## 7. Critical Observations

### Traceability
- Every input used is traceable in final document
- Clear source marking: external (RAG), author-owned (stories/opinions), or generated
- Automatic footnotes/citations for each RAG input

### Radical Personalization
- Ensure author content meshes with universal editorial result
- Author stories and opinions appear organically
- Balance between author voice and editorial quality

### Future Adaptations
- Internal structures allow adding new input types
- Extensible channel for new assets (images, videos, etc.)
- New research channels integrable without refactoring

---

## 8. External Dependencies

### Required APIs and Services
- **Google Gemini API**: For LLMs (Flash + Pro) and embeddings
- **Supabase API**: For storage and vector operations
- **Context7 MCP Server**: For semantic knowledge base retrieval (independent execution)
- **GitHub API** (optional): For automated repository creation and file management
- **Banana API** (or similar): For AI cover generation (optional)
- **Pandoc**: For format conversion (local installation)

### Context7 MCP Server
- **Purpose**: Provide semantic search across multiple knowledge bases for academic and scientific research
- **Execution**: Runs independently from VS Code and Copilot
- **Integration**: Called directly by Deep Research Agent in pipeline
- **Knowledge Bases**: Academic papers, books, studies, data repositories, industry reports
- **Functionality**:
  - Query multiple knowledge bases by topic
  - Return top-k relevant documents with source metadata
  - Include credibility indicators (peer-review status, author expertise, publication date)
  - Support for semantic similarity search
  - Used only during Stage 4A (Deep Research)

### GitHub Integration (Examples & Exercises Repository)
- **Purpose**: Manage code examples and exercises collected by Examples & Exercises Code Reviewer
- **Structure**:
  ```
  github_repo/
  ├── README.md (book info, setup instructions, prerequisites)
  ├── chapter_01/
  │   ├── example_1.py
  │   ├── example_2.py
  │   ├── example_3.py
  │   └── exercise_1.py
  ├── chapter_02/
  │   ├── example_1.py
  │   └── exercise_1.py
  ├── chapter_n/
  │   └── ...
  ├── requirements.txt (all Python dependencies)
  ├── setup.py (optional package setup)
  └── .gitignore
  ```
- **Automation**:
  - Examples & Exercises Code Reviewer collects tested code during review
  - Organize into chapter structure automatically
  - Generate README with setup instructions
  - Create GitHub links for book references
- **Purpose in Book**:
  - Links to complete runnable code examples
  - Readers can clone and experiment locally
  - Maintains code freshness and testability

### Environment Configuration
```bash
export GOOGLE_API_KEY="your-gemini-api-key"
export NEXT_PUBLIC_SUPABASE_URL="https://your-project.supabase.co"
export NEXT_PUBLIC_SUPABASE_ANON_KEY="your-supabase-key"
export CONTEXT7_SERVER_URL="http://localhost:8000"  # or production URL
export GITHUB_TOKEN="your-github-token"  # optional for repo automation
export BANANA_API_KEY="your-key"  # optional for cover
```

---

### Logging and Output Standards

All output must use logging and Rich formatting:

```python
from src.config import get_logger, console, print_panel

logger = get_logger('module_name')

# ✅ Logging (never use print)
logger.info("Pipeline iniciado")
logger.warning("Aviso importante")  
logger.error("Erro na execução")
logger.debug("Detalhes técnicos")

# ✅ Rich output
print_panel(
    title="Resultado da Revisão",
    content="Feedback dos personas",
    style="cyan"
)

# ❌ NEVER use print()
print("Resultado")  # Incorrect - use logging instead
```

**Logging Levels**:
- `logger.debug()` - Technical details and tracing
- `logger.info()` - Normal progress information
- `logger.warning()` - Warnings (e.g., outdated versions)
- `logger.error()` - Execution errors
- `logger.critical()` - Critical failures blocking continuation

**Rich Output Methods**:
- `print_panel(title, content, style)` - Display formatted panels
- `print_table(title, headers, rows, style)` - Display formatted tables
- `print_progress(total, description)` - Display progress bars
- `console.print()` - Direct Rich console output for structured data

### Parameter-Driven Architecture

Pipeline execution is fully parameterized from specs/:

```python
from src.main import run_ebook_pipeline
from src.input_validator import validate_book_input
from src.config import get_pipeline_config

# Option 1: Validate input/book_input.yaml and run
config = validate_book_input()
result = run_ebook_pipeline(**config['metadata'], **config['parameters'])

# Option 2: Use defaults from pipeline.yaml
result = run_ebook_pipeline(
    topic="Python para Análise",
    target_audience="Data Scientists",
    word_count_target=15000  # from pipeline.yaml default
)

# Option 3: Custom overrides via stage_overrides in input
config = validate_book_input()  # includes stage_overrides from input/book_input.yaml
result = run_ebook_pipeline(**config)
```
- Author personal data encrypted
- Compliance validated in Compliance Agent
- Retention policy: 6 months (customizable)

### HIPAA (Healthcare)
- Automatic medical disclaimer validation
- Alerts for sensitive health content
- Qualified review for medical content

### KDP Compliance
- Automatic format validation
- Metadata according to Amazon requirements
- Publishability test before export

---

## 10. Next Evolutions

### v1.1 (Q1 2025)
- [ ] Complete review loop (3 iterations)
- [ ] Simple dashboard for monitoring
- [ ] Detailed execution logging

### v1.2 (Q2 2025)
- [ ] REST API for remote execution
- [ ] Automatic KDP publishing
- [ ] Quality analytics per chapter

### v2.0 (Q3 2025)
- [ ] LangGraph for advanced orchestration
- [ ] Complete web UI
- [ ] Batch processing for multiple eBooks
- [ ] Multi-language

---

## 11. Component Diagram

```
┌─────────────────────────────────────────────────────┐
│        EBOOK GENERATOR 1.0 - ARCHITECTURE           │
└─────────────────────────────────────────────────────┘

INPUT LAYER
├── InputMD Parser
└── Config Validator

AGENT LAYER (9 Main + 10 Review + 5 Virtual Readers + 1 Coordinator)
├── Central Idea
├── Title/Subtitle
├── Structurer
├── Deep Research (Stage 4A)
├── Writer (Stage 4B)
├── Multiple Review (10 specialized personas)
├── Critical Reading (5 virtual readers - 3 iterations)
├── Code
├── Style Editor
└── Summary/Cover

RAG LAYER
├── External RAG (Gemini 2.5 Pro) - Research knowledge (generated)
├── Author RAG - 3 Knowledge Types (pre-loaded):
│   ├── Personal Stories (rag_author_stories)
│   ├── Market Positioning (rag_author_positioning)
│   └── Vision & Opinions (rag_author_vision)
├── Supabase Storage (4 vectorized tables)
└── LangChain Retriever

EXPORT LAYER
├── HTML Converter
├── DOCX Converter
├── EPUB Converter
└── JSON Metadata

PUBLICATION LAYER
└── KDP Assistant

LLM LAYER
├── Gemini 2.5 Flash (writing)
└── Gemini 2.5 Pro (research & analysis)
```

---

**Document Version**: 1.0  
**Last Updated**: November 12, 2025  
**Owner**: Igor Medeiros  
**Status**: Active

```
USER INPUT (topic, audience, word_count)
    ↓
┌─ ORCHESTRATOR (run_ebook_pipeline)
│
├─→ STAGE 1: IDEATION AGENT
│   └─ Define central idea, problem, audience, promise
│
├─→ STAGE 2: TITLE AGENT
│   └─ Generate 3 Amazon-optimized title options
│
├─→ STAGE 3: STRUCTURE AGENT
│   └─ Create hierarchical outline with chapter definitions
│
├─→ STAGE 4A: DEEP RESEARCH AGENT
│   └─ Query Context7 MCP Server, vectorize research, store in rag_external
│
├─→ STAGE 4B: WRITER AGENT
│   └─ Write chapters with research-backed content (uses rag_external)
│
├─→ STAGE 5: SPECIALIZED REVIEW (10 PERSONAS)
│   ├─→ TECHNICAL REVIEWER (code quality, versions)
│   ├─→ EDITORIAL REVIEWER (clarity, tone, flow)
│   ├─→ CONTENT STYLIST (formatting, structure)
│   ├─→ GOVERNANCE QA (compliance, metadata)
│   ├─→ ETHICS VALIDATOR (bias, disclaimers)
│   ├─→ AUTHOR STORIES & DIDACTICS (narrative balance, RAG Stories)
│   ├─→ AUTHOR POSITIONING (marketing authority, RAG Positioning)
│   ├─→ AUTHOR VISION & OPINIONS (values alignment, RAG Vision)
│   ├─→ EXAMPLES & EXERCISES CODE REVIEWER (executes code, collects for GitHub)
│   └─→ RESEARCH & REFERENCES VALIDATOR (source credibility validation)
│       └─ Aggregated feedback dict (10 perspectives)
│
├─→ STAGE 6: CRITICAL READING & ITERATIVE REVISION (3 CYCLES)
│   ├─→ ITERATION 1: Initial critical reading feedback & revision
│   │   ├─→ 5 virtual readers analyze independently
│   │   ├─→ Feedback aggregation & prioritization
│   │   ├─→ Revision addressing critical issues
│   │   └─→ Coordinator validation
│   ├─→ ITERATION 2: Secondary improvements & engagement enhancement
│   │   ├─→ 5 virtual readers re-analyze
│   │   ├─→ Identify secondary improvements
│   │   ├─→ Targeted revision
│   │   └─→ Coordinator confirmation
│   └─→ ITERATION 3: Final polish & publication readiness
│       ├─→ 5 virtual readers validate final state
│       ├─→ Final refinements
│       └─→ Coordinator approval for publication
│
├─→ STAGE 7: EDITING AGENT
│   └─ Final formatting and validation
│
├─→ STAGE 8: FINALIZATION AGENT
│   └─ Cover generation and metadata
│
└─→ STAGE 9: PUBLICATION AGENT
    └─ DOCX, EPUB, PDF, JSON exports

OUTPUT (results dictionary with all stage outputs)
```

---

## 🎯 The 9 Main Pipeline Stages

### 1️⃣ **Stage 1: Ideation Agent**
- **Purpose:** Transform raw input into coherent business idea
- **Responsibility:** Define transformation promise, core problem, target audience
- **Tools:** 
  - `search_knowledge_base()` - Find relevant information
  - `retrieve_rag_context()` - RAG integration point
- **Output:** Central idea framework with:
  - Transformation promise
  - Problem definition
  - Target audience profile
  - Value proposition

### 2️⃣ **Stage 2: Title Agent**
- **Purpose:** Generate market-optimized titles for Amazon visibility
- **Responsibility:** Create 3 title + subtitle combinations optimized for SEO and market appeal
- **Tools:**
  - `generate_amazon_optimized_title()` - Market analysis
  - `validate_title_seo()` - SEO scoring
- **Output:** 3 Amazon-optimized options with:
  - Title + subtitle combinations
  - SEO keyword alignment
  - Market appeal rating

### 3️⃣ **Stage 3: Structure Agent**
- **Purpose:** Create content hierarchy dimensioned to target word count
- **Responsibility:** Generate hierarchical outline with section weights
- **Tools:**
  - `generate_outline()` - Creates structured outline
  - `count_words()` - Validates word counts
- **Output:** Table of contents in Markdown with:
  - Chapter structure
  - Estimated word counts per section
  - Didactic flow

### 4️⃣ **Stage 4: Chapter Writing Agent**
- **Purpose:** Write didactic, high-quality content chapters
- **Responsibility:** Produce engaging technical content with RAG context
- **Tools:**
  - `retrieve_rag_context()` - Knowledge retrieval
  - `format_markdown()` - Markdown formatting
  - `validate_content_quality()` - Quality metrics
- **Output:** Didactic chapters with:
  - Technical accuracy
  - Clear explanations
  - RAG citations
  - Proper formatting

### 5️⃣ **Stage 5: Specialized Review (5 Personas)**
- **Purpose:** Comprehensive multi-perspective quality assurance
- **Responsibility:** Execute 5 specialized reviewers for thorough validation
- **Review Personas:**

#### **Technical Reviewer Agent**
- **Focus:** Code quality, framework versions, technical accuracy
- **Checks:**
  - Python code syntax and best practices
  - LangChain 1.0+ API compatibility
  - AI/ML concept accuracy
  - Example code execution validation
- **Output:** Technical feedback with quality metrics

#### **Editorial Reviewer Agent**
- **Focus:** Writing quality, clarity, flow, audience alignment
- **Checks:**
  - Readability and clarity
  - Tone consistency
  - Paragraph flow and transitions
  - Grammar and spelling accuracy
- **Output:** Editorial suggestions and improvements

#### **Content Stylist Agent**
- **Focus:** Formatting consistency, visual hierarchy, structure
- **Checks:**
  - Heading hierarchy (H1, H2, H3)
  - Code block formatting
  - List consistency
  - Table of contents accuracy
- **Output:** Formatting recommendations

#### **Governance QA Agent**
- **Focus:** Compliance, metadata, security, standards
- **Checks:**
  - Framework version compliance
  - Security and data protection
  - LGPD compliance (Brazilian regulation)
  - Metadata completeness
- **Output:** Compliance validation report

#### **Ethics Validator Agent**
- **Focus:** Bias detection, medical disclaimers, AI ethics principles
- **Checks:**
  - Language bias detection
  - Medical disclaimer requirements
  - AI ethics principles
  - HIPAA/LGPD compliance
- **Output:** Ethics validation and recommendations

#### **Author Stories & Didactics Reviewer Agent** (NEW)
- **Focus:** Balance between author's personal narratives and pedagogical clarity
- **Responsibility:** Ensure author stories enhance (not overshadow) learning objectives
- **Checks:**
  - Story relevance to chapter topic
  - Narrative weight vs. content balance
  - Educational value and didactic flow
  - Avoid excessive personal details or off-topic anecdotes
  - Stories serve as teaching tools or relatable examples
- **RAG Integration:** Consults RAG Author Stories knowledge base
- **Output:** Balance feedback and narrative optimization suggestions

#### **Author Positioning Reviewer Agent** (NEW)
- **Focus:** Author's market positioning and subject matter authority
- **Responsibility:** Validate clear positioning in target industry/theme and expertise prominence
- **Checks:**
  - Author's authority and credibility are evident
  - Positioning in target market/industry is clear
  - Niche expertise and specialization shine through
  - Marketing positioning is authentic and compelling
  - Author's unique perspective/angle is distinctive
- **RAG Integration:** Consults RAG Author Positioning knowledge base
- **Output:** Positioning clarity and authority validation

#### **Author Vision & Opinions Reviewer Agent** (NEW)
- **Focus:** Author's worldview, core values, and thematic opinions
- **Responsibility:** Ensure content aligns with author's philosophy and authentic voice
- **Checks:**
  - Content reflects author's stated values and principles
  - Opinions are authentic and consistent
  - Philosophical stance is clear and coherent
  - Author's vision for impact permeates the work
  - No contradictions with stated worldview
- **RAG Integration:** Consults RAG Author Vision & Opinions knowledge base
- **Output:** Vision consistency and authenticity feedback

- **Output:** Aggregated feedback from 5 perspectives:
  ```python
  {
    "technical": "Code quality feedback...",
    "editorial": "Writing quality feedback...",
    "stylist": "Formatting feedback...",
    "governance": "Compliance feedback...",
    "ethics": "Ethics and bias feedback..."
  }
  ```

### 6️⃣ **Stage 6: Critical Reading & Iterative Revision (3 Cycles)**
- **Purpose:** Validate content quality through diverse reader perspectives and improve through iterative feedback
- **Responsibility:** Execute 3 complete cycles of critical reading feedback and revision
- **Process:**
  
#### **Virtual Reader Personas** (execute independently each iteration):
  
1. **Curious Beginner Reader**
   - Perspective: New to topic, seeks clarity and accessibility
   - Feedback Focus: Terminology clarity, progression speed, foundational assumptions
   - Identifies: Confusing sections, missing context, overly technical language
   
2. **Technical Professional Reader**
   - Perspective: Senior practitioner, validates depth and accuracy
   - Feedback Focus: Technical correctness, framework knowledge, best practices
   - Identifies: Outdated patterns, missing nuances, incorrect examples
   
3. **Didactic Educator Reader**
   - Perspective: Teacher/mentor with pedagogical expertise
   - Feedback Focus: Learning progression, exercise effectiveness, knowledge scaffolding
   - Identifies: Pedagogical gaps, ineffective examples, poor sequencing
   
4. **Domain Specialist Reader**
   - Perspective: Expert in specific domain, cross-disciplinary perspective
   - Feedback Focus: Specialized knowledge accuracy, cross-domain consistency
   - Identifies: Domain-specific gaps, contextual misalignments, missing frameworks
   
5. **Reflective Reader**
   - Perspective: General audience, evaluates emotional impact
   - Feedback Focus: Emotional connection, relatability, engagement level
   - Identifies: Tone issues, missing human context, disconnected sections

#### **Iteration 1: Critical Issues & Initial Improvements**
- **Phase 1:** 5 virtual readers analyze content independently
- **Phase 2:** Feedback aggregation and prioritization (critical → nice-to-have)
- **Phase 3:** Targeted revision addressing critical comprehension and accuracy issues
- **Phase 4:** Coordinator validation of improvement quality
- **Output:** Improved content with critical issues resolved

#### **Iteration 2: Secondary Improvements & Engagement Enhancement**
- **Phase 1:** 5 virtual readers re-analyze updated content
- **Phase 2:** Identify remaining issues and refinement opportunities
- **Phase 3:** Revision addressing engagement and secondary improvements
- **Phase 4:** Coordinator confirms progressive improvement trajectory
- **Output:** Further polished content with majority of issues resolved

#### **Iteration 3: Final Polish & Publication Readiness**
- **Phase 1:** 5 virtual readers validate final improvements
- **Phase 2:** Final polish and verification feedback
- **Phase 3:** Address remaining refinements and final enhancements
- **Phase 4:** Coordinator approves content as publication-ready
- **Output:** Publication-ready content with coordinator sign-off

- **Success Criteria:**
  - All 5 readers provide independent, detailed feedback each iteration
  - 3 complete cycles executed sequentially
  - Critical issues resolved by Iteration 2
  - All identified issues addressed by Iteration 3
  - Content measurably improves each cycle (tracked by resolution rate)
  - Final version receives coordinator approval for publication

### 7️⃣ **Stage 7: Editing Agent**
- **Purpose:** Final formatting validation and consistency check
- **Responsibility:** Ensure document meets publishing standards
- **Tools:**
  - `review_logical_flow()` - Flow validation
  - `validate_markdown_format()` - Format validation
- **Output:** Publication-ready formatted document

### 8️⃣ **Stage 8: Finalization Agent**
- **Purpose:** Generate cover and validate all metadata
- **Responsibility:** Create cover concept and complete metadata
- **Tools:**
  - `generate_cover()` - AI cover design
  - `generate_kdp_metadata()` - Metadata generation
### 9️⃣ **Stage 9: Publication Agent**
- **Purpose:** Export to multiple formats for KDP
- **Responsibility:** Generate publication-ready packages
- **Tools:**
  - `export_to_docx()` - Word format export
  - `export_to_epub()` - EPUB format export
  - `export_to_pdf()` - PDF format export
  - Export to JSON for metadata
- **Output:** Complete KDP package with:
  - DOCX file (for editing)
  - EPUB file (for distribution)
  - PDF file (for preview)
  - JSON metadata

---

## 📁 File Organization

```
src/
├── main.py           # Pipeline orchestration (9 stages)
├── agents.py         # 9 main agents + 1 coordinator + 10 specialized reviewers + 5 virtual readers
├── tools.py          # 30+ specialized tools
├── config.py         # Model initialization and config
└── __init__.py       # Package initialization
```

---

## 🚀 Performance Summary

| Component | Time | Notes |
|-----------|------|-------|
| Full Pipeline | 2-5 min | API latency dependent |
| Single Agent | 15-30 sec | Average per stage |
| 5 Review Personas | 60-90 sec | Sequential execution |
| Total Tokens | 5K-10K | Gemini API usage |

---

## 🔐 Security & Compliance

- ✅ LGPD (Brazilian Data Protection) - Validated in Governance QA
- ✅ HIPAA (Healthcare) - Checked in Ethics Validator
- ✅ No credentials in code - Environment-based configuration
- ✅ Type hints and docstrings - Full documentation
- ✅ Error handling - Layered approach across all levels

---

## ✅ Implementation Status

| Component | Status | Details |
|-----------|--------|---------|
| 8 Main Agents | ✅ Complete | All stages implemented |
| 5 Review Personas | ✅ Complete | Specialized expertise agents |
| 30+ Tools | ✅ Complete | Organized by stage |
| LangChain 1.0+ | ✅ Integrated | Using create_agent() pattern |
| Gemini 2.5 Flash | ✅ Configured | Model initialized |
| RAG Integration Points | ✅ Ready | TODO implementations marked |
| Code Standards | ✅ Documented | .github/copilot-instructions.md |
| Documentation | ✅ Complete | README.md, ARCHITECTURE.md |

### 🎯 **Superagente Coordenador**
- **Responsabilidade:** Orquestra todo o pipeline de 8 etapas
- **Ferramentas:** Todas as ferramentas disponíveis
- **Output:** E-book completo publicável

---

## 🛠️ Ferramentas Disponíveis

### Search and Query
- `search()` - Context-aware information search
- `calculate()` - Mathematical expressions
- `query_rag()` - Vector database query

### Creation and Formatting
- `generate_outline()` - Content structure
- `generate_amazon_title()` - KDP-optimized titles
- `format_markdown()` - Standard formatting
- `generate_ai_cover()` - Visual cover
- `generate_kdp_metadata()` - JSON metadata file

### Validation and Review
- `review_engagement()` - Tone and engagement
- `review_empathy()` - Clarity and accessibility
- `review_grammar()` - Spelling and grammar
- `review_coherence()` - Logical flow
- `review_code()` - Technical examples
- `validate_content()` - Overall quality

### Export
- `export_docx()` - Microsoft Word
- `export_epub()` - E-book format
- `count_words()` - Final word counter

---

## 📁 File Structure

```
src/
├── main.py           # Main editorial pipeline (9 stages)
├── agents.py         # Definition of 8 specialized agents
├── tools.py          # Available tools (30+ tools)
├── config.py         # Gemini 2.5 Flash model configuration
└── __pycache__/
```

---

## 🚀 How to Run

```bash
# Set environment variable
export GOOGLE_API_KEY='your_api_key'

# Run pipeline
uv run python src/main.py
```

### Customize Topic and Target

Edit in `src/main.py`, function `main()`:

```python
topic = "Your Topic"
target_audience = "Your Audience"
word_count_target = 15000  # or another value
run_ebook_pipeline(topic, target_audience, word_count_target)
```

---

## 📊 Pipeline Flow

```
INPUT (topic, audience, target)
         ↓
    IDEATION (Agent 1)
         ↓
    TITLE (Agent 2)
         ↓
    STRUCTURE (Agent 3)
         ↓
    CHAPTERS (Agent 4) → RAG
         ↓
    REVIEW (Agent 5) → 3 loops
         ↓
    EDITING (Agent 6)
         ↓
    FINALIZATION (Agent 7) → Cover
         ↓
    KDP (Agent 8) → DOCX + EPUB + JSON
         ↓
OUTPUT (eBook ready for publication)
```

---

## ✨ Features

- ✅ **Modular:** Each agent has single responsibility
- ✅ **Scalable:** Easy to add new agents/tools
- ✅ **RAG-Ready:** Integrated with vector database (Supabase pgvector)
- ✅ **MCP-Compatible:** Interface for external tools
- ✅ **KDP-Compliant:** Output ready for Amazon Kindle
- ✅ **Bilingual:** Strings in Portuguese, code in English

---

## 🎯 Next Iterations (Roadmap)

- [ ] **v1.1:** Complete review loop (3 iterations)
- [ ] **v1.2:** MCP integration with external tools
- [ ] **v2.0:** LangGraph + Web Interface
- [ ] **v2.1:** Automatic KDP publication

---

**Developed by:** Igor Medeiros  
**Date:** November 2025  
**Version:** 1.0 (MVP)
