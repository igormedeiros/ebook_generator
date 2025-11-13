""""""

Main pipeline orchestration for Ebook Generator 1.0.Main entry point for the Ebook Generator 1.0 pipeline.

Orchestrates the 9-stage editorial process with specialized agents and iterative review cycles.

Executes the 9-stage editorial pipeline sequentially:"""

1. Ideation - Generate central idea and problem definition

2. Title Generation - Create Amazon-optimized titlesfrom config import get_model

3. Structure - Build hierarchical outlinefrom agents import (

4A. Deep Research - Gather and vectorize research with Context7 MCP    create_ideation_agent,

4B. Chapter Writing - Write didactic content with RAG integration    create_title_agent,

5. Specialized Review - Collect feedback from 10 review personas    create_structure_agent,

6. Critical Reading - 3 cycles with 5 virtual readers (MVP: 1 cycle)    create_deep_research_agent,

7. Editing - Format and validate content    create_chapter_agent,

8. Finalization - Generate cover and metadata    create_review_agent,

9. Publication - Export to multiple formats    create_editing_agent,

"""    create_finalization_agent,

    create_publication_agent,

from typing import Any, Dict    create_coordinator_superagent,

from .config import (    execute_agent,

    get_model,    execute_review_personas,

    get_research_model,    execute_critical_reading_iterations,

    get_logger,    create_technical_reviewer_agent,

    console,    create_editorial_reviewer_agent,

    print_panel,    create_content_stylist_agent,

)    create_governance_agent,

from .agents import (    create_ethics_validator_agent,

    create_ideation_agent,)

    create_title_agent,

    create_structure_agent,

    create_deep_research_agent,def run_ebook_pipeline(

    create_chapter_agent,    topic: str,

    create_review_coordinator_agent,    target_audience: str,

    create_critical_reading_coordinator_agent,    word_count_target: int = 15000,

    create_editing_agent,    run_all_stages: bool = True

    create_finalization_agent,) -> dict:

    create_publication_agent,    """

    execute_agent,    Complete 9-stage ebook generation pipeline with specialized review personas and iterative refinement.

)    

    Pipeline Stages:

logger = get_logger(__name__)    1. Ideation - Define central idea, problem, target audience, transformation promise

    2. Title - Generate 3 Amazon-optimized title options

    3. Structure - Create hierarchical outline scaled to word count

def run_ebook_pipeline(    4A. Deep Research - Query external sources, vectorize findings, integrate with RAG

    topic: str,    4B. Chapter Writing - Write didactic content with research + author context

    target_audience: str,    5. Specialized Review - Execute 10 specialized review personas

    word_count_target: int = 15000,       ├─ Technical Reviewer (code quality, framework versions, accuracy)

    transformation_promise: str = "",       ├─ Editorial Reviewer (clarity, tone, flow, linguistics)

    reading_level: str = "intermediary",       ├─ Content Stylist (formatting, structure, consistency)

    **kwargs       ├─ Governance QA (compliance, metadata, security, LGPD)

) -> Dict[str, Any]:       ├─ Ethics Validator (bias, medical disclaimers, AI ethics, HIPAA)

    """       ├─ Author Stories Reviewer (narrative integration with didactic balance)

    Execute the complete 9-stage Ebook Generator pipeline.       ├─ Author Positioning Reviewer (market positioning and authority)

           ├─ Author Vision & Opinions (values and philosophy alignment)

    Args:       ├─ Examples & Exercises Code Reviewer (GitHub examples validation)

        topic: Main topic of the ebook       └─ Research & References Validator (research quality and citations)

        target_audience: Target audience segment    6. Critical Reading & Iterative Revision - 3 iteration cycles with 5 virtual readers

        word_count_target: Target word count (default: 15000)       ├─ Cycle 1: Critical Issues (major content and structure issues)

        transformation_promise: Transformation promise for reader       ├─ Cycle 2: Secondary Improvements (refinement and polish)

        reading_level: Reading level (beginner/intermediary/advanced/expert)       └─ Cycle 3: Final Polish (consistency and perfection)

        **kwargs: Additional stage-specific parameters from specs       Virtual Readers:

           ├─ Curious Beginner (accessibility, progression)

    Returns:       ├─ Technical Professional (depth, relevance, rigor)

        dict: Pipeline results with all stage outputs       ├─ Didactic Educator (pedagogical structure, methodology)

           ├─ Domain Specialist (cross-disciplinary coherence, application)

    Example:       └─ Reflective Reader (empathy, purpose, emotional impact)

        >>> result = run_ebook_pipeline(    7. Editing - Final formatting and validation

        ...     topic="Python for Data Analysis",    8. Finalization - Cover generation and metadata

        ...     target_audience="Data Scientists",    9. Publication - DOCX/EPUB/PDF/JSON export for KDP

        ...     word_count_target=20000    

        ... )    Args:

        >>> result['stage_1_ideation']['output']        topic: The main topic or theme of the ebook

        'Central idea of the book...'        target_audience: Specific audience segment

    """        word_count_target: Target word count (default: 15000)

            run_all_stages: Whether to run all 9 stages (default: True)

    logger.info(f"🚀 Starting Ebook Generator pipeline for topic: {topic}")    

        Returns:

    results = {}        Dictionary with results from each pipeline stage

        """

    try:    print("=" * 80)

        # STAGE 1: IDEATION    print("🚀 EBOOK GENERATOR 1.0 - AUTONOMOUS EDITORIAL PIPELINE (9-STAGE)")

        print_panel(    print("=" * 80)

            title="Stage 1: Ideation",    

            content="Generating central idea, problem definition, and target audience clarity...",    results = {}

            style="cyan"    model = get_model()

        )    

        logger.info("Executing Stage 1: Ideation")    # STAGE 1: IDEATION

            print("\n📋 STAGE 1: IDEATION")

        write_model = get_model()    print("-" * 80)

        ideation_agent = create_ideation_agent(write_model)    ideation_agent = create_ideation_agent(model)

            ideation_query = f"""Define the central idea for an ebook:

        ideation_query = f"""Generate the central idea for an ebook on '{topic}' for '{target_audience}'.Topic: {topic}

Target word count: {word_count_target} words.Target Audience: {target_audience}

Transformation promise: {transformation_promise if transformation_promise else 'To be determined'}Target Word Count: {word_count_target}



Provide: central idea, problem definition, target audience clarity, and transformation promise."""Define the transformation promise, core problem, and value proposition."""

            

        ideation_output = execute_agent(ideation_agent, ideation_query)    ideation_result = execute_agent(ideation_agent, ideation_query)

        results['stage_1_ideation'] = {    results["ideation"] = ideation_result

            "output": ideation_output,    print(ideation_result[:500] + "..." if len(ideation_result) > 500 else ideation_result)

        }    

        logger.info("✓ Stage 1 complete")    if not run_all_stages:

                return results

        # STAGE 2: TITLE GENERATION    

        print_panel(    # STAGE 2: TITLE GENERATION

            title="Stage 2: Title Generation",    print("\n📚 STAGE 2: TITLE GENERATION")

            content="Creating 3 Amazon-optimized title options...",    print("-" * 80)

            style="cyan"    title_agent = create_title_agent(model)

        )    title_query = f"""Generate 3 Amazon-optimized title + subtitle combinations:

        logger.info("Executing Stage 2: Title Generation")Topic: {topic}

        Target Audience: {target_audience}

        title_agent = create_title_agent(write_model)

        Focus on market appeal, SEO, and reader engagement."""

        title_query = f"""Based on this ebook concept:    

Topic: {topic}    title_result = execute_agent(title_agent, title_query)

Target Audience: {target_audience}    results["title"] = title_result

Central Idea: {ideation_output[:300]}    print(title_result[:500] + "..." if len(title_result) > 500 else title_result)

    

Generate 3 Amazon-optimized title options. Each title should be:    # STAGE 3: STRUCTURE

- 5-15 words long    print("\n🗂️  STAGE 3: STRUCTURE & OUTLINE")

- Include relevant keywords    print("-" * 80)

- Appeal to the target audience    structure_agent = create_structure_agent(model)

- Follow Amazon KDP best practices"""    structure_query = f"""Create a hierarchical table of contents:

        Topic: {topic}

        title_output = execute_agent(title_agent, title_query)Target Word Count: {word_count_target}

        results['stage_2_title'] = {Target Audience: {target_audience}

            "output": title_output,

        }Generate a didactic outline in Markdown format with section weights based on word count."""

        logger.info("✓ Stage 2 complete")    

            structure_result = execute_agent(structure_agent, structure_query)

        # STAGE 3: STRUCTURE    results["structure"] = structure_result

        print_panel(    print(structure_result[:500] + "..." if len(structure_result) > 500 else structure_result)

            title="Stage 3: Structure & Outline",    

            content="Building hierarchical outline scaled to word count target...",    # STAGE 4A: DEEP RESEARCH

            style="cyan"    print("\n🔬 STAGE 4A: DEEP RESEARCH & KNOWLEDGE INTEGRATION")

        )    print("-" * 80)

        logger.info("Executing Stage 3: Structure")    deep_research_agent = create_deep_research_agent(model)

            research_query = f"""Conduct deep research and knowledge integration:

        structure_agent = create_structure_agent(write_model)Topic: {topic}

        Target Audience: {target_audience}

        structure_query = f"""Create a detailed outline for an ebook with the following specs:

Topic: {topic}Query external sources and Context7 MCP for:

Target Audience: {target_audience}1. Latest research findings and best practices

Word Count Target: {word_count_target}2. Industry trends and relevant case studies

Central Idea: {ideation_output[:200]}3. Expert perspectives and methodologies

4. Data and statistics to support the topic

Generate a hierarchical table of contents with:

- 4-6 main chaptersVectorize findings and integrate with RAG system."""

- Subsections for each chapter    

- Estimated word count per section    research_result = execute_agent(deep_research_agent, research_query)

- Learning progression flow    results["deep_research"] = research_result

- Didactic structure"""    print(research_result[:500] + "..." if len(research_result) > 500 else research_result)

            

        structure_output = execute_agent(structure_agent, structure_query)    # STAGE 4B: CHAPTER WRITING

        results['stage_3_structure'] = {    print("\n✍️  STAGE 4B: CHAPTER WRITING")

            "output": structure_output,    print("-" * 80)

        }    chapter_agent = create_chapter_agent(model)

        logger.info("✓ Stage 3 complete")    chapter_words = word_count_target // 8

            chapter_query = f"""Write an introduction chapter incorporating research findings:

        # STAGE 4A: DEEP RESEARCHTopic: {topic}

        print_panel(Target Word Count: approximately {chapter_words} words

            title="Stage 4A: Deep Research",Target Audience: {target_audience}

            content="Gathering research with Context7 MCP and vectorizing for RAG...",Research Context: {research_result[:300]}

            style="cyan"

        )Use RAG context (author knowledge + research findings) when available. 

        logger.info("Executing Stage 4A: Deep Research")Make content didactic, engaging, and well-researched."""

            

        research_model = get_research_model()    chapter_result = execute_agent(chapter_agent, chapter_query)

        deep_research_agent = create_deep_research_agent(research_model)    results["chapter"] = chapter_result

            print(chapter_result[:500] + "..." if len(chapter_result) > 500 else chapter_result)

        research_query = f"""Conduct comprehensive research for an ebook on '{topic}'.    

Target Audience: {target_audience}    # STAGE 5: SPECIALIZED REVIEW WITH 10 PERSONAS

Outline provided: {structure_output[:300]}    print("\n🔍 STAGE 5: SPECIALIZED REVIEW (10 PERSONAS)")

    print("-" * 80)

Gather research on:    

- Key concepts and definitions    review_sample = chapter_result[:2000]  # Use excerpt for efficiency

- Best practices and methodologies    

- Case studies and real-world examples    print("  Executing 10 specialized reviewers:")

- Trends and expert perspectives    persona_feedback = execute_review_personas(model, review_sample)

- Data and statistics    results["review_personas"] = persona_feedback

    

Focus on depth and credibility for target audience."""    for reviewer_name, feedback in persona_feedback.items():

                print(f"\n  ▸ {reviewer_name.upper()} FEEDBACK:")

        research_output = execute_agent(deep_research_agent, research_query)        print("    " + feedback[:300] + "..." if len(feedback) > 300 else "    " + feedback)

        results['stage_4a_deep_research'] = {    

            "output": research_output,    # STAGE 6: CRITICAL READING & ITERATIVE REVISION (3 CYCLES)

        }    print("\n📖 STAGE 6: CRITICAL READING & ITERATIVE REVISION (3 CYCLES)")

        logger.info("✓ Stage 4A complete")    print("-" * 80)

            print("  Executing 3-cycle iterative refinement with 5 virtual readers...")

        # STAGE 4B: CHAPTER WRITING    

        print_panel(    critical_reading_results = execute_critical_reading_iterations(

            title="Stage 4B: Chapter Writing",        model=model,

            content="Writing didactic chapters with research integration and author voice...",        content=chapter_result,

            style="cyan"        review_feedback=persona_feedback

        )    )

        logger.info("Executing Stage 4B: Chapter Writing")    results["critical_reading"] = critical_reading_results

            

        chapter_agent = create_chapter_agent(write_model)    print(f"\n  ✓ Cycle 1 (Critical Issues): Complete")

            print(f"  ✓ Cycle 2 (Secondary Improvements): Complete")

        chapter_query = f"""Write chapters for an ebook with the following context:    print(f"  ✓ Cycle 3 (Final Polish): Complete")

Topic: {topic}    print(f"\n  Total iterations: {len(critical_reading_results.get('iterations', []))} cycles")

Target Audience: {target_audience}    print(f"  Refined content ready for editing.")

Outline: {structure_output[:300]}    

Research: {research_output[:300]}    # Use the refined content from critical reading for next stages

    refined_content = critical_reading_results.get("refined_content", chapter_result)

Write the first 2 chapters with:    

- Clear, didactic explanations    # STAGE 7: EDITING

- Practical examples for target audience    print("\n🎨 STAGE 7: EDITING & FORMATTING")

- Connection to transformation promise    print("-" * 80)

- Engaging author voice    editing_agent = create_editing_agent(model)

- 2-3 examples per section    editing_query = """Validate and perfect Markdown formatting:

- Practice exercises included- Check heading hierarchy (H1, H2, H3)

- Verify code block formatting

Format: Markdown with proper heading hierarchy"""- Ensure list consistency

        - Validate link structure

        chapter_output = execute_agent(chapter_agent, chapter_query)- Check for formatting consistency

        results['stage_4b_chapter_writing'] = {

            "output": chapter_output,Provide final formatting polish suggestions."""

        }    

        logger.info("✓ Stage 4B complete")    editing_result = execute_agent(editing_agent, editing_query)

            results["editing"] = editing_result

        # STAGE 5: SPECIALIZED REVIEW (10 PERSONAS)    print(editing_result[:500] + "..." if len(editing_result) > 500 else editing_result)

        print_panel(    

            title="Stage 5: Specialized Review",    # STAGE 8: FINALIZATION

            content="Collecting feedback from 10 specialized review personas...",    print("\n✨ STAGE 8: FINALIZATION & COVER")

            style="cyan"    print("-" * 80)

        )    finalization_agent = create_finalization_agent(model)

        logger.info("Executing Stage 5: Specialized Review")    finalization_query = f"""Generate cover concept and validate metadata:

        Topic: {topic}

        review_agent = create_review_coordinator_agent(research_model)Target Audience: {target_audience}

        

        review_query = f"""Review the following content for an ebook:Create an attractive cover concept and validate all metadata requirements."""

Topic: {topic}    

Target Audience: {target_audience}    finalization_result = execute_agent(finalization_agent, finalization_query)

Content Sample: {chapter_output[:500] if len(chapter_output) > 500 else chapter_output}    results["finalization"] = finalization_result

    print(finalization_result[:500] + "..." if len(finalization_result) > 500 else finalization_result)

Provide structured feedback addressing:    

- Technical accuracy    # STAGE 9: PUBLICATION

- Editorial clarity    print("\n📦 STAGE 9: PUBLICATION & KDP EXPORT")

- Content styling    print("-" * 80)

- Governance compliance    publication_agent = create_publication_agent(model)

- Ethical considerations    publication_query = f"""Prepare for KDP publication:

- Author story integrationTopic: {topic}

- Author positioningAuthor: Igor Medeiros

- Author vision alignmentTarget Word Count: {word_count_target}

- Code example quality

- Research validation"""Generate complete KDP metadata package (DOCX, EPUB, PDF, JSON)."""

            

        review_output = execute_agent(review_agent, review_query)    publication_result = execute_agent(publication_agent, publication_query)

        results['stage_5_review'] = {    results["publication"] = publication_result

            "output": review_output,    print(publication_result[:500] + "..." if len(publication_result) > 500 else publication_result)

        }    

        logger.info("✓ Stage 5 complete")    # COMPLETION

            print("\n" + "=" * 80)

        # STAGE 6: CRITICAL READING & ITERATION (1 CYCLE FOR MVP)    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")

        print_panel(    print("=" * 80)

            title="Stage 6: Critical Reading & Iteration",    print(f"\nPipeline Summary:")

            content="Executing 1 iteration cycle with 5 virtual readers (MVP: simplified)...",    print(f"  • Topic: {topic}")

            style="cyan"    print(f"  • Target Audience: {target_audience}")

        )    print(f"  • Target Word Count: {word_count_target}")

        logger.info("Executing Stage 6: Critical Reading (1 cycle)")    print(f"  • Stages Completed: 9/9")

            print(f"  • Specialized Review Personas: 10")

        critical_reading_agent = create_critical_reading_coordinator_agent(research_model)    print(f"  • Critical Reading Iterations: 3 cycles with 5 virtual readers")

            print(f"  • Deep Research Integration: ✓ Completed")

        critical_reading_query = f"""Evaluate the following ebook content through the lens of 5 virtual readers:    

1. Curious Beginner - Assess clarity and accessibility    return results

2. Technical Professional - Verify depth and relevance

3. Didactic Educator - Check pedagogical structure

4. Domain Specialist - Validate cross-disciplinary coherencedef main():

5. Reflective Reader - Assess empathy and impact    """Main entry point - demonstration of the 9-stage pipeline with critical reading iterations."""

    topic = "Advanced Python with LangChain"

Content to review: {chapter_output[:400] if len(chapter_output) > 400 else chapter_output}    target_audience = "Senior Python Developers and AI Engineers"

Target Audience: {target_audience}    word_count_target = 15000

    

Provide feedback for improvement in next iteration."""    results = run_ebook_pipeline(

                topic=topic,

        critical_reading_output = execute_agent(critical_reading_agent, critical_reading_query)        target_audience=target_audience,

        results['stage_6_critical_reading'] = {        word_count_target=word_count_target,

            "output": critical_reading_output,        run_all_stages=True

            "iterations": 1,    )

        }    

        logger.info("✓ Stage 6 complete (1 cycle)")    return results

        

        # STAGE 7: EDITING

        print_panel(if __name__ == "__main__":

            title="Stage 7: Editing",    main()

            content="Final formatting and content validation...",
            style="cyan"
        )
        logger.info("Executing Stage 7: Editing")
        
        editing_agent = create_editing_agent(write_model)
        
        editing_query = f"""Edit and format the ebook content for publication.
Content: {chapter_output[:300] if len(chapter_output) > 300 else chapter_output}

Apply:
- Markdown formatting standards
- Heading hierarchy consistency
- Grammar and style checks
- Structure validation
- Word count verification
- Link validation

Deliver publication-ready formatted content."""
        
        editing_output = execute_agent(editing_agent, editing_query)
        results['stage_7_editing'] = {
            "output": editing_output,
        }
        logger.info("✓ Stage 7 complete")
        
        # STAGE 8: FINALIZATION
        print_panel(
            title="Stage 8: Finalization",
            content="Generating cover concept and metadata...",
            style="cyan"
        )
        logger.info("Executing Stage 8: Finalization")
        
        finalization_agent = create_finalization_agent(write_model)
        
        finalization_query = f"""Finalize the ebook with cover concept and metadata.
Title: {title_output[:100] if len(title_output) > 100 else title_output}
Topic: {topic}
Target Audience: {target_audience}

Generate:
- Cover concept (visual description for designer)
- Metadata (keywords, description, category)
- Author bio section
- Back cover copy
- Table of contents final version"""
        
        finalization_output = execute_agent(finalization_agent, finalization_query)
        results['stage_8_finalization'] = {
            "output": finalization_output,
        }
        logger.info("✓ Stage 8 complete")
        
        # STAGE 9: PUBLICATION
        print_panel(
            title="Stage 9: Publication",
            content="Preparing files for multi-format publication...",
            style="cyan"
        )
        logger.info("Executing Stage 9: Publication")
        
        publication_agent = create_publication_agent(write_model)
        
        publication_query = f"""Prepare the ebook for publication in multiple formats.
Title: {title_output[:100] if len(title_output) > 100 else title_output}
Content: {editing_output[:200] if len(editing_output) > 200 else editing_output}
Word Count Target: {word_count_target}

Export to:
- DOCX (Microsoft Word format)
- EPUB (e-reader format)
- PDF (fixed layout)
- JSON (metadata)

Include KDP compliance checks."""
        
        publication_output = execute_agent(publication_agent, publication_query)
        results['stage_9_publication'] = {
            "output": publication_output,
        }
        logger.info("✓ Stage 9 complete")
        
        # Pipeline complete
        print_panel(
            title="Pipeline Complete ✓",
            content=f"Ebook '{topic}' successfully generated through all 9 stages.",
            style="green"
        )
        logger.info(f"✓ Pipeline complete for topic: {topic}")
        
        results['pipeline_status'] = 'completed'
        results['summary'] = {
            'topic': topic,
            'target_audience': target_audience,
            'word_count_target': word_count_target,
            'stages_completed': 9,
        }
        
        return results
        
    except Exception as e:
        logger.error(f"Pipeline error: {str(e)}")
        results['pipeline_status'] = 'error'
        results['error'] = str(e)
        print_panel(
            title="Pipeline Error ❌",
            content=f"Error in pipeline execution: {str(e)}",
            style="red"
        )
        return results


if __name__ == "__main__":
    # Example usage
    result = run_ebook_pipeline(
        topic="Python for Data Analysis",
        target_audience="Data Scientists and Analysts",
        word_count_target=20000,
        transformation_promise="Master advanced data analysis techniques in Python"
    )
    
    logger.info(f"Pipeline results: {result['pipeline_status']}")
