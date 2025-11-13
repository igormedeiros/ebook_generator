# Ebook Generator 1.0

**A Production-Ready, AI-Powered Editorial Pipeline for Autonomous Ebook Generation**

Transform raw topics into publication-ready ebooks with a sophisticated 9-stage editorial pipeline powered by LangChain 1.0+ and Google's Gemini AI.

## 🎯 Overview

Ebook Generator 1.0 is an advanced multi-agent system that orchestrates the complete editorial process from ideation to KDP publication. The pipeline combines 25 independent agent specifications with 10 specialized review personas and 5 virtual readers for iterative critical feedback.

### Key Features

- **9-Stage Autonomous Pipeline**: From ideation to publication-ready package
- **25 Independent Agents**: 9 pipeline + 10 review + 5 readers (defined in specs/agents.yaml, not stage-coupled)
- **10 Specialized Review Personas**: Technical, Editorial, Style, Governance, Ethics, Author Stories, Author Positioning, Author Vision, Code Reviewer, Research Validator
- **5 Virtual Readers**: Beginner, Professional, Educator, Specialist, and Reflective perspectives
- **Dual-Model Strategy**: Gemini 2.5 Flash (writing, 0.7°) + Gemini 2.5 Pro (research/RAG, 0.3°)
- **LangChain 1.0+ Native**: Built on latest best practices and patterns
- **Configuration-Driven Architecture**: All parameters externalized to YAML specs (no hardcoding)
- **RAG Integration Ready**: Supabase pgvector support for knowledge augmentation
- **Production Quality**: Output validated for Amazon KDP, LGPD, and industry standards
- **Extensible Architecture**: Easy to add new agents, tools, and personas

## 📋 Pipeline Architecture

### The 9-Stage Editorial Pipeline

```
STAGE 1: Ideation
├─ Agent: ideation_agent (Flash)
├─ Input: Topic, target audience, word count target
└─ Output: Central idea, problem definition, transformation promise

STAGE 2: Title Generation
├─ Agent: title_agent (Flash)
├─ Input: Ideation results
└─ Output: 3 Amazon-optimized title options

STAGE 3: Structure & Outline
├─ Agent: structure_agent (Flash)
├─ Input: Title + ideation
└─ Output: Hierarchical table of contents in Markdown

STAGE 4A: Deep Research
├─ Agent: deep_research_agent (Pro)
├─ Input: Chapter definitions
└─ Output: Vectorized research in rag_external (Supabase)

STAGE 4B: Chapter Writing
├─ Agent: chapter_writing_agent (Flash)
├─ Input: Outline + RAG research context
└─ Output: Didactic content chapters with citations

STAGE 5: Specialized Review (10 Personas)
├─ Agent: review_coordinator_agent (Pro)
├─ Reviewers: Technical, Editorial, Stylist, Governance, Ethics,
│             Author Stories, Author Positioning, Author Vision,
│             Code Reviewer, Research Validator
└─ Output: Structured feedback from 10 perspectives

STAGE 6: Critical Reading & Iteration (3 Cycles)
├─ Agent: critical_reading_coordinator_agent (Pro)
├─ Readers: Curious Beginner, Technical Professional, Educator,
│           Domain Specialist, Reflective Reader
└─ Output: Refined content with reader validation

STAGE 7: Editing & Formatting
├─ Agent: editing_agent (Flash)
├─ Input: Iterated content
└─ Output: Publication-ready formatted document

STAGE 8: Finalization & Cover
├─ Agent: finalization_agent (Flash)
├─ Input: Edited content
└─ Output: Cover concept + validated metadata

STAGE 9: Publication & Export
├─ Agent: publication_agent (Flash)
├─ Input: Final content
└─ Output: DOCX, EPUB, PDF, JSON for KDP
```

## 📁 Project Structure

```
ebook-generator/
├── .github/
│   └── copilot-instructions.md    # Code standards and best practices
├── src/
│   ├── main.py                     # Pipeline orchestration (9 stages)
│   ├── agents.py                   # Agent definitions (25 agents)
│   ├── tools.py                    # Tool definitions (30+ tools)
│   ├── config.py                   # Configuration loading, logging, models
│   ├── input_validator.py          # Input validation with interactive prompts
│   └── __init__.py                 # Package initialization
├── specs/                          # Configuration & Specifications
│   ├── pipeline.yaml               # 9-stage parameters with agent ID mappings
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

## 📋 Configuration System

All parameters are externalized to YAML specifications in `specs/` - **no hardcoded values in code**.

### Core Configuration Files

#### 1. **pipeline.yaml** - 9-Stage Pipeline with Agent Mappings
Defines all 9 pipeline stages with parameters and agent references.

Key architecture: Each stage references an agent via the `agent` field.
```yaml
stage_1_ideation:
  name: "Ideação"
  agent: "ideation_agent"  # Reference from agents.yaml
  parameters:
    topic:
      type: string
      required: true
    target_audience:
      type: string
      required: true
    word_count_target:
      type: integer
      default: 15000
      min: 5000
      max: 100000
```

#### 2. **agents.yaml** - 25 Independent Agent Specifications
Defines all agents INDEPENDENTLY (not per-stage). This allows agents to be reused or reconfigured.

**Main Pipeline Agents (9)**:
- `ideation_agent` - Central idea synthesis (Gemini Flash)
- `title_agent` - Title generation (Flash)
- `structure_agent` - Outline creation (Flash)
- `deep_research_agent` - Deep research via Context7 MCP (Gemini Pro)
- `chapter_writing_agent` - Content generation (Flash)
- `review_coordinator_agent` - Review orchestration (Pro)
- `critical_reading_coordinator_agent` - Iterative refinement (Pro)
- `editing_agent` - Formatting & validation (Flash)
- `finalization_agent` - Cover & metadata (Flash)
- `publication_agent` - Export to all formats (Flash)

**Review Personas (10)**:
- `technical_reviewer` - Code quality & framework validation
- `editorial_reviewer` - Clarity, tone, flow
- `content_stylist` - Formatting & consistency
- `governance_qa` - Compliance & security
- `ethics_validator` - Bias & AI ethics
- `author_stories_reviewer` - Narrative balance (RAG: author_stories)
- `author_positioning_reviewer` - Authority & positioning (RAG: author_positioning)
- `author_vision_reviewer` - Vision alignment (RAG: author_vision_opinions)
- `code_examples_reviewer` - Code execution & GitHub collection
- `research_validator` - Source credibility & fact-checking

**Virtual Readers (5)**:
- `curious_beginner` - Beginner perspective
- `technical_professional` - Expert validation
- `didactic_educator` - Methodology perspective
- `domain_specialist` - Cross-disciplinary view
- `reflective_reader` - General audience

Each agent spec includes: name, model, role, responsibility, focus_areas, process, output_format, tools, timeouts.

#### 3. **config.yaml** - Centralized Portuguese Strings
- 100+ messages (pipeline events, agent operations, validation results)
- Labels for UI and reporting
- System prompts base for agents
- Table titles and icons for Rich formatting

#### 4. **models.yaml** - AI Model Configuration
- **write_model**: Gemini 2.5 Flash (temperature: 0.7 - balanced creativity)
- **research_model**: Gemini 2.5 Pro (temperature: 0.3 - focused for RAG)
- API configuration and token limits

#### 5. **tools.yaml** - 30+ Tool Specifications
- Tool definitions organized by pipeline stage
- Default values and constraints
- Timeout and retry configurations

#### 6. **book.yaml** - Generated Configuration
- Auto-generated from `input/book_input.yaml` + defaults
- Merged configuration ready for pipeline execution
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

# Get pipeline configuration
pipeline_config = get_pipeline_config()
stage_1_params = pipeline_config['stages']['stage_1_ideation']['parameters']
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google API Key (Gemini 2.5)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/igormedeiros/ebook-generator.git
   cd ebook-generator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Add your Google API Key
   export GOOGLE_API_KEY="your-api-key-here"
   ```

### Basic Usage

```python
from src.input_validator import validate_book_input
from src.main import run_ebook_pipeline

# Validate input and run the 9-stage pipeline
config = validate_book_input()  # Loads and validates input/book_input.yaml
results = run_ebook_pipeline(**config)

# Access results from each stage
ideation = results["ideation"]
titles = results["title"]
structure = results["structure"]
chapters = results["chapters"]
reviews = results["review_personas"]  # 10 specialized reviews
```

## 🔧 Core Components

### src/config.py - Configuration & Model Management

Unified interface for configuration loading:

```python
from src.config import get_model, get_research_model, get_logger

# Get models
write_model = get_model()           # Gemini 2.5 Flash (0.7°)
research_model = get_research_model()  # Gemini 2.5 Pro (0.3°)

# Get configuration
pipeline_config = get_pipeline_config()
agents_config = get_agents_config()

# Get logging
logger = get_logger(__name__)
logger.info("Pipeline iniciado")
```

### src/agents.py - 25 Agent Definitions

All agents created from specs/agents.yaml specifications:

```python
from src.agents import create_ideation_agent
from src.config import get_model

model = get_model()
agent = create_ideation_agent(model)

# Execute agent
response = agent.invoke({
    "messages": [{"role": "user", "content": query}]
})
```

### src/tools.py - 30+ Tool Definitions

Tools organized by pipeline stage:

**Stage 1 - Ideation Tools**:
- `search_knowledge_base()` - Knowledge retrieval
- `retrieve_rag_context()` - RAG context

**Stage 2 - Title Tools**:
- `generate_amazon_optimized_title()` - Market-optimized titles
- `validate_title_seo()` - SEO validation

**Stage 3 - Structure Tools**:
- `generate_outline()` - Hierarchical outlines
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

**Stage 7 - Finalization Tools**:
- `generate_cover()` - Cover design
- `generate_kdp_metadata()` - KDP metadata

**Stage 9 - Publication Tools**:
- `export_to_docx()` - Word export
- `export_to_epub()` - EPUB export
- `export_to_pdf()` - PDF export
- `export_to_json()` - JSON export

### src/input_validator.py - Input Validation

Validates `input/book_input.yaml` and generates `specs/book.yaml`:

```python
from src.input_validator import validate_book_input

# Validate and get merged configuration
config = validate_book_input()

# config contains:
# {
#   'metadata': {...},
#   'parameters': {...},
#   'stages': {...}
# }
```

## 💡 Usage Examples

### Example 1: Full Pipeline Execution

```python
from src.input_validator import validate_book_input
from src.main import run_ebook_pipeline

# Validate input (loads input/book_input.yaml, merges with defaults)
config = validate_book_input()

# Run complete 9-stage pipeline
results = run_ebook_pipeline(**config)

print(f"Stage 1 (Ideation): {results['ideation']}")
print(f"Stage 2 (Titles): {results['title']}")
print(f"Stage 5 Reviews: {results['review_personas'].keys()}")
```

### Example 2: Single Agent Execution

```python
from src.agents import create_ideation_agent
from src.config import get_model

model = get_model()
agent = create_ideation_agent(model)

query = """
Define the central idea for a technical ebook:
Topic: Machine Learning in Healthcare
Target Audience: Healthcare professionals
Target Word Count: 12000
"""

response = agent.invoke({
    "messages": [{"role": "user", "content": query}]
})
output = response["messages"][-1].content
print(output)
```

## 🧠 LangChain 1.0+ Integration

Built on LangChain 1.0+ with native patterns:

### Dual-Model Strategy

**Writing & Revision Model**: Gemini 2.5 Flash
- Purpose: Fast, creative text generation
- Temperature: 0.7 (balanced creativity/consistency)
- Usage: Writing, reviews, summary generation

**Research & Analysis Model**: Gemini 2.5 Pro
- Purpose: Deep analysis, RAG retrieval, semantic search
- Temperature: 0.3 (focused for RAG accuracy)
- Usage: External RAG, research analysis, validation

### Tool Definition Pattern

```python
from langchain.tools import tool

@tool
def my_tool(param: str) -> str:
    """Tool description."""
    return "Tool result"
```

### Agent Creation Pattern

```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="Clear role and responsibility..."
)
```

## 🔗 RAG Integration (Supabase)

Integration points for Retrieval-Augmented Generation:

```python
from langchain.vectorstores import PGVectorStore

# Setup connection
vector_store = PGVectorStore.connect_from_documents(
    connection_string="postgresql+psycopg://user:password@host/db",
    documents=documents,
    embedding=embeddings,
)

# Use in agents
context = vector_store.similarity_search(query, k=3)
```

## 🔐 Security & Compliance

### Standards Implemented

- **LGPD**: Brazilian data protection compliance
- **HIPAA**: Medical content disclaimer validation
- **KDP**: Amazon publication standards
- **Ethics**: Bias detection and AI ethics validation

### Best Practices

- Store API keys in environment variables (.env)
- Use virtual environments
- Validate all inputs before processing
- Implement audit logging for sensitive operations

## 📊 System Architecture

```
┌────────────────────────────────────────────────┐
│         EBOOK GENERATOR 1.0                    │
├────────────────────────────────────────────────┤
│                                                │
│  ORCHESTRATION LAYER                           │
│  ├─ run_ebook_pipeline()                      │
│  └─ Input validation → specs/book.yaml        │
│                                                │
│  AGENT LAYER (25 agents)                       │
│  ├─ 9 Main Pipeline Agents                     │
│  ├─ 10 Review Personas                         │
│  └─ 5 Virtual Readers                          │
│                                                │
│  TOOL LAYER (30+ tools)                        │
│  ├─ Generation Tools                           │
│  ├─ Review Tools                               │
│  ├─ Validation Tools                           │
│  └─ Export Tools                               │
│                                                │
│  MODEL LAYER                                   │
│  ├─ LangChain 1.0+                             │
│  ├─ Gemini 2.5 Flash (0.7°) + Pro (0.3°)      │
│  └─ RAG Backend (Supabase pgvector)            │
│                                                │
│  CONFIGURATION LAYER (All YAML, no hardcoding) │
│  ├─ specs/pipeline.yaml (9 stages)             │
│  ├─ specs/agents.yaml (25 agents)              │
│  ├─ specs/config.yaml (messages)               │
│  ├─ specs/models.yaml (AI config)              │
│  └─ specs/tools.yaml (30+ tools)               │
│                                                │
└────────────────────────────────────────────────┘
```

## 📚 Documentation

### Key Files

- `README.md` - This file (complete documentation)
- `.github/copilot-instructions.md` - Code standards
- `docs/PRD.md` - Product Requirements Document
- `docs/ARCHITECTURE.md` - Technical Architecture
- `specs/README.md` - Configuration documentation

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=src tests/
```

## 📝 License

MIT License - see LICENSE file for details.

## 👤 Author

**Igor Medeiros**
- GitHub: [@igormedeiros](https://github.com/igormedeiros)

## 🔗 Links

- [LangChain Documentation](https://python.langchain.com)
- [Google Generative AI](https://ai.google.dev)
- [Supabase Documentation](https://supabase.com/docs)
- [Amazon KDP](https://kdp.amazon.com)

---

**Version**: 1.0  
**Last Updated**: November 12, 2025  
**Status**: Production Ready ✅
