# 📚 Ebook Generator 1.0

Pipeline editorial multiagente em Python + LangChain que gera ebooks técnicos sobre LangChain aplicado à saúde clínica. O sistema lê um **Book Requirements Document (`specs/brd.yaml`)**, executa pesquisas temáticas e por capítulo com Gemini 2.5 Pro, redige capítulos completos com Gemini 2.5 Flash e entrega o material final em Markdown (`result/ebook.md`). Toda a experiência é guiada via Rich, com confirmações, tabelas e resumos visuais.

> Documentação complementar: [docs/PRD.md](docs/PRD.md) · [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 🎯 Overview

Ebook Generator 1.0 is an advanced multi-agent system that orchestrates the complete editorial process from ideation to KDP publication. The pipeline combines specialized AI agents with 10 specialized review personas and 5 virtual readers for iterative critical feedback.

### Key Features

- **9-Stage Autonomous Pipeline**: From ideation to publication-ready package
- **10 Specialized Review Personas**: Technical, Editorial, Style, Governance, Ethics, Author Stories, Author Positioning, Author Vision, Code Reviewer, Research Validator
- **5 Virtual Readers**: Beginner, Professional, Educator, Specialist, and Reflective perspectives
- **25 Independent Agents**: 9 pipeline + 10 review + 5 readers (defined in specs/agents.yaml)
- **Dual-Model Strategy**: Gemini 2.5 Flash (writing, 0.7°) + Gemini 2.5 Pro (research/RAG, 0.3°)
- **LangChain 1.0+ Native**: Built on latest best practices and patterns
- **Configuration-Driven**: All parameters in YAML (pipeline, agents, config, models, tools)
- **RAG Integration Ready**: Supabase pgvector support for knowledge augmentation
- **Production Quality**: Output validated for Amazon KDP, LGPD, and industry standards
- **Extensible Architecture**: Easy to add new agents, tools, and personas
- **Envio automático para Kindle**: Tool dedicada envia o EPUB finalizado via SMTP (Gmail) diretamente para o e-mail do Kindle

## � Implementation Status

**Phase 1: Architecture & Configuration ✅ COMPLETE**
- ✅ specs/ YAML system (pipeline.yaml, agents.yaml, config.yaml, models.yaml, tools.yaml)
- ✅ agents.yaml: 25 agents fully specified (9 main + 10 review + 5 readers)
- ✅ pipeline.yaml: 9 stages with agent ID mappings
- ✅ Agent decoupling: Agents independent of stages
- ✅ config.py: YAML loading, dual-model setup, logging with Rich
- ✅ Documentation: PRD.md, ARCHITECTURE.md, copilot-instructions.md

**Phase 2: Core Implementation ⏳ IN PROGRESS**
- ⏳ agents.py: Complete logic for 25 agents (currently stubs)
- ⏳ tools.py: Implement 30+ tools (currently stubs)
- ⏳ main.py: Sequential execution of 9-stage pipeline
- ⏳ input_validator.py: Validation and spec merging
- ⏳ Supabase RAG integration (basic operations)

**Phase 3: Testing & Refinement ❌ NOT STARTED**
- ❌ tests/: Unit tests for agents, tools, pipeline
- ❌ Context7 MCP deep research integration
- ❌ Performance optimization
- ❌ Edge case handling

**Current Focus**: See TODO.md for detailed task list. Start with agents.py completion to unblock the entire pipeline.

## �📋 Pipeline Architecture

### The 9-Stage Editorial Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│ EBOOK GENERATOR 1.0 - 9-STAGE EDITORIAL PIPELINE                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ Stage 1: IDEATION                                                      │
│ └─ Define: Central idea, problem, target audience, transformation    │
│    Output: Business idea framework                                    │
│                                                                         │
│ Stage 2: TITLE GENERATION                                             │
│ └─ Generate: 3 Amazon-optimized title + subtitle combinations        │
│    Output: Market-optimized titles                                    │
│                                                                         │
│ Stage 3: STRUCTURE & OUTLINE                                          │
│ └─ Create: Hierarchical table of contents scaled to word count        │
│    Output: Didactic outline in Markdown                               │
│                                                                         │
│ Stage 4: CHAPTER WRITING                                              │
│ └─ Write: Didactic content with RAG context integration               │
│    Output: Content chapters with citations                            │
│                                                                         │
│ Stage 5: SPECIALIZED REVIEW (5 PERSONAS)                              │
│ ├─ Technical Reviewer (code quality, framework versions)              │
│ ├─ Editorial Reviewer (clarity, tone, flow, linguistics)               │
│ ├─ Content Stylist (formatting, structure, consistency)                │
│ ├─ Governance QA (compliance, metadata, security, LGPD)                │
│ └─ Ethics Validator (bias, medical disclaimers, AI ethics, HIPAA)     │
│    Output: 5-perspective feedback dictionary                          │
│                                                                         │
│ Stage 6: CRITICAL READING (5 VIRTUAL READERS)                        │
│ ├─ Curious Beginner (clarity, progression, accessibility)            │
│ ├─ Technical Professional (depth, relevance, accuracy)                │
│ ├─ Didactic Educator (pedagogical structure, methodology)             │
│ ├─ Domain Specialist (application relevance, coherence)               │
│ └─ Reflective Reader (empathy, purpose, emotional impact)             │
│    Output: Independent feedback from 5 reading perspectives            │
│                                                                         │
│ Stage 7: EDITING & FORMATTING                                         │
│ └─ Validate: Markdown formatting, heading hierarchy, consistency      │
│    Output: Publication-ready formatted document                       │
│                                                                         │
│ Stage 8: FINALIZATION & COVER                                         │
│ └─ Generate: Cover concept and validate metadata                      │
│    Output: Cover design + validated metadata                          │
│                                                                         │
│ Stage 9: PUBLICATION & KDP EXPORT                                     │
│ └─ Export: DOCX, EPUB, PDF, JSON formats for KDP                      │
│    Output: Complete publication package                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Review Personas: The Quality Assurance Core

The system includes 5 specialized review personas, each with domain expertise:

#### 1. **Technical Reviewer Agent**
- **Expertise**: Code quality and technical accuracy
- **Focus**:
  - Python code syntax and best practices
  - LangChain API compatibility (v1.0+ patterns)
  - AI/ML concept accuracy
  - Framework version validation
  - Example code execution testing

#### 2. **Editorial Reviewer Agent**
- **Expertise**: Writing quality and audience engagement
- **Focus**:
  - Clarity and readability
  - Tone and voice consistency
  - Paragraph flow and transitions
  - Grammar and spelling accuracy
  - Terminology consistency

#### 3. **Content Stylist Agent**
- **Expertise**: Formatting and visual consistency
- **Focus**:
  - Heading hierarchy (H1, H2, H3)
  - Code block formatting
  - List consistency
  - Table of contents accuracy
  - Visual emphasis usage

#### 4. **Governance QA Agent**
- **Expertise**: Compliance and standards
- **Focus**:
  - Framework version accuracy
  - Security compliance
  - LGPD compliance (Brazilian data protection)
  - Metadata completeness
  - Copyright and license declarations

#### 5. **Ethics Validator Agent**
- **Expertise**: AI ethics and regulatory compliance
- **Focus**:
  - Bias detection and mitigation
  - Medical disclaimer requirements
  - AI ethics principles
  - LGPD/HIPAA compliance
  - Diversity and inclusion language

## � Virtual Readers: Critical Reading Personas

The system simulates **5 virtual readers** that provide independent, iterative feedback:

| Persona | Profile | Validation Focus |
|---------|---------|------------------|
| **👩‍💻 Curious Beginner** | New to AI/programming | Clarity, progression, accessibility |
| **🧔 Technical Professional** | Senior developer | Depth, relevance, technical accuracy |
| **👩‍🏫 Didactic Educator** | Teacher/mentor | Pedagogical structure, methodology |
| **👨‍⚕️ Domain Specialist** | Physician, researcher | Application relevance, cross-disciplinary coherence |
| **🧘 Reflective Reader** | General audience | Empathy, purpose, emotional impact |

Each reader generates independent reports that feed into the **3-iteration refinement loop** conducted by the Coordinator Super Agent.

## �🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google API Key (Gemini 2.5 Flash)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/igormedeiros/ebook-generator.git
   cd ebook-generator
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Configure environment**
   ```bash
   # Add your Google API Key
   export GOOGLE_API_KEY="your-api-key-here"
   ```

### Basic Usage

The project now ships with a dedicated CLI entry point exposed through `src/__main__.py`. Running `python -m src` (or `uv run python -m src` inside the managed environment) boots the validator shim and executes the same pipeline used in tests, so you no longer need wrapper scripts or ad-hoc modules.

#### Option 1: Interactive Mode (Recommended)

### Optional: Kindle Delivery

To automatically deliver the final EPUB to your Kindle account, configure the following environment variables (a Gmail account with an app password is required):

```bash
export KINDLE_EMAIL="seu_usuario@kindle.com"            # Endereço aprovado na Amazon
export KINDLE_SMTP_USER="seu_usuario@gmail.com"        # Conta Gmail usada para envio
export KINDLE_SMTP_PASSWORD="app-password"             # App password do Gmail
# Opcional: sobrescreva servidor/porta padrão
# export KINDLE_SMTP_SERVER="smtp.gmail.com"
# export KINDLE_SMTP_PORT="587"
```

O pipeline passa a disponibilizar a tool `send_epub_to_kindle` durante a fase de finalização/publicação. Ao invocá-la (manual ou automaticamente), o arquivo `.epub` já convertido é anexado ao e-mail e entregue diretamente no Kindle registrado, permitindo revisar o conteúdo final no dispositivo.

The pipeline automatically loads specifications from `input/book_input.yaml`. If any required fields are missing, it will prompt you interactively:

```bash
uv run python -m src
```

This will:
1. Load `input/book_input.yaml` specifications
2. Prompt for any missing required fields (topic, audience, word count)
3. Execute the full 9-stage pipeline
4. Generate publication-ready output

#### Option 2: Pre-configured Book Specification

Edit `input/book_input.yaml` with your book specifications:

```yaml
# input/book_input.yaml
topic: "Advanced Python with LangChain"
target_audience: "Senior Python Developers"
word_count_target: 15000
transformation_promise: "Master LangChain for production AI systems"
reading_level: "advanced"
```

Then run:
```bash
uv run python -m src
```

#### Option 3: Programmatic Usage

The CLI ultimately delegates to `run_ebook_pipeline` in `src/main.py`, so you can import the same helper inside notebooks or automation scripts:

```python
from src.input_validator import InputValidator
from src.main import run_ebook_pipeline

# Validate specifications and collect missing data
validator = InputValidator()
config = validator.validate()

# Execute the pipeline
results = run_ebook_pipeline(
    topic=config["topic"],
    target_audience=config["target_audience"],
    word_count_target=config["word_count_target"],
    transformation_promise=config.get("transformation_promise", ""),
    reading_level=config.get("reading_level", "intermediate"),
    run_all_stages=True
)
```

#### Specification File Format

The system uses `input/book_input.yaml` to configure your ebook:

```yaml
# Mandatory fields
topic: "Your ebook topic"
target_audience: "Who this is for"
word_count_target: 15000

# Optional fields
transformation_promise: "What transformation will readers experience?"
reading_level: "beginner|intermediate|advanced"
author_name: "Your name"
author_bio: "Your credentials"
publication_year: 2025

# Advanced: Stage-specific overrides
stage_overrides:
  stage_1_ideation:
    reading_level: "beginner"
  stage_2_title:
    title_count: 5
```

## 📁 Project Structure

```
ebook-generator/
├── .github/
│   └── copilot-instructions.md    # Code standards and best practices
├── src/
│   ├── main.py                     # Pipeline orchestration (9 stages)
│   ├── agents.py                   # All agent definitions (25 agents)
│   ├── tools.py                    # All tool definitions (30+ tools)
│   ├── config.py                   # Configuration, logging, models
│   ├── input_validator.py          # Input validation and interactive prompts
│   └── __init__.py                 # Package initialization
├── specs/                          # Configuration & Specifications
│   ├── pipeline.yaml               # 9-stage parameters with agent mappings
│   ├── agents.yaml                 # 25 independent agent specifications
│   ├── config.yaml                 # Portuguese strings and messages
│   ├── models.yaml                 # Gemini model configuration
│   ├── tools.yaml                  # Tool specifications (30+)
│   ├── book.yaml                   # Generated from input validation (gitignore)
│   └── README.md                   # Configuration documentation
├── input/
│   └── book_input.yaml             # User-provided book specification
├── docs/
│   ├── PRD.md                      # Product Requirements Document (v1.0)
│   └── ARCHITECTURE.md             # Technical Architecture (v1.0)
├── pyproject.toml                  # Project metadata and dependencies
├── README.md                        # This file
└── requirements.txt                # Python dependencies
```

## � Configuration System

All parameters are externalized to YAML specifications in `specs/`:

### Core Configuration Files

**1. pipeline.yaml** - 9-stage pipeline with agent ID mappings
- Defines 9 stages (Stage 1: Ideation → Stage 9: Publication)
- Each stage references an agent via the `agent` field
- Includes stage-specific parameters with types, defaults, and ranges
- Example: `stage_1_ideation: { agent: "ideation_agent", parameters: {...} }`

**2. agents.yaml** - 25 independent agent specifications
- **Main Pipeline Agents** (9): ideation_agent, title_agent, structure_agent, deep_research_agent, chapter_writing_agent, review_coordinator_agent, critical_reading_coordinator_agent, editing_agent, finalization_agent, publication_agent
- **Review Personas** (10): technical_reviewer, editorial_reviewer, content_stylist, governance_qa, ethics_validator, author_stories_reviewer, author_positioning_reviewer, author_vision_reviewer, code_examples_reviewer, research_validator
- **Virtual Readers** (5): curious_beginner, technical_professional, didactic_educator, domain_specialist, reflective_reader
- Each agent includes: name, model, role, responsibility, focus_areas, process, output_format, tools, timeouts

**3. config.yaml** - Centralized Portuguese strings
- 100+ messages (pipeline events, agent operations, validation results)
- Labels for UI and reporting
- System prompts base for agents
- Table titles and icons for Rich formatting

**4. models.yaml** - AI model configuration
- **write_model**: Gemini 2.5 Flash (temperature: 0.7 - balanced creativity)
- **research_model**: Gemini 2.5 Pro (temperature: 0.3 - focused for RAG)
- API configuration and token limits

**5. tools.yaml** - 30+ tool specifications
- Tool definitions organized by pipeline stage
- Default values and constraints
- Timeout and retry configurations

**6. book.yaml** - Generated at runtime
- Merged configuration from `input/book_input.yaml` + defaults
- Auto-generated during input validation
- Not committed to git (regenerated on each run)

### Input Validation Flow

```
input/book_input.yaml (user fills)
    ↓
InputValidator.validate_book_input()
    ├─ Check mandatory fields (topic, target_audience, word_count_target)
    ├─ Validate types and ranges
    ├─ Interactive prompts for missing/invalid fields
    └─ Merge with defaults from pipeline.yaml
    ↓
specs/book.yaml (auto-generated)
    ↓
run_ebook_pipeline(**config)
```

### Configuration Access in Code

```python
from src.config import (
    get_pipeline_config,      # Load all 9 stages with parameters
    get_agents_config,        # Load all 25 agent specifications
    get_agent_for_stage,      # Map stage name to agent ID
    get_models_config,        # Load model configuration
    get_message,              # Get Portuguese message by key
)

# Get agent for a specific stage
agent_id = get_agent_for_stage("stage_1_ideation")  # Returns: "ideation_agent"

# Load agent specification
agents_config = get_agents_config()
agent_spec = agents_config['main_pipeline_agents'][agent_id]
```

## �🔧 Core Components

### agents.py: Specialized Agents

The system includes 25 distinct agent specifications:

**Main Pipeline Agents (9)**:
- `ideation_agent` - Stage 1: Central idea definition (Flash)
- `title_agent` - Stage 2: Amazon-optimized titles (Flash)
- `structure_agent` - Stage 3: Outline generation (Flash)
- `deep_research_agent` - Stage 4A: Deep research via Context7 MCP (Pro)
- `chapter_writing_agent` - Stage 4B: Content writing with RAG (Flash)
- `review_coordinator_agent` - Stage 5: Review orchestration (Pro)
- `critical_reading_coordinator_agent` - Stage 6: Critical reading iterations (Pro)
- `editing_agent` - Stage 7: Formatting validation (Flash)
- `finalization_agent` - Stage 8: Cover and metadata (Flash)
- `publication_agent` - Stage 9: Export to all formats (Flash)

**Specialized Review Personas (10)**:
- `technical_reviewer` - Code quality, framework versions, syntax
- `editorial_reviewer` - Clarity, tone, flow, audience alignment
- `content_stylist` - Formatting consistency, visual hierarchy
- `governance_qa` - Compliance, metadata, security, LGPD
- `ethics_validator` - Bias detection, medical disclaimers, AI ethics
- `author_stories_reviewer` - Narrative balance, didactic flow (RAG: author_stories)
- `author_positioning_reviewer` - Authority, positioning clarity (RAG: author_positioning)
- `author_vision_reviewer` - Vision alignment, opinion authenticity (RAG: author_vision_opinions)
- `code_examples_reviewer` - Code execution, exercises, GitHub collection
- `research_validator` - Source credibility, fact-checking, citation accuracy

**Virtual Reader Personas (5)**:
- `curious_beginner` - New learner perspective (Flash)
- `technical_professional` - Expert validation (Pro)
- `didactic_educator` - Methodology perspective (Flash)
- `domain_specialist` - Cross-disciplinary view (Pro)
- `reflective_reader` - General audience (Flash)

### agents.py: Specialized Agents

The system includes agent creators for all 25 agents:

**Main Pipeline Agents (9)**:
- `create_ideation_agent()` - Stage 1: Central idea definition
- `create_title_agent()` - Stage 2: Amazon-optimized titles
- `create_structure_agent()` - Stage 3: Outline generation
- `create_chapter_agent()` - Stage 4: Content writing
- `create_review_agent()` - Stage 5: Review orchestration
- `create_editing_agent()` - Stage 6: Formatting validation
- `create_finalization_agent()` - Stage 7: Cover and metadata
````
- `create_publication_agent()` - Stage 8: Export and packaging

**Specialized Review Agents (5)**:
- `create_technical_reviewer_agent()` - Code quality validation
- `create_editorial_reviewer_agent()` - Writing quality
- `create_content_stylist_agent()` - Formatting consistency
- `create_governance_agent()` - Compliance validation
- `create_ethics_validator_agent()` - Ethics and bias checking

**Orchestration**:
- `create_coordinator_superagent()` - 9-stage pipeline orchestrator
- `execute_review_personas()` - Execute all 5 reviewers in sequence

### tools.py: Specialized Tools

30+ tools organized by pipeline stage:

**Stage 1 - Ideation Tools**:
- `search_knowledge_base()` - Find relevant knowledge
- `retrieve_rag_context()` - RAG context retrieval

**Stage 2 - Title Tools**:
- `generate_amazon_optimized_title()` - Market-optimized titles
- `validate_title_seo()` - SEO validation

**Stage 3 - Structure Tools**:
- `generate_outline()` - Create hierarchical outlines
- `count_words()` - Word count validation

**Stage 4 - Writing Tools**:
- `format_markdown()` - Markdown formatting
- `validate_content_quality()` - Content metrics

**Stage 5 - Review Tools**:
- `review_tone_and_engagement()` - Tone analysis
- `review_clarity_and_empathy()` - Clarity checking
- `review_grammar_and_style()` - Grammar validation
- `review_logical_flow()` - Flow analysis
- `review_code_examples()` - Code validation

**Stage 6 - Editing Tools**:
- (Formatting validation tools)

**Stage 7 - Finalization Tools**:
- `generate_cover()` - Cover design generation
- `generate_kdp_metadata()` - KDP metadata

**Stage 8 - Publication Tools**:
- `export_to_docx()` - Word export
- `export_to_epub()` - EPUB export
- `export_to_pdf()` - PDF export

### config.py: Configuration

Centralized configuration and model initialization:

```python
from config import get_model

model = get_model()  # Returns ChatGoogleGenerativeAI with Gemini 2.5 Flash
```

Configuration parameters:
- **Model**: Gemini 2.5 Flash
- **Temperature**: 0.7 (balanced creativity/consistency)
- **top_p**: 0.95
- **top_k**: 40

## 💡 Usage Examples

### Example 1: Full Pipeline Execution

```python
from src.main import run_ebook_pipeline

# Run complete 9-stage pipeline
results = run_ebook_pipeline(
    topic="Python Data Science with Pandas",
    target_audience="Data Scientists and Analysts",
    word_count_target=20000,
    run_all_stages=True
)

print(f"Stage 1 (Ideation): {results['ideation'][:200]}...")
print(f"Stage 2 (Titles): {results['title'][:200]}...")
print(f"Stage 5 Reviews: {results['review_personas'].keys()}")
```

### Example 2: Single Stage Execution

```python
from src.agents import (
    create_ideation_agent,
    execute_agent
)
from config import get_model

model = get_model()
agent = create_ideation_agent(model)

query = """
Define the central idea for a technical ebook:
Topic: Machine Learning in Healthcare
Target Audience: Healthcare professionals
Target Word Count: 12000
"""

result = execute_agent(agent, query)
print(result)
```

### Example 3: Custom Review Process

```python
from src.agents import (
    create_technical_reviewer_agent,
    create_editorial_reviewer_agent,
    execute_agent
)
from config import get_model

model = get_model()
content = "Your ebook content here..."

# Technical review
tech_agent = create_technical_reviewer_agent(model)
tech_feedback = execute_agent(tech_agent, f"Review this: {content}")

# Editorial review
editorial_agent = create_editorial_reviewer_agent(model)
editorial_feedback = execute_agent(editorial_agent, f"Review this: {content}")

print(f"Technical: {tech_feedback}")
print(f"Editorial: {editorial_feedback}")
```

## 🧠 LangChain 1.0+ Integration

The system uses LangChain 1.0+ native patterns with **dual-model strategy**:

### Dual-Model Architecture

**Writing & Revision Model**: Gemini 2.5 Flash
- Purpose: Fast, creative text generation and iterative refinement
- Configuration: temperature=0.7 (balanced creativity/consistency)

**Research & Analysis Model**: Gemini 2.5
- Purpose: Deep analysis, RAG context retrieval, semantic search
- Configuration: temperature=0.3 (focused for RAG accuracy)

### Tool Definition Pattern

```python
from langchain.tools import tool

@tool
def my_tool(param: str) -> str:
    """Tool description."""
    return "Tool result"
```

### Structured Output Pattern

```python
@tool(response_format="content_and_artifact")
def structured_tool(param: str) -> tuple[str, dict]:
    """Returns both narrative and structured data."""
    return narrative_text, structured_data
```

### Agent Creation

```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="Clear role definition..."
)
```

### Execution

```python
response = agent.invoke({
    "messages": [{"role": "user", "content": query}]
})
output = response["messages"][-1].content
```

## 🔗 RAG Integration (Supabase)

The system includes integration points for Retrieval-Augmented Generation:

### Chapter Writing RAG Modes

Stage 6 of the workflow (Escrita) now supports three explicit strategies for supplying context to the chapter-writing agent:

1. **RAG Local (KB completa)** — Carrega integralmente cada arquivo da pasta `kb/` para o contexto imediato do modelo. Ideal para bases pequenas ou estáticas.
2. **RAG Local com ChromaDB** — Indexa os arquivos da pasta `kb/` em um vetorstore local (ChromaDB) e recupera apenas os trechos relevantes (`rag_strategy: local_chromadb`).
3. **RAG Cloud Supabase** — Utiliza o backend Supabase pgvector para buscar conteúdos com embeddings hospedados na nuvem (`rag_strategy: supabase_cloud`).

Configure a estratégia desejada no `specs/pipeline.yaml` (parâmetro `rag_strategy` do estágio `stage_6_writing`) ou sobrescreva via input do pipeline.

```python
# Tools marked with RAG integration points
@tool
def retrieve_rag_context(query: str) -> str:
    """
    TODO: Implement Supabase pgvector integration
    1. Connect to Supabase (postgresql+psycopg://...)
    2. Query pgvector with similarity_search()
    3. Return top-k relevant documents
    """
    pass
```

### Setup Instructions

1. **Create Supabase project** with pgvector extension enabled
2. **Configure connection**:
   ```python
   from langchain.vectorstores import PGVectorStore
   
   vector_store = PGVectorStore.connect_from_documents(
       connection_string="postgresql+psycopg://user:password@host/db",
       documents=documents,
       embedding=embeddings,
   )
   ```
3. **Use in agents**: Call `retrieve_rag_context()` during chapter writing

## 📊 System Architecture

```
┌──────────────────────────────────────────────────────┐
│            EBOOK GENERATOR 1.0                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ORCHESTRATOR LAYER                                  │
│  ├─ create_coordinator_superagent()                 │
│  └─ run_ebook_pipeline()                            │
│                                                      │
│  AGENT LAYER (14 agents)                            │
│  ├─ 8 Main Pipeline Agents (ideation to pub)        │
│  ├─ 5 Specialized Review Personas                   │
│  └─ 1 Coordinator Super Agent                       │
│                                                      │
│  TOOL LAYER (30+ tools)                             │
│  ├─ Generation Tools (titles, outlines, etc)        │
│  ├─ Review Tools (tone, clarity, grammar)           │
│  ├─ Validation Tools (quality, compliance)          │
│  └─ Export Tools (DOCX, EPUB, PDF, JSON)            │
│                                                      │
│  MODEL LAYER                                         │
│  ├─ LangChain 1.0+                                  │
│  ├─ Google Generative AI (Gemini 2.5 Flash)         │
│  └─ RAG Backend (Supabase pgvector)                 │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## 🛠️ Configuration & Environment

### Environment Variables

```bash
# .env file
GOOGLE_API_KEY="your-gemini-api-key"

# Optional: RAG configuration
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-supabase-key"
```

### Model Parameters

Default Gemini 2.5 Flash configuration (in `config.py`):

```python
ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,      # Balanced creativity/consistency
    top_p=0.95,          # Diverse but focused
    top_k=40,            # Top K sampling
)
```

## 📈 Performance & Scaling

### Optimization Tips

1. **Batch Tool Calls**: Execute multiple tools in parallel when independent
2. **RAG Context**: Use top-k parameter to limit context size
3. **Token Usage**: Monitor Gemini API usage for cost optimization
4. **Caching**: Implement caching for repeated queries

### Expected Performance

- **Full Pipeline**: ~2-5 minutes (depending on API latency)
- **Single Agent**: ~15-30 seconds
- **Review Personas**: ~60-90 seconds (5 reviewers in sequence)
- **Token Cost**: ~5000-10000 tokens per full pipeline

## 🔐 Security & Compliance

### Standards Implemented

- **LGPD**: Brazilian data protection compliance checks
- **HIPAA**: Medical content disclaimer validation
- **Security**: No credentials in code, environment-based config
- **Ethics**: Bias detection and AI ethics validation

### Best Practices

- Store API keys in environment variables
- Use virtual environments
- Validate all inputs before processing
- Implement audit logging for sensitive operations

## 📚 Documentation

### Key Files

- `README.md` - This file, complete project documentation
- `.github/copilot-instructions.md` - Code standards and best practices
- `ARCHITECTURE.md` - Detailed system architecture
- `src/agents.py` - Agent definitions and docstrings
- `src/tools.py` - Tool definitions and docstrings

### Code Documentation

All functions include comprehensive docstrings:

```python
def my_function(param: str) -> dict:
    """
    Brief description.
    
    Args:
        param: Parameter description
    
    Returns:
        dict: Return value description
    """
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

## ✨ Principais capacidades

- **Fluxo em 3 fases** (`src/main.py`): pesquisa temática abrangente → pesquisa por capítulo → geração de conteúdo final.
- **Rastreabilidade total**: cada pesquisa é salva imediatamente em `kb/` (tanto por tópico quanto por capítulo) e reaproveitada em execuções futuras.
- **Configuração declarativa**: `specs/` concentra BRD, pipeline, agentes, tools, modelos, personas e mensagens em YAML.
- **UI rica**: `src/ui.py` oferece headers, tabelas, barras de progresso, prompts e resumos com Rich.
- **Multiagentes Gemini**: `src/agents.py` combina Gemini 2.5 Flash (escrita) e Gemini 2.5 Pro (research) com o inventário de tools em `src/tools.py`.
- **Exportações auxiliares**: ferramentas para DOCX/EPUB/PDF/JSON já existem (stubs) e podem ser orquestradas em automações futuras.

---

## 🗂️ Estrutura do repositório

```
├── docs/                 # PRD + Arquitetura atualizados a partir de src/
├── kb/                   # Pesquisas salvas (criado em tempo de execução)
├── result/               # Saída final em Markdown
├── specs/                # Configurações YAML (brd, pipeline, agents, tools, models, personas)
├── src/                  # Código-fonte (main, agents, tools, ui, config, input_validator)
├── templates/, template/ # Recursos auxiliares
├── tests/                # Testes automatizados (pytest)
├── pyproject.toml        # Dependências e metadados
└── README.md             # Este arquivo
```

---

## ⚙️ Pré-requisitos

- Python **3.11+**
- Conta Google com acesso ao **Gemini 2.5 Flash/Pro**
- `GOOGLE_API_KEY` definido no ambiente (`.env` suportado)
- macOS/Linux/WSL com acesso a terminal colorido (Rich)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/igormedeiros/ebook-generator.git
cd ebook-generator

# 2. Instale dependências (escolha uma opção)
uv sync              # recomendado
# ou
pip install -e .

# 3. Configure credenciais
export GOOGLE_API_KEY="sua-chave"
```

---

## 🧾 Preparando o BRD

1. Edite `specs/brd.yaml` para definir nome, descrição, público-alvo, `required_topics`, tom e características de escrita.
2. Ajuste parâmetros avançados em `specs/pipeline.yaml`, `specs/models.yaml`, `specs/tools.yaml` ou `specs/personas.yaml` conforme necessário.
3. Opcionalmente, rode `src/input_validator.py` para garantir que `specs/book.yaml` esteja completo antes da execução principal.

> Dica: mantenha pesquisas antigas em `kb/`. Na próxima execução o programa perguntará se deseja reutilizá-las ou gerar tudo do zero.

---

## ▶️ Executando o pipeline

```bash
uv run python -m src.main
# ou
python -m src.main
```

Durante a execução:

1. O sistema gera estrutura de capítulos e mostra prévia para aprovação.
2. Pesquisas temáticas são criadas (ou reutilizadas) e salvas imediatamente em `kb/thematic_*.md`.
3. Cada capítulo recebe pesquisa dedicada (`kb/research_*.md`).
4. Os capítulos finais são escritos em Markdown com base no research consolidado.
5. O ebook final é salvo em `result/ebook.md`, acompanhado de um resumo na TUI.

---

## 🔧 Tools e agentes

- `src/tools.py` agrupa mais de 30 ferramentas organizadas por estágio (ideação, títulos, estrutura, pesquisa, escrita, revisão, edição e publicação). Diversas funções já expõem TODOs para integrações reais com Supabase, Context7, ebooklib etc.
- `src/agents.py` registra `writer_agent`, `research_agent` e `thematic_research_agent` com prompts completos, garantindo consistência com o PRD.
- `src/config.py` carrega YAMLs e expõe `get_model()`, `get_research_model()` e helpers para mensagens, permitindo ajustes sem alterar código.

---

## 📄 Documentação complementar

- **Produto e requisitos**: [docs/PRD.md](docs/PRD.md)
- **Arquitetura técnica**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Specs avançadas**: veja arquivos em `specs/` (BRD, pipeline, agentes, tools, modelos, personas, prompts)

---

## ✅ Próximos passos sugeridos

- Conectar Supabase/pgvector nas funções `search_knowledge_base`, `retrieve_rag_context` e `store_in_rag_external`.
- Integrar Context7 MCP ao fluxo de pesquisa para enriquecer fontes externas.
- Ativar exportações DOCX/EPUB/PDF/JSON direto do pipeline principal.
- Automatizar validação de input (`SpecValidator`) antes de carregar o BRD.
- Criar testes de regressão para cada fase usando mocks de agentes.

Sinta-se à vontade para contribuir abrindo issues ou pull requests!
