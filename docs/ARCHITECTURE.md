# Technical Architecture – Automated eBook Generator

**Ebook Generator 1.0 - Technical Architecture Specification**

**Version**: 1.0  
**Last Updated**: November 13, 2025  

## Related Documentation

- **[Product Requirements Document (PRD.md)](./PRD.md)** - Business objectives, features, and success metrics
- **[This Architecture Document](./ARCHITECTURE.md)** - Technical stack, components, and execution flow
- **[Copilot Instructions (.github/copilot-instructions.md)](../.github/copilot-instructions.md)** - Coding standards and implementation details

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

### 2.1 Configuration System (`specs/`)

All pipeline parameters are externalized to YAML configuration files. This parameter-driven architecture allows for flexible and reusable components.

```
specs/
├── pipeline.yaml         # 9-stage definitions with agent mappings
├── agents.yaml           # 25 independent agent specifications
├── config.yaml           # Portuguese strings, messages, labels
├── models.yaml           # Gemini model configuration
├── tools.yaml            # 30+ tool specifications
├── personas.yaml         # 10 review personas + 5 virtual readers
├── book.yaml             # Generated from input validation (gitignore)
└── README.md             # Configuration documentation
```

**Key Principle**: **Agents are defined independently of stages**
- `agents.yaml` contains all agent specifications without stage associations.
- `pipeline.yaml` defines the 9 stages with parameters and references agents by their ID.
- This mapping allows agents to be reusable and reconfigurable without altering the pipeline structure.

**Key Files**:

1.  **`pipeline.yaml`**: Defines the 9 pipeline stages, their parameters, and the `agent` ID responsible for each stage.
2.  **`agents.yaml`**: Contains specifications for all 25 agents (9 main pipeline, 10 review personas, 5 virtual readers).
3.  **`config.yaml`**: Centralizes all user-facing strings (in Portuguese) for the TUI, including messages, prompts, and labels.
4.  **`models.yaml`**: Configures the Gemini models (Flash and Pro) with their respective settings (temperature, top_p, etc.).
5.  **`tools.yaml`**: Specifies the 30+ tools available to the agents, organized by category.
6.  **`personas.yaml`**: Details the 10 review personas and 5 virtual readers, including their expertise and evaluation criteria.
7.  **`book.yaml`**: Auto-generated file that merges user input with pipeline defaults. It is not committed to version control.

### 2.2 `src/` Directory

The `src/` directory contains the core application logic.

```
src/
├── main.py               # Pipeline orchestration (9 stages)
├── agents.py             # All agent definitions
├── tools.py              # All tool definitions
├── config.py             # Configuration, logging, models, YAML loading
├── input_validator.py    # Input validation and interactive prompts
└── __init__.py           # Package initialization
```

-   **`main.py`**: Orchestrates the 9-stage ebook generation pipeline.
-   **`agents.py`**: Contains the functions that create the LangChain agents.
-   **`tools.py`**: Defines the tools that agents can use.
-   **`config.py`**: Loads configurations from the `specs/` directory and sets up logging.
-   **`input_validator.py`**: Validates user input and prompts for missing information.
-   **`__init__.py`**: Makes the `src` directory a Python package.

### 2.3 Input Validator (`src/input_validator.py`)

Validates and converts user input to pipeline configuration.

**Validation Flow**:

1.  Load `input/book_input.yaml` (user-provided).
2.  Check for mandatory fields (`topic`, `target_audience`, `word_count_target`).
3.  If fields are missing or invalid, it prompts the user interactively.
4.  Merges validated input with defaults from `specs/pipeline.yaml`.
5.  Generates `specs/book.yaml`.

### 2.4 Configuration Module (`src/config.py`)

Provides a unified interface for loading all configurations from the `specs/` directory. It also handles logging setup using the Rich library for a colorful TUI.

### 2.5 Logging and Output Standards

All output must use the `logging` module and Rich for formatting, not `print()`.

```python
from src.config import get_logger, console

logger = get_logger(__name__)

# Logging with levels
logger.info("Pipeline iniciado")
logger.warning("Aviso importante")
logger.error("Erro na execução")
logger.debug("Detalhes técnicos")

# Rich output for panels
console.print("[bold cyan]Resultado da Revisão[/bold cyan]")
```

---

## 3. RAG Pipeline

### 3.1 Author Knowledge Base (Pre-loaded in Supabase)

-   **`rag_author_stories`**: Personal narratives and experiences.
-   **`rag_author_positioning`**: Market positioning and authority.
-   **`rag_author_vision`**: Values, philosophy, and opinions.

This data is pre-loaded and used by reviewers to ensure the author's voice and perspective are maintained.

### 3.2 External RAG - Deep Research Pipeline

1.  **Stage 3 (Structure)**: The Structure Agent defines the chapters.
2.  **Stage 4A (Deep Research)**: The Deep Research Agent queries the Context7 MCP Server for academic papers, books, and other sources for each chapter. The results are vectorized and stored in the `rag_external` table in Supabase.
3.  **Stage 4B (Chapter Writing)**: The Writer Agent uses the vectorized research from `rag_external` to write the chapters, including citations.
4.  **Stage 5 (Review)**: The Research & References Validator persona verifies the quality and credibility of the cited sources.

### 3.3 Supabase Configuration

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

-- Other rag tables for author knowledge...
```

---

## 4. Execution Sequence

The pipeline consists of 9 stages, executed sequentially:

1.  **Ideation**: Defines the central idea, problem, and audience.
2.  **Title Generation**: Creates 3 Amazon-optimized title options.
3.  **Structure**: Generates a hierarchical table of contents.
4.  **Deep Research & Chapter Writing**:
    -   **4A. Deep Research**: Gathers and vectorizes external knowledge.
    -   **4B. Chapter Writing**: Writes chapters using the research.
5.  **Specialized Review**: 10 specialized personas review the content.
6.  **Critical Reading & Iteration**: 5 virtual readers provide feedback in 3 cycles.
7.  **Editing**: Finalizes formatting and validation.
8.  **Finalization**: Generates a cover concept and metadata.
9.  **Publication**: Exports the ebook to DOCX, EPUB, PDF, and JSON.

---

## 5. Gemini Model Roles

-   **Gemini 2.5 Flash (Fast Writing)**: Used for creative writing, reviews, and summaries. (Temperature: 0.7)
-   **Gemini 2.5 Pro (Deep Research)**: Used for research, analysis, and factual validation. (Temperature: 0.3)

---
## 6. Review and Reading Personas

### Review Personas (10)

1.  **Technical Reviewer**: Validates code and technical accuracy.
2.  **Editorial Reviewer**: Checks for clarity, tone, and flow.
3.  **Content Stylist**: Ensures formatting consistency.
4.  **Governance QA**: Verifies compliance and metadata.
5.  **Ethics Validator**: Detects bias and ethical issues.
6.  **Author Stories & Didactics Reviewer**: Balances author stories with learning objectives.
7.  **Author Positioning Reviewer**: Validates the author's market positioning.
8.  **Author Vision & Opinions Reviewer**: Aligns content with the author's worldview.
9.  **Examples & Exercises Code Reviewer**: Executes and collects code examples.
10. **Research & References Validator**: Validates the credibility of sources.

### Critical Reading Personas (5)

1.  **Curious Beginner**: Represents a newcomer to the topic.
2.  **Technical Professional**: A senior developer who validates technical depth.
3.  **Didactic Educator**: A teacher who focuses on pedagogical structure.
4.  **Domain Specialist**: An expert in a related field.
5.  **Reflective Reader**: A general reader who evaluates the emotional impact.

---

## 7. External Dependencies

-   **Google Gemini API**: For LLMs and embeddings.
-   **Supabase API**: For storage and vector operations.
-   **Context7 MCP Server**: For semantic knowledge base retrieval.
-   **GitHub API** (optional): For managing code examples.
-   **Pandoc**: For format conversion.