[ ] Add Stage 4A: Deep Research Agent to agents.py
[ ] Create 4 Stage 4A tools (query_context7_mcp, perform_deep_research, vectorize_research, store_in_rag_external)
[ ] Create 5 virtual reader agents (curious_beginner, technical_professional, didactic_educator, domain_specialist, reflective_reader)
[ ] Implement execute_critical_reading_iterations() with 3-cycle loop
[ ] Create 5 new review personas (author_stories, author_positioning, author_vision, examples_exercises, research_references)
[ ] Update main.py for 9-stage pipeline with Stage 4A and Stage 6
[ ] Update docstring in main.py (8→9 stages, 5→10 personas)
[ ] Verify config.py dual-model configuration (Flash 0.7 + Pro 0.3)
[ ] Update __init__.py exports for all 25 agents and 30+ tools
[ ] Implement aggregate_review_feedback() tool
[ ] Implement identify_critical_issues() tool
[ ] Implement prioritize_revisions() tool
[ ] Implement apply_iterative_revisions() tool
[ ] Create corresponding tools for 5 new review personas
[ ] Integrate RAG author knowledge retrieval in new personas
[ ] Test 9-stage pipeline with sample data
[ ] Verify Context7 MCP integration feasibility
[ ] Add GitHub examples/exercises validation
[ ] Create md_parser.py module
[ ] Implement parse_spec_file() for .md specification parsing
[ ] Setup Supabase rag_external table with pgvector
[ ] Implement retrieve_author_context() with similarity search
[ ] Update create_chapter_agent() to use RAG autoral
[ ] Integrate Gemini 2.5 Pro for external research
[ ] Create code_validator_agent.py
[ ] Implement extract_code_blocks() from chapters
[ ] Create aesthetic_editor_agent.py
[ ] Implement heading hierarchy validation
[ ] Create cover_generator_agent.py
[ ] Integrate with cover generation API
[ ] Create tests/ directory structure
[ ] Implement test_deep_research_agent.py
[ ] Implement test_critical_reading.py
[ ] Implement test_review_personas.py
[ ] Setup pytest coverage (target: 80%+)
[ ] Create MD_INPUT_GUIDE.md
[ ] Create AUDIT_REPORT.md (implementation gaps)
[ ] Create DEPLOYMENT.md
[ ] Create app.py with FastAPI setup
[ ] Implement POST /ebook/generate endpoint
[ ] Implement GET /ebook/{id}/status
[ ] Add API key authentication
[ ] Create Dockerfile
[ ] Setup GitHub Actions CI/CD
[ ] Implement structured logging
[ ] Add execution metrics tracking
[ ] Implement performance monitoring
[ ] Implement batch processing for multiple ebooks
[ ] Create custom agent template system
[ ] Build analytics dashboard
[ ] Add multi-language support
