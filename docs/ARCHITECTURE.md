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

### 2.1 MD Input Parser
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

### 2.2 Main Agents (8)

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
- **Responsibility**: Write chapters with synthetic inputs
- **Input**: Outline, central idea, specified style
- **Output**: Didactic chapters with personal/author examples
- **Tools**: 
  - External RAG (Gemini 2.5 Pro)
  - Author RAG (stories and opinions)
  - Markdown formatting
  - Quality validation

#### 5. Agent: Multiple Review
- **Responsibility**: Simulate specialized review personas (8 personas)
- **Personas**:
  - Editorial: Clarity, tone, flow
  - Technical: Code quality, conceptual precision
  - Empathy: Accessibility, emotional connection
  - Humor/Engagement: Lightness, interest
  - Compliance: LGPD, HIPAA, KDP
  - Stories & Didactics: Balances author narratives with pedagogy
  - Positioning: Validates author authority and market positioning
  - Vision & Opinions: Reviews author vision and opinions coherence
- **Input**: Raw chapters
- **Output**: Structured feedback by persona (8 perspectives)
- **RAG Integration**:
  - RAG Author Stories (for narrative balance evaluation)
  - RAG Positioning (for authority validation)
  - RAG Vision & Opinions (for philosophical coherence)
- **Loop**: Review cycle critical based on target audience, style and author identity

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

### 3.1 External RAG
```
Flow: Writer → Gemini 2.5 Pro → Query Supabase → Retriever
- Gemini 2.5 Pro performs deep research for each chapter
- Results vectorized and stored in Supabase
- LangChain Retriever searches top-k relevant documents
- Results feed into writing context
```

### 3.2 RAG Autoral - Author Knowledge Integration (Stories, Positioning, Vision)
```
Flow: Author Input → Ingestion → Vectorization → Supabase (3 categories) → Retriever
- Ingestion of 3 types of author knowledge:
  1. Personal Stories (narratives, experiences, author memories)
  2. Market Positioning (authority, niche, differentiation)
  3. Vision & Opinions (values, philosophy, worldview)
- Vectorization of each category with context metadata
- Storage in separate Supabase tables (rag_author_stories, rag_author_positioning, rag_author_vision)
- Retriever integrated in:
  - Writer: To incorporate author narratives organically
  - Author Stories Reviewer: To validate narrative balance
  - Author Positioning Reviewer: To validate positioning clarity
  - Author Vision Reviewer: To validate philosophical coherence
- Traceability guarantee: Each author RAG input is marked in final document
```

### 3.3 External RAG
```
Flow: Author Input → Ingestion → Vectorization → Supabase → Retriever
- Ingestion of author's personal stories
- Vectorization of opinions (especially on AI in healthcare)
- Storage in separate Supabase table
- Retriever integrated in Writer for recurring use
- Traceability guarantee in final document
```

### 3.4 Supabase Configuration
```sql
-- Table: rag_external
CREATE TABLE rag_external (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  embedding vector(1536),
  source VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table: rag_author_stories
CREATE TABLE rag_author_stories (
  id BIGSERIAL PRIMARY KEY,
  story TEXT NOT NULL,
  embedding vector(1536),
  category VARCHAR(100),
  tags TEXT[],
  author_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table: rag_author_positioning
CREATE TABLE rag_author_positioning (
  id BIGSERIAL PRIMARY KEY,
  positioning_statement TEXT NOT NULL,
  embedding vector(1536),
  aspect VARCHAR(100),
  author_name VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table: rag_author_vision
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
InputMD 
  ↓
MD Parser (validation and configuration propagation)
  ↓
Central Idea (essence + promise)
  ↓
Title Subtitle (research + 3 options)
  ↓
Structurer (outline + word distribution)
  ↓
Writer (chapters with RAG)
  ├→ External RAG (Gemini 2.5 Pro)
  ├→ Author Stories RAG (personal stories)
  ├→ Author Opinions RAG (author opinions)
  └→ Writer (synthesis of inputs)
  ↓
Multiple Review (8 personas)
  ├→ Editorial
  ├→ Technical
  ├→ Empathy
  ├→ Engagement
  ├→ Compliance
  ├→ Stories & Didactics (Stories RAG)
  ├→ Positioning (Positioning RAG)
  └→ Vision & Opinions (Vision RAG)
  ↓
Code Agent (Python code block validation)
  ↓
Style Editor (Markdown formatting)
  ↓
Summary Cover (dynamic + design API)
  ↓
Final Converter (format export)
  ├→ HTML
  ├→ DOCX
  ├→ EPUB
  └→ JSON (metadata)
  ↓
Publication Agent (KDP compilation)
  ├→ Metadata
  ├→ Synopsis
  ├→ Catalog sheet
  └→ Final files
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

### Required APIs
- **Google Gemini API**: For LLMs (Flash + Pro)
- **Supabase API**: For storage and vectorization
- **Banana API** (or similar): For AI cover generation
- **Pandoc**: For format conversion (local)

### Environment Configuration
```bash
export GOOGLE_API_KEY="your-key"
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-key"
export BANANA_API_KEY="your-key"  # optional for cover
```

---

## 9. Security and Compliance

### LGPD (General Data Protection Law)
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

AGENT LAYER (8 Agents)
├── Central Idea
├── Title/Subtitle
├── Structurer
├── Writer
├── Multiple Review (8 specialized personas)
├── Code
├── Style Editor
└── Summary/Cover

RAG LAYER
├── External RAG (Gemini 2.5 Pro)
├── Author RAG - 3 Knowledge Types:
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
└── Gemini 2.5 Pro (research)
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
│   └─ Create hierarchical outline
│
├─→ STAGE 4: CHAPTER AGENT
│   └─ Write didactic content with RAG
│
├─→ STAGE 5: REVIEW (8 SPECIALIZED PERSONAS)
│   ├─→ TECHNICAL REVIEWER (code quality, versions)
│   ├─→ EDITORIAL REVIEWER (clarity, tone, flow)
│   ├─→ CONTENT STYLIST (formatting, structure)
│   ├─→ GOVERNANCE QA (compliance, metadata)
│   ├─→ ETHICS VALIDATOR (bias, disclaimers)
│   ├─→ AUTHOR STORIES & DIDACTICS (narrative balance, RAG Stories)
│   ├─→ AUTHOR POSITIONING (marketing authority, RAG Positioning)
│   └─→ AUTHOR VISION & OPINIONS (values alignment, RAG Vision)
│       └─ Aggregated feedback dict (8 perspectives)
│
├─→ STAGE 6: EDITING AGENT
│   └─ Final formatting and validation
│
├─→ STAGE 7: FINALIZATION AGENT
│   └─ Cover generation and metadata
│
└─→ STAGE 8: PUBLICATION AGENT
    └─ DOCX, EPUB, PDF, JSON exports

OUTPUT (results dictionary with all stage outputs)
```

---

## 🎯 The 8 Main Pipeline Stages

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

### 6️⃣ **Stage 6: Editing Agent**
- **Purpose:** Final formatting validation and consistency check
- **Responsibility:** Ensure document meets publishing standards
- **Tools:**
  - `review_logical_flow()` - Flow validation
  - `validate_markdown_format()` - Format validation
- **Output:** Publication-ready formatted document

### 7️⃣ **Stage 7: Finalization Agent**
- **Purpose:** Generate cover and validate all metadata
- **Responsibility:** Create cover concept and complete metadata
- **Tools:**
  - `generate_cover()` - AI cover design
  - `generate_kdp_metadata()` - Metadata generation
### 8️⃣ **Stage 8: Publication Agent**
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
├── main.py           # Pipeline orchestration (8 stages)
├── agents.py         # 8 agents + 1 coordinator + 5 specialized reviewers
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
├── main.py           # Main editorial pipeline (8 stages)
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
