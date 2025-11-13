## CORE AGENTS (9 + 10 + 5 = 25 agents)
[x] Complete agents.py: Implement create_ideation_agent() with real logic from agents.yaml spec
[x] Complete agents.py: Implement create_title_agent() with real logic
[x] Complete agents.py: Implement create_structure_agent() with real logic
[x] Complete agents.py: Implement create_deep_research_agent() with Context7 MCP integration
[x] Complete agents.py: Implement create_chapter_agent() with RAG research integration
[x] Complete agents.py: Implement create_review_coordinator_agent() with 10 persona execution
[x] Complete agents.py: Implement create_critical_reading_coordinator_agent() with simple iteration loop (1 cycle)
[x] Complete agents.py: Implement create_editing_agent() with formatting logic
[x] Complete agents.py: Implement create_finalization_agent() with cover and metadata
[x] Complete agents.py: Implement create_publication_agent() with export logic
[x] Complete agents.py: Implement 10 review persona agents (use personas from agents.yaml)
[x] Complete agents.py: Implement 5 virtual reader agents (use virtual_readers from agents.yaml)
[x] Complete agents.py: Implement execute_agent() and execute_review_personas() helpers

## TOOLS (30+)
[x] Complete tools.py: Implement get_ideation_tools() - search_knowledge_base, retrieve_rag_context
[x] Complete tools.py: Implement get_title_tools() - generate_amazon_optimized_title, validate_title_seo
[x] Complete tools.py: Implement get_structure_tools() - generate_outline, count_words
[x] Complete tools.py: Implement get_deep_research_tools() - query_context7_mcp, vectorize_research, store_in_rag
[x] Complete tools.py: Implement get_chapter_writing_tools() - retrieve_rag_research, format_markdown, validate_content
[x] Complete tools.py: Implement get_review_tools() with 10+ review tools for personas
[x] Complete tools.py: Implement get_editing_tools() - format_markdown, validate_structure
[x] Complete tools.py: Implement get_finalization_tools() - generate_cover, generate_kdp_metadata
[x] Complete tools.py: Implement get_publication_tools() - export_to_docx, export_to_epub, export_to_pdf, export_to_json

## PIPELINE ORCHESTRATION
[x] Complete main.py: Implement run_ebook_pipeline() sequential execution of all 9 stages
[x] Complete main.py: Ensure stages 1-3 flow correctly (ideation → titles → structure)
[x] Complete main.py: Ensure stages 4A & 4B flow correctly (deep research → chapter writing)
[x] Complete main.py: Ensure stage 5 collects feedback from 10 review personas
[x] Complete main.py: Ensure stage 6 simple iteration with 5 virtual readers (1 cycle only)
[x] Complete main.py: Ensure stages 7-9 flow correctly (editing → finalization → publication)
[x] Complete main.py: Add proper logging at each stage using get_logger()

## INPUT VALIDATION
[x] Complete input_validator.py: Implement validate_book_input() with mandatory field checks
[x] Complete input_validator.py: Implement merge input/book_input.yaml with pipeline.yaml defaults
[x] Complete input_validator.py: Implement interactive prompts for missing/invalid fields
[x] Complete input_validator.py: Implement generate specs/book.yaml at runtime

## RAG INTEGRATION
[x] Setup Supabase connection in config.py with pgvector support
[x] Implement simple rag_external table operations (store and retrieve)
[x] Implement retrieve_rag_external() for vectorized research search
[x] Implement query to author knowledge tables (rag_author_stories, rag_author_positioning, rag_author_vision)

## CONFIGURATION & UTILITIES
[x] Update config.py: Verify get_agent_for_stage() maps stages to agent IDs correctly
[x] Update config.py: Ensure dual-model setup works (Flash 0.7 + Pro 0.3)
[x] Update __init__.py: Export all public functions from agents, tools, config, main, input_validator
[x] Verify all YAML files load correctly: pipeline.yaml, agents.yaml, config.yaml, models.yaml, tools.yaml

## TESTING (BASIC)
[x] Create tests/ directory and __init__.py
[x] Create tests/test_config.py: Test YAML loading and configuration access
[x] Create tests/test_input_validator.py: Test input validation and merging
[x] Create tests/test_agents.py: Test agent creation and execute_agent() function
[x] Create tests/test_pipeline.py: Test complete pipeline with minimal sample data
[x] Run all tests: Verify no import errors and basic functionality works

## DOCUMENTATION & STANDARDS
[x] Update .github/copilot-instructions.md: Add "TODO.md Workflow" section (see template below)
[x] Update .github/copilot-instructions.md: Clarify "Always commit after completing tasks" requirement
[x] Verify README.md reflects current 9-stage pipeline architecture
[x] Verify copilot-instructions.md matches actual implementation patterns

## FINAL COMMIT
[x] git add -A && git commit -m "feat: implement core agents, tools, and 9-stage pipeline"
