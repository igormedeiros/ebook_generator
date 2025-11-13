## PHASE 2: IMPLEMENTATION & BUGFIX

### Agents & Tools (Completed)
[x] 25 agents: ideation, title, structure, deep_research, chapter, 10 reviewers, 5 readers, 2 coordinators
[x] 30+ tools: organized by stage with @tool decorator (LangChain 1.0+)
[x] System prompts: dynamic from agents.yaml specs

### Pipeline Orchestration (Completed)
[x] run_ebook_pipeline(): 9 stages sequential execution
[x] Logging: all stages use get_logger() with Rich output

### Input Validation (Completed)
[x] validate_book_input(): mandatory field checks
[x] Merge input/book_input.yaml + pipeline.yaml defaults
[x] Interactive prompts for missing/invalid fields
[x] Generate specs/book.yaml at runtime

### RAG Integration (Completed)
[x] Supabase pgvector connection in config.py
[x] store_in_rag() and retrieve_rag_external()
[x] Author knowledge tables: rag_author_stories, rag_author_positioning, rag_author_vision

### Configuration & Utils (Completed)
[x] config.py: dual-model setup (Flash 0.7 + Pro 0.3)
[x] get_agent_for_stage(): stages → agent IDs
[x] All YAML files load correctly

## PHASE 2: BUGFIX & CLEAN CODE

### Syntax & Import Errors
[ ] Fix src/__init__.py: Add __all__ exports for agents, tools, config, main, input_validator
[ ] Fix src/main.py: Correct relative imports and module entry point
[ ] Fix execution: Enable `uv run python -m src.main` entry point

### Code Quality - LangChain 1.0+ Alignment
[ ] agents.py: Verify create_agent() pattern matches LangChain v1 spec
[ ] tools.py: Ensure all tools follow @tool decorator pattern
[ ] config.py: Add RunnableConfig support for agent middleware (future)

### Test Execution
[ ] Run: uv run python -m src.main --topic "Python for Data Analysis" --audience "Data Scientists"
[ ] Validate: 9-stage pipeline executes without errors
[ ] Verify: Output JSON contains all stage results

## FINAL COMMIT
[ ] git add -A && git commit -m "fix: resolve import errors and align with LangChain 1.0+ patterns"
