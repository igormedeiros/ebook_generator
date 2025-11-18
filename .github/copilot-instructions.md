# Copilot Instructions - Ebook Generator 1.0

**Author:** Igor Medeiros  
**Date:** November 10, 2025  
**Version:** 1.0

This file documents the coding standards and best practices for all code agents in the **Ebook Generator 1.0** project, based on the PRD v1.0. Follow these guidelines strictly in all code generation, refactoring, and implementation tasks.

---

## � TODO.md Workflow

**CRITICAL**: This workflow must be followed for ALL multi-step work:

### Format Rules
- TODO.md contains ONLY tasks with checkboxes: `[ ] Task description`
- Format for completed tasks: `[x] Task description`
- NO summaries, no status reports, no progress descriptions
- Plain text, no Markdown formatting except checkbox syntax
- One task per line

### Task Management Workflow
1. **When starting a work session**: Read TODO.md to understand pending tasks
2. **Before implementing a task**: Update the checkbox to `[x]` (completed) IMMEDIATELY after finishing
3. **After each task completion**: 
   - Mark it as `[x]` in TODO.md
   - Make a focused git commit with that task
   - Do NOT batch multiple tasks into one commit
4. **Last task in TODO.md**: Always `[ ] git add -A && git commit -m "..."` (the final commit)
5. **After completing ALL tasks**: Push to remote only when user explicitly requests

### Important Reminders
- **NEVER** add summary sections explaining work done
- **NEVER** add progress reports or narrative descriptions
- **NEVER** batch completions of multiple tasks
- Keep the file clean and focused on actionable tasks
- Each git commit corresponds to 1-3 completed tasks (topic-related)

### Example Workflow
```
1. User: "Implement stage 1-3 agents"
   
2. You update TODO.md: Mark 3 agent tasks as in-progress
   - Start first agent implementation
   
3. After completing ideation_agent:
   - Update TODO.md: [x] Complete agents.py: Implement create_ideation_agent()
   - Commit: "feat: implement ideation_agent with spec-driven logic"
   
4. After completing title_agent:
   - Update TODO.md: [x] Complete agents.py: Implement create_title_agent()
   - Commit: "feat: implement title_agent"
   
5. Continue for each task...
   
6. After ALL tasks: 
   - Final commit: "feat: complete core agents, tools, and pipeline"
   - Wait for user to request push
```

### Commit Message Convention
- Use semantic commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
- Be specific about what was done
- Reference completed tasks when relevant
- Example: `feat: implement stage 4A deep research agent with Context7 MCP`

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
- All comments must be Portuguese
- All docstrings must be Portuguese
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

## File Organization

```
src/
├── main.py               # Pipeline orchestration - entry point for ebook generation
├── agents.py             # Writer agent using LangChain 1.0+ with Gemini 2.5 Flash
├── tools.py              # All tool implementations with @tool decorator
├── config.py             # Configuration, logging, models, YAML loading
├── input_validator.py    # Input validation and interactive prompts
├── llm_fallback.py       # LLM fallback mechanism
├── seed_supabase.py      # Script to seed Supabase RAG tables
└── tests/                # Test modules

specs/
├── pipeline.yaml         # 9-stage parameters with agent ID mappings
├── agents.yaml           # 25 independent agent specifications (main + review + readers)
├── config.yaml           # Portuguese strings and messages (centralized)
├── models.yaml           # Gemini model configuration
├── tools.yaml            # Tool specifications (30+)
├── brd.yaml              # Book content structure and metadata
└── README.md             # Specs documentation

input/
└── book_input.yaml       # User-provided book specification (mandatory)

docs/
├── PRD.md                # Product Requirements Document (v1.0)
└── ARCHITECTURE.md       # Technical Architecture (v1.0)
```

### Package Initialization & Entry Points

1. **src/ IS a Python package** with `__init__.py` for re-exports
2. **Entry Point**: `src/main.py` with `if __name__ == "__main__"` block
3. **Execution Methods**:
   ```bash
   # ✅ CORRECT - Primary method
   uv run python -m src.main
   
   # ✅ CORRECT - Also works with __init__.py
   uv run python src/main.py
   ```

4. **Import Pattern**:
   ```python
   # ✅ Good (in src/ files)
   from langchain.agents import create_agent
   from .config import get_model
   from .tools import get_all_tools
   
   # ✅ Good (from root level or external scripts)
   from src.config import get_model
   from src.main import generate_ebook
   
   # ❌ NEVER (src in imports from src/ files)
   from src.config import get_model  # WRONG in src/ files
   
   # ❌ Avoid
   from langchain.agents import *
   ```

5. **__init__.py Pattern**:
   - Re-exports main functions for convenience
   - Allows both `python -m src.main` and `python src/main.py`
   - Keeps imports clean and simple

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

## Dependency Management

**Tool**: `uv` (not pip or pip-tools)

All Python package management uses `uv` for faster, more reliable dependency resolution:

```bash
# Install dependencies from pyproject.toml
uv sync

# Add a new package
uv add package_name

# Update all packages
uv lock
```

**Never use**:
- `pip install`
- `poetry install`
- `pip-tools`

All dependencies are declared in `pyproject.toml` and managed via `uv`.

## Python Execution

**Always use `uv` to execute Python code**:

```bash
# Run a script
uv run script.py

# Run tests
uv run pytest tests/

# Run a module
uv run -m module_name

# Run with arguments
uv run script.py --arg1 value1
```

**Benefits**:
- Ensures correct virtual environment is used
- Consistent execution across all environments
- Automatic dependency resolution
- No need to manually activate venv

**Never use**:
- `python script.py` (incorrect environment)
- `/path/to/venv/bin/python script.py` (brittle paths)
- Direct Python invocation without `uv`

All Python execution in the project must use `uv run` to ensure reproducibility and correct environment isolation.

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
- Always use relative imports for local modules (never use `src` in imports)

```python
# ✅ Good (in src/ files)
from langchain.agents import create_agent
from .config import get_model
from .tools import get_all_tools

# ✅ Good (from root level)
from src.config import get_model
from src.tools import get_all_tools

# ❌ NEVER (src in imports from src/ files)
from src.config import get_model  # WRONG - this creates import errors
from src.tools import get_all_tools  # WRONG

# ❌ Avoid
from langchain.agents import *
import *
```

**CRITICAL RULE**: When writing code in `src/` module files:
- Use relative imports: `from .config import ...`
- NEVER use `from src.config import ...` in src/ files
- Use `from src.X import ...` only from root-level scripts (main.py, tests, etc.)

## Testing & Validation

Before committing code:
1. Verify all imports work correctly
2. Check for syntax errors using `pylance`
3. Test agent execution with sample queries
4. Validate tool output formats
5. Ensure all documentation is complete

### Important: Skip Testing and Documentation Tasks

**CRITICAL**: Do NOT implement testing or documentation tasks unless explicitly requested by the user.

**Task Skipping Rules**:
- Skip all tasks in "TESTING (BASIC)" section of TODO.md unless user explicitly requests
- Skip all tasks in "DOCUMENTATION & STANDARDS" section unless user explicitly requests  
- User will request explicitly: "add tests", "create tests", "implement testing", "add documentation", etc.
- If user says "resolve all TODO tasks", skip testing and documentation - implement core features only

**Exception**: If user explicitly says "implement all tasks including tests and docs", then proceed with all tasks.

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

----

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

### CRITICAL: No Communication of Work Done

**⚠️ CRITICAL RULE - ALWAYS ENFORCE ⚠️**

**NEVER** generate summaries, status reports, or narratives about work completed unless **explicitly requested by the user**.

This includes:
- ❌ "Here's what I did..." summaries
- ❌ "In this session we accomplished..." reports
- ❌ "I've implemented X, Y, Z..." lists
- ❌ "Progress update: 5/10 tasks completed"
- ❌ "The work is complete. Here's what was done:"
- ❌ Explanations of changes made (unless user asks specifically)

**The ONLY exception**: User explicitly requests:
- "summarize what you did"
- "give me a status report"
- "what was completed?"
- "explain the changes"
- Similar explicit requests

**Correct behavior**:
1. Complete work silently
2. Update TODO.md checkboxes
3. Make git commits with descriptive messages
4. Return to user with short confirmation (if needed) or just finish

**Example of WRONG output** (never do this):
```
✅ COMPLETED WORK SUMMARY
- Implemented LLM fallback mechanism
- Added Groq integration
- Updated 3 files
- Made 1 git commit
[... long explanation ...]
```

**Example of RIGHT output** (do this):
```
Done. Fallback mechanism implemented and committed.
```

### Commit Workflow
- After completing tasks from TODO.md: **Always commit changes** with descriptive message
- Format: `git commit -m "feat/fix: description of completed tasks"`
- Reference completed tasks in commit message when relevant
- **NEVER push** without explicit user request
- Push only when user asks: "push", "make push", "upload to remote", etc.
- Workflow: Complete tasks → Update TODO.md checkboxes → Commit → Await push instruction

---

## CRITICAL Communication Rules

**⚠️ ENFORCE THESE STRICTLY ⚠️**

### Never Generate Unsolicited Summaries

**NEVER** create work summaries, progress reports, or status updates unless explicitly requested.

**What triggers explicit requests**:
- "summarize"
- "status"
- "progress"
- "what did you do"
- "explain the changes"
- "give me a report"
- Similar questions from user

**All other times**: Work silently, commit with descriptive messages, wait for instructions.

### Silent Completion Pattern

When completing work WITHOUT explicit request for summary:
1. ✅ Do the work
2. ✅ Update TODO.md
3. ✅ Make descriptive git commit
4. ✅ Brief confirmation only: "Done." or "Committed."
5. ❌ NO explanations, no lists, no narratives

### When to Communicate

**Communicate when**:
- User asks explicitly
- Critical errors occur
- User's attention needed
- Blocking issues found

**Don't communicate when**:
- Completing routine tasks
- Implementing features
- Running tests
- Making commits
- Updating configurations
