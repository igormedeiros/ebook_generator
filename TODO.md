## CORE AGENTS (9 + 10 + 5 = 25 agents)[ ] Add Stage 4A: Deep Research Agent to agents.py

[ ] Complete agents.py: Implement create_ideation_agent() with real logic from agents.yaml spec[ ] Create 4 Stage 4A tools (query_context7_mcp, perform_deep_research, vectorize_research, store_in_rag_external)

[ ] Complete agents.py: Implement create_title_agent() with real logic[ ] Create 5 virtual reader agents (curious_beginner, technical_professional, didactic_educator, domain_specialist, reflective_reader)

[ ] Complete agents.py: Implement create_structure_agent() with real logic[ ] Implement execute_critical_reading_iterations() with 3-cycle loop

[ ] Complete agents.py: Implement create_deep_research_agent() with Context7 MCP integration[ ] Create 5 new review personas (author_stories, author_positioning, author_vision, examples_exercises, research_references)

[ ] Complete agents.py: Implement create_chapter_agent() with RAG research integration[ ] Update main.py for 9-stage pipeline with Stage 4A and Stage 6

[ ] Complete agents.py: Implement create_review_coordinator_agent() with 10 persona execution[ ] Update docstring in main.py (8→9 stages, 5→10 personas)

[ ] Complete agents.py: Implement create_critical_reading_coordinator_agent() with simple iteration loop (1 cycle)[ ] Verify config.py dual-model configuration (Flash 0.7 + Pro 0.3)

[ ] Complete agents.py: Implement create_editing_agent() with formatting logic[ ] Update __init__.py exports for all 25 agents and 30+ tools

[ ] Complete agents.py: Implement create_finalization_agent() with cover and metadata[ ] Implement aggregate_review_feedback() tool

[ ] Complete agents.py: Implement create_publication_agent() with export logic[ ] Implement identify_critical_issues() tool

[ ] Complete agents.py: Implement 10 review persona agents (use personas from agents.yaml)[ ] Implement prioritize_revisions() tool

[ ] Complete agents.py: Implement 5 virtual reader agents (use virtual_readers from agents.yaml)[ ] Implement apply_iterative_revisions() tool

[ ] Complete agents.py: Implement execute_agent() and execute_review_personas() helpers[ ] Create corresponding tools for 5 new review personas

[ ] Integrate RAG author knowledge retrieval in new personas

## TOOLS (30+)[ ] Test 9-stage pipeline with sample data

[ ] Complete tools.py: Implement get_ideation_tools() - search_knowledge_base, retrieve_rag_context[ ] Verify Context7 MCP integration feasibility

[ ] Complete tools.py: Implement get_title_tools() - generate_amazon_optimized_title, validate_title_seo[ ] Add GitHub examples/exercises validation

[ ] Complete tools.py: Implement get_structure_tools() - generate_outline, count_words[ ] Create md_parser.py module

[ ] Complete tools.py: Implement get_deep_research_tools() - query_context7_mcp, vectorize_research, store_in_rag[ ] Implement parse_spec_file() for .md specification parsing

[ ] Complete tools.py: Implement get_chapter_writing_tools() - retrieve_rag_research, format_markdown, validate_content[ ] Setup Supabase rag_external table with pgvector

[ ] Complete tools.py: Implement get_review_tools() with 10+ review tools for personas[ ] Implement retrieve_author_context() with similarity search

[ ] Complete tools.py: Implement get_editing_tools() - format_markdown, validate_structure[ ] Update create_chapter_agent() to use RAG autoral

[ ] Complete tools.py: Implement get_finalization_tools() - generate_cover, generate_kdp_metadata[ ] Integrate Gemini 2.5 Pro for external research

[ ] Complete tools.py: Implement get_publication_tools() - export_to_docx, export_to_epub, export_to_pdf, export_to_json[ ] Create code_validator_agent.py

[ ] Implement extract_code_blocks() from chapters

## PIPELINE ORCHESTRATION[ ] Create aesthetic_editor_agent.py

[ ] Complete main.py: Implement run_ebook_pipeline() sequential execution of all 9 stages[ ] Implement heading hierarchy validation

[ ] Complete main.py: Ensure stages 1-3 flow correctly (ideation → titles → structure)[ ] Create cover_generator_agent.py

[ ] Complete main.py: Ensure stages 4A & 4B flow correctly (deep research → chapter writing)[ ] Integrate with cover generation API

[ ] Complete main.py: Ensure stage 5 collects feedback from 10 review personas[ ] Create tests/ directory structure

[ ] Complete main.py: Ensure stage 6 simple iteration with 5 virtual readers (1 cycle only)[ ] Implement test_deep_research_agent.py

[ ] Complete main.py: Ensure stages 7-9 flow correctly (editing → finalization → publication)[ ] Implement test_critical_reading.py

[ ] Complete main.py: Add proper logging at each stage using get_logger()[ ] Implement test_review_personas.py

[ ] Setup pytest coverage (target: 80%+)

## INPUT VALIDATION[ ] Create MD_INPUT_GUIDE.md

[ ] Complete input_validator.py: Implement validate_book_input() with mandatory field checks[ ] Create AUDIT_REPORT.md (implementation gaps)

[ ] Complete input_validator.py: Implement merge input/book_input.yaml with pipeline.yaml defaults[ ] Create DEPLOYMENT.md

[ ] Complete input_validator.py: Implement interactive prompts for missing/invalid fields[ ] Create app.py with FastAPI setup

[ ] Complete input_validator.py: Implement generate specs/book.yaml at runtime[ ] Implement POST /ebook/generate endpoint

[ ] Implement GET /ebook/{id}/status

## RAG INTEGRATION[ ] Add API key authentication

[ ] Setup Supabase connection in config.py with pgvector support[ ] Create Dockerfile

[ ] Implement simple rag_external table operations (store and retrieve)[ ] Setup GitHub Actions CI/CD

[ ] Implement retrieve_rag_external() for vectorized research search[ ] Implement structured logging

[ ] Implement query to author knowledge tables (rag_author_stories, rag_author_positioning, rag_author_vision)[ ] Add execution metrics tracking

[ ] Implement performance monitoring

## CONFIGURATION & UTILITIES[ ] Implement batch processing for multiple ebooks

[ ] Update config.py: Verify get_agent_for_stage() maps stages to agent IDs correctly[ ] Create custom agent template system

[ ] Update config.py: Ensure dual-model setup works (Flash 0.7 + Pro 0.3)[ ] Build analytics dashboard

[ ] Update __init__.py: Export all public functions from agents, tools, config, main, input_validator[ ] Add multi-language support

[ ] Verify all YAML files load correctly: pipeline.yaml, agents.yaml, config.yaml, models.yaml, tools.yaml

## TESTING (BASIC)
[ ] Create tests/ directory and __init__.py
[ ] Create tests/test_config.py: Test YAML loading and configuration access
[ ] Create tests/test_input_validator.py: Test input validation and merging
[ ] Create tests/test_agents.py: Test agent creation and execute_agent() function
[ ] Create tests/test_pipeline.py: Test complete pipeline with minimal sample data
[ ] Run all tests: Verify no import errors and basic functionality works

## DOCUMENTATION & STANDARDS
[ ] Update .github/copilot-instructions.md: Add "TODO.md Workflow" section (see template below)
[ ] Update .github/copilot-instructions.md: Clarify "Always commit after completing tasks" requirement
[ ] Verify README.md reflects current 9-stage pipeline architecture
[ ] Verify copilot-instructions.md matches actual implementation patterns

## FINAL COMMIT
[ ] git add -A && git commit -m "feat: implement core agents, tools, and 9-stage pipeline"
