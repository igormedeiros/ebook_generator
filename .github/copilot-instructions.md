# Copilot Instructions - Ebook Generator 1.0

**Author:** Igor Medeiros  
**Date:** November 10, 2025  
**Version:** 1.0

This file documents the coding standards and best practices for all code agents in the **Ebook Generator 1.0** project, based on the PRD v1.0. Follow these guidelines strictly in all code generation, refactoring, and implementation tasks.

---

## 📘 Project Overview

**Ebook Generator 1.0** is a multi-agent AI-powered editorial automation platform that transforms raw ideas into publication-ready ebooks using:

- **LangChain 1.0+** for orchestration
- **Gemini 2.5 Flash** for writing and textual revision (temp: 0.7)
- **Gemini 2.5 Pro** for research and contextual analysis / RAG (temp: 0.3)
- **Supabase + pgvector** for semantic search and embeddings
- **Pandoc** for format conversion (DOCX, EPUB, PDF)
- **MD Parser** for flexible input via .md specification files
- **RAG Autoral** for author stories and opinions integration
- **Multi-Persona Review** with 5 specialized reviewers
- **KDP Integration** for direct Amazon publication

---

## Language Standards

### Code Language: 100% English
- All variable names must be English
- All function names must be English
- All class names must be English
- All comments and docstrings must be English
- Exception: String content can be Portuguese when appropriate for user-facing text

### String Content: Flexible
- User-facing messages may use Portuguese
- Documentation strings should use English
- Error messages should use English for clarity

### Comments & Documentation
- All comments must be English
- All docstrings must be English
- Use clear, concise technical language

## LangChain 1.0+ Standards

### Tool Definition Pattern
Use the native `@tool` decorator from LangChain 1.0+:

```python
from langchain.tools import tool

@tool
def my_tool(param: str) -> str:
    """
    Brief description of what the tool does.
    
    Args:
        param: Description of the parameter
    
    Returns:
        str: Description of the return value
    """
    # Implementation here
    return result
```

### Structured Output Pattern
For tools returning both narrative and structured data:

```python
@tool(response_format="content_and_artifact")
def my_structured_tool(param: str) -> tuple[str, dict]:
    """
    Tool returning both text and structured data.
    
    Returns:
        tuple[str, dict]: (narrative_text, structured_data)
    """
    narrative = "Explanation of the output..."
    structured = {"key": "value", "data": [...]}
    return narrative, structured
```

### Agent Creation Standard
Use `create_agent()` function with structured parameters:

```python
from langchain.agents import create_agent

def create_my_agent(model: ChatGoogleGenerativeAI):
    """
    Description of agent purpose and responsibility.
    """
    return create_agent(
        model=model,
        tools=get_my_tools(),
        system_prompt="""Clear role definition.
Your responsibility is to...

Key behaviors:
1. Behavior 1
2. Behavior 2

Provide structured output..."""
    )
```

### Agent Execution Standard
Use consistent execution interface:

```python
def execute_agent(agent, query: str) -> str:
    """Execute an agent with a query and return the response."""
    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return response["messages"][-1].content
```

## Tool Organization

### Tool Collection Functions
Organize tools by pipeline stage:

```python
def get_ideation_tools() -> list:
    """Return tools used in Stage 1: Ideation."""
    return [
        search_knowledge_base,
        retrieve_rag_context,
    ]

def get_title_tools() -> list:
    """Return tools used in Stage 2: Title Generation."""
    return [
        generate_amazon_optimized_title,
        validate_title_seo,
    ]

def get_all_tools() -> list:
    """Return all available tools across all stages."""
    return (
        get_ideation_tools() +
        get_title_tools() +
        get_structure_tools() +
        # ... other stage tools
    )
```

## System Prompt Structure

Every agent must have a clear system prompt with:

1. **Role Definition**: What the agent is
2. **Responsibility**: What the agent does
3. **Focus Areas**: Key areas of expertise (numbered list)
4. **Process**: Step-by-step execution approach
5. **Output Format**: What output is expected

Example template:

```
You are the [Agent Name] - a [specialty] expert.
Your responsibility is to [primary goal].

Focus Areas:
1. [Focus 1]
2. [Focus 2]
3. [Focus 3]

Process:
- Step 1
- Step 2
- Step 3

Output Format:
[Specify expected format]
```

## Pipeline Stages

The Ebook Generator follows this 9-stage pipeline with independent agent specifications:

**Key Architecture Pattern**: Agents are defined independently in `specs/agents.yaml` (not per-stage). Pipeline stages in `specs/pipeline.yaml` reference agents via the `agent` field.

### Stage 1: Ideation
- Agent ID: `ideation_agent` (specs/agents.yaml > main_pipeline_agents)
- Config: `specs/pipeline.yaml` > `stage_1_ideation`
- Agent Model: Gemini 2.5 Flash (0.7 temperature)
- Output: Central idea, problem definition, target audience

### Stage 2: Title Generation
- Agent ID: `title_agent`
- Config: `specs/pipeline.yaml` > `stage_2_title`
- Agent Model: Gemini 2.5 Flash
- Output: 3 Amazon-optimized title options

### Stage 3: Structure
- Agent ID: `structure_agent`
- Config: `specs/pipeline.yaml` > `stage_3_structure`
- Agent Model: Gemini 2.5 Flash
- Output: Hierarchical table of contents in Markdown

### Stage 4A: Deep Research
- Agent ID: `deep_research_agent`
- Config: `specs/pipeline.yaml` > `stage_4a_deep_research`
- Agent Model: Gemini 2.5 Pro (0.3 temperature)
- Tools: Context7 MCP, vectorization, RAG storage
- Output: Vectorized research in rag_external

### Stage 4B: Chapter Writing
- Agent ID: `chapter_writing_agent`
- Config: `specs/pipeline.yaml` > `stage_4b_chapter_writing`
- Agent Model: Gemini 2.5 Flash
- Tools: Writing + RAG integration
- Output: Didactic content chapters

### Stage 5: Specialized Review (10 Personas)
- Agent ID: `review_coordinator_agent`
- Config: `specs/pipeline.yaml` > `stage_5_review`
- Agent Model: Gemini 2.5 Pro
- Review Personas: Technical, Editorial, Stylist, Governance, Ethics, Author Stories, Author Positioning, Author Vision, Code Reviewer, Research Validator
- Output: Structured feedback by persona (10 perspectives)

### Stage 6: Critical Reading & Iteration (3 Cycles)
- Agent ID: `critical_reading_coordinator_agent`
- Config: `specs/pipeline.yaml` > `stage_6_critical_reading`
- Agent Model: Gemini 2.5 Pro
- Virtual Readers: Curious Beginner, Technical Professional, Educator, Specialist, Reflective
- Output: Refined content with reader validation

### Stage 7: Editing
- Agent ID: `editing_agent`
- Config: `specs/pipeline.yaml` > `stage_7_editing`
- Agent Model: Gemini 2.5 Flash
- Output: Validated and formatted document

### Stage 8: Finalization
- Agent ID: `finalization_agent`
- Config: `specs/pipeline.yaml` > `stage_8_finalization`
- Agent Model: Gemini 2.5 Flash
- Output: Cover concept and validated metadata

### Stage 9: Publication
- Agent ID: `publication_agent`
- Config: `specs/pipeline.yaml` > `stage_9_publication`
- Agent Model: Gemini 2.5 Flash
- Tools: Export tools (DOCX, EPUB, PDF, JSON)
- Output: Publication-ready package

## File Organization

```
src/
├── main.py               # Pipeline orchestration (9 stages)
├── agents.py             # All agent definitions (25 agents)
├── tools.py              # All tool definitions (30+ tools)
├── config.py             # Configuration, logging, models, YAML loading
├── input_validator.py    # Input validation and interactive prompts
└── __init__.py           # Package initialization

specs/
├── pipeline.yaml         # 9-stage parameters with agent ID mappings
├── agents.yaml           # 25 independent agent specifications (main + review + readers)
├── config.yaml           # Portuguese strings and messages (centralized)
├── models.yaml           # Gemini model configuration
├── tools.yaml            # Tool specifications (30+)
├── book.yaml             # Generated from input validation (gitignore)
└── README.md             # Specs documentation

input/
└── book_input.yaml       # User-provided book specification (mandatory)

docs/
├── PRD.md                # Product Requirements Document (v1.0)
└── ARCHITECTURE.md       # Technical Architecture (v1.0)
```

### Package Initialization

**Important**: `__init__.py` files must NEVER be empty:

1. **Purpose**: Export public API of each package
2. **Content**: Include `__all__` list with exported names
3. **Documentation**: Include module docstring explaining package purpose
4. **Example**:
   ```python
   """
   Ebook Generator 1.0 - Multi-agent editorial automation platform.
   """
   from config import get_model, get_research_model
   from config import (
       get_logger, 
       get_config, 
       get_pipeline_config,
       console
   )
   from agents import create_ideation_agent, ...
   from main import run_ebook_pipeline

   __version__ = "1.0.0"
   __all__ = [
       "get_model",
       "get_research_model",
       "get_logger",
       "console",
       "create_ideation_agent",
       "run_ebook_pipeline",
   ]
   ```

3. **Never**: Leave `__init__.py` blank or with only comments
4. **Rationale**: Clear API surface, better IDE support, explicit exports

### Logging and Output Standards

**All output must use logging and Rich, NOT print()**:

# Logging and Output Standards

**All output must use logging and Rich, NOT print()**:

```python
from src.config import get_logger, console

logger = get_logger(__name__)

# ✅ Logging with levels
logger.info("Pipeline iniciado")           # ✓ Info level
logger.warning("Aviso importante")         # ⚠️ Warning level
logger.error("Erro na execução")           # ❌ Error level
logger.debug("Detalhes técnicos")          # Apenas em modo DEBUG

# ✅ Rich output for panels
print_panel(
    title="Resultado da Revisão",
    content="Feedback consolidado de personas",
    style="cyan"
)

# ❌ NEVER use print()
print("Resultado")  # Incorreto

# ❌ NEVER use console.print() para logs
console.print("Iniciando...")  # Apenas para output estruturado
```

**Logging Levels**:
- `logger.debug()` - Detalhes técnicos e rastreamento
- `logger.info()` - Informações normais de progresso
- `logger.warning()` - Avisos (ex: versões desatualizadas)
- `logger.error()` - Erros na execução
- `logger.critical()` - Falhas críticas que impedem continuação

**Rich Output**:
- `console.print()` - Saída estruturada (tabelas, painéis, etc)
- `print_panel()` - Exibir conteúdo em painel
- `print_table()` - Exibir tabela formatada
- `print_progress()` - Barra de progresso

### Configuration Management

All configurable elements are in `specs/`:

```python
from src.config import (
    get_pipeline_config,
    get_models_config,
    get_personas_config,
    get_tools_config,
    get_message
)
from src.input_validator import validate_book_input

# Load pipeline configuration
pipeline_cfg = get_pipeline_config()
stage_1_params = pipeline_cfg['stages']['stage_1_ideation']['parameters']

# Load Portuguese messages
msg = get_message('pipeline_start')  # "🚀 Iniciando pipeline..."

# Validate user input and generate book config
config = validate_book_input()
book_config = config  # Merged specs/book.yaml equivalent

# Load model configuration
models_cfg = get_models_config()
gemini_flash = models_cfg['models']['write_model']
```

**String Management**:
- **All Portuguese strings go in `specs/config.yaml`**
- No hardcoded strings in code
- Use `get_message(key)` for retrieval
- Exception: Comments and docstrings in English remain in code

### Parameter-Driven Architecture

Pipeline execution is parameter-driven from specs/:

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
    word_count_target=15000
)

# Option 3: Custom overrides via stage_overrides in input
config = validate_book_input()  # includes stage_overrides
result = run_ebook_pipeline(**config)
```
config['input']['word_count_target'] = 50000
result = run_ebook_pipeline(**config['input'])
```

### Documentation Standards

**Important**: The only `.md` file in the project root should be `README.md`. All other documentation must be:

1. **In `docs/` folder**: `prd.md`, `ARCHITECTURE.md` (if needed), etc.
2. **NOT in root**: No `CHANGELOG.md`, `CONTRIBUTING.md`, or other `.md` files in root
3. **Rationale**: Maintains clean root structure, centralizes documentation

This keeps the project root focused on essential files (README, pyproject.toml, requirements.txt, etc.).

## Model Configuration

### Dual-Model Strategy

**Writing & Revision Model**: Gemini 2.5 Flash
- Purpose: Fast, creative text generation and iterative refinement
- Configuration:
  ```python
  write_model = ChatGoogleGenerativeAI(
      model="gemini-2.5-flash",
      temperature=0.7,  # Balanced creativity/consistency
      top_p=0.95,
      top_k=40,
      google_api_key=os.getenv("GOOGLE_API_KEY")
  )
  ```

**Research & Analysis Model**: Gemini 2.5
- Purpose: Deep analysis, RAG context retrieval, semantic search
- Configuration:
  ```python
  research_model = ChatGoogleGenerativeAI(
      model="gemini-2.5",
      temperature=0.3,  # More focused for RAG
      top_p=0.95,
      top_k=40,
      google_api_key=os.getenv("GOOGLE_API_KEY")
  )
  ```

Both models use environment-based API key management and support the LangChain 1.0+ create_agent() standard.

## RAG Integration Points

RAG tools are marked with integration points:

```python
@tool
def retrieve_rag_context(query: str) -> str:
    """
    Retrieve context from Supabase vector store.
    
    TODO: Implement Supabase pgvector integration:
    1. Connect to Supabase with connection string
    2. Use pgvector similarity_search()
    3. Return top-k relevant documents
    """
```

Connection pattern (Supabase):
```python
from langchain.vectorstores import PGVectorStore
vector_store = PGVectorStore.connect_from_documents(
    connection_string="postgresql+psycopg://...",
    documents=docs,
    embedding=embeddings,
)
```

## Error Handling

All functions should include basic error handling:

```python
def my_function(param: str) -> str:
    try:
        # Main implementation
        result = process(param)
        return result
    except ValueError as e:
        return f"Error: Invalid input - {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
```

## Documentation Requirements

Every function must have:
1. **Docstring** with description
2. **Args section** with parameter descriptions
3. **Returns section** with return type and description
4. **Example** (optional but recommended for complex functions)

Example:

```python
def my_function(topic: str, audience: str, word_count: int) -> dict:
    """
    Process topic information and return structured output.
    
    Args:
        topic: The main topic of the ebook
        audience: Target audience segment
        word_count: Target word count goal
    
    Returns:
        dict: Dictionary with processed information including
              'idea', 'problem', 'promise', 'outline'
    
    Example:
        >>> result = my_function("Python", "Developers", 15000)
        >>> result['promise']
        'Learn advanced Python techniques...'
    """
```

## Type Hints

Always use type hints for function parameters and returns:

```python
# ✅ Good
def process_content(text: str, count: int) -> dict:
    pass

# ❌ Avoid
def process_content(text, count):
    pass
```

## Code Style

### Naming Conventions
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Variables: `snake_case`

### Line Length
- Maximum 100 characters per line
- Break long lines with logical continuation

### Imports
- Group imports: standard library, third-party, local
- Use explicit imports over wildcards
- Always use absolute imports

```python
# ✅ Good
from langchain.agents import create_agent
from config import get_model
from tools import get_all_tools

# ❌ Avoid
from langchain.agents import *
import *
```

## Testing & Validation

Before committing code:
1. Verify all imports work correctly
2. Check for syntax errors using `pylance`
3. Test agent execution with sample queries
4. Validate tool output formats
5. Ensure all documentation is complete

## Middleware Patterns (Future)

LangChain 1.0+ supports middleware for aspect-oriented concerns:

```python
from langchain_core.runnables import RunnableConfig

# Pattern for future middleware implementation
class PIIMiddleware:
    """Remove personally identifiable information."""
    pass

class SummarizationMiddleware:
    """Summarize long outputs."""
    pass

class HumanInTheLoopMiddleware:
    """Request human approval before proceeding."""
    pass
```

## Review Personas Specialization

The system integrates **8 specialized review personas** that form the core of textual refinement:

### Technical Reviewer
- **Role**: Python Engineer
- **Focus**: Code quality, framework versions, syntax validation
- **Checks**: LangChain compatibility, example execution, documentation accuracy

### Editorial Reviewer
- **Role**: Communicator
- **Focus**: Clarity, tone, flow, audience alignment
- **Checks**: Readability, emotional connection, narrative progression

### Content Stylist
- **Role**: Editor Literário
- **Focus**: Document structure, formatting consistency, visual hierarchy
- **Checks**: Heading hierarchy, Markdown format, style uniformity

### Governance QA
- **Role**: Compliance Officer
- **Focus**: Framework versions, security, LGPD compliance, metadata
- **Checks**: Version accuracy, security disclaimers, regulatory compliance

### Ethics Validator
- **Role**: AI Ethics Expert
- **Focus**: Bias detection, medical disclaimers, AI ethics principles
- **Checks**: Language bias, required disclaimers, HIPAA/LGPD compliance

### Author Stories & Didactics Reviewer (NEW)
- **Role**: Narrative & Pedagogy Expert
- **Focus**: Balance between author personal stories and learning objectives
- **Checks**: Story relevance, narrative weight, didactic flow, authenticity
- **RAG Integration**: Author Stories knowledge base for context

### Author Positioning Reviewer (NEW)
- **Role**: Marketing & Authority Expert
- **Focus**: Author's market positioning and subject matter expertise
- **Checks**: Positioning clarity, authority prominence, niche distinctiveness
- **RAG Integration**: Author Positioning knowledge base for positioning framework

### Author Vision & Opinions Reviewer (NEW)
- **Role**: Values & Philosophy Expert
- **Focus**: Alignment with author's worldview and core principles
- **Checks**: Vision coherence, opinion authenticity, value alignment
- **RAG Integration**: Author Vision & Opinions knowledge base for philosophical framework

---

## Critical Reading Personas (Virtual Readers)

The system also simulates **5 virtual readers** for iterative feedback:

| Persona | Profile | Validation Focus |
|---------|---------|------------------|
| **Curious Beginner** | New to AI/programming | Clarity, progression, accessibility |
| **Technical Professional** | Senior developer | Depth, relevance, technical accuracy |
| **Didactic Educator** | Teacher/mentor | Pedagogical structure, methodology |
| **Domain Specialist** | Physician, researcher | Application relevance, cross-disciplinary coherence |
| **Reflective Reader** | General audience | Empathy, purpose, emotional impact |

These readers generate independent reports that feed into the refinement loop, conducted by the Coordinator Super Agent through **3 complete iterations**.

## Version Control

- Branch: `develop` for active development
- All code changes must follow these standards
- Use descriptive commit messages
- Reference issues when applicable

## Performance Considerations

- Batch tool calls when possible
- Use RAG context efficiently (top-k parameter)
- Implement caching for repeated queries
- Monitor token usage with Gemini API

## Continuous Integration

All code must pass:
- Syntax validation
- Import validation
- Type hint verification
- Documentation completeness check

## TODO.md Management

### Format Rules
- TODO.md contains ONLY tasks with checkboxes
- Format: `[ ] Task description` (not completed) or `[x] Task description` (completed)
- NO summaries, no status reports, no additional text
- NO narratives about what was done
- Plain text, no Markdown formatting except checkbox syntax
- One task per line

### Important: No Summary Updates
- **NEVER** add summary sections explaining work completed
- **NEVER** add status reports or progress descriptions
- **NEVER** write narrative about implementation
- Only update individual task checkboxes when work is done
- Keep the file clean and focused on actionable tasks

### Commit Workflow
- After completing tasks from TODO.md: **Always commit changes** with descriptive message
- Format: `git commit -m "feat/fix: description of completed tasks"`
- Reference completed tasks in commit message when relevant
- **NEVER push** without explicit user request
- Push only when user asks: "push", "make push", "upload to remote", etc.
- Workflow: Complete tasks → Update TODO.md checkboxes → Commit → Await push instruction

---

## PRD Reference

The complete Product Requirements Document (v1.0) defines:

### 9-Stage Editorial Pipeline
1. **Ideation** - Central idea, problem, audience, transformation promise
2. **Title Generation** - Amazon-optimized titles (3 options)
3. **Structure** - Hierarchical outline scaled to word count
4. **Deep Research** - External RAG with Context7 MCP, vectorized research
5. **Chapter Writing** - Didactic content with research-backed integration
6. **Specialized Review** - 10 specialized review personas
7. **Critical Reading & Iteration** - 5 virtual readers, 3 cycles of refinement
8. **Editing** - Final formatting and validation
9. **Publication** - DOCX, EPUB, PDF, JSON export for KDP

### Dual-Model Architecture
- **Gemini 2.5 Flash** - Writing, creativity, speed (temperature: 0.7)
- **Gemini 2.5 Pro** - Research, analysis, RAG, factuality (temperature: 0.3)
- **Gemini 2.5** - Research, analysis, RAG, factuality (temperature: 0.3)

### Success Criteria
- ≥80% reduction in editorial production time
- ≥95% factuality (via RAG + validation)
- 100% Amazon KDP compatibility
- ≥90% user satisfaction
