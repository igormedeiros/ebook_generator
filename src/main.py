"""
Main entry point for the Ebook Generator 1.0 pipeline.
Orchestrates the 8-stage editorial process with specialized agents.
"""

from config import get_model
from agents import (
    create_ideation_agent,
    create_title_agent,
    create_structure_agent,
    create_chapter_agent,
    create_review_agent,
    create_editing_agent,
    create_finalization_agent,
    create_publication_agent,
    create_coordinator_superagent,
    execute_agent,
    execute_review_personas,
    create_technical_reviewer_agent,
    create_editorial_reviewer_agent,
    create_content_stylist_agent,
    create_governance_agent,
    create_ethics_validator_agent,
)


def run_ebook_pipeline(
    topic: str,
    target_audience: str,
    word_count_target: int = 15000,
    run_all_stages: bool = True
) -> dict:
    """
    Complete 8-stage ebook generation pipeline with specialized review personas.
    
    Pipeline Stages:
    1. Ideation - Define central idea, problem, target audience, transformation promise
    2. Title - Generate 3 Amazon-optimized title options
    3. Structure - Create hierarchical outline scaled to word count
    4. Chapter Writing - Write didactic content with RAG integration
    5. Review - Execute 5 specialized review personas
       ├─ Technical Reviewer (code quality, framework versions, accuracy)
       ├─ Editorial Reviewer (clarity, tone, flow, linguistics)
       ├─ Content Stylist (formatting, structure, consistency)
       ├─ Governance QA (compliance, metadata, security, LGPD)
       └─ Ethics Validator (bias, medical disclaimers, AI ethics, HIPAA)
    6. Editing - Final formatting and validation
    7. Finalization - Cover generation and metadata
    8. Publication - DOCX/EPUB/PDF/JSON export for KDP
    
    Args:
        topic: The main topic or theme of the ebook
        target_audience: Specific audience segment
        word_count_target: Target word count (default: 15000)
        run_all_stages: Whether to run all 8 stages (default: True)
    
    Returns:
        Dictionary with results from each pipeline stage
    """
    print("=" * 80)
    print("🚀 EBOOK GENERATOR 1.0 - AUTONOMOUS EDITORIAL PIPELINE")
    print("=" * 80)
    
    results = {}
    model = get_model()
    
    # STAGE 1: IDEATION
    print("\n📋 STAGE 1: IDEATION")
    print("-" * 80)
    ideation_agent = create_ideation_agent(model)
    ideation_query = f"""Define the central idea for an ebook:
Topic: {topic}
Target Audience: {target_audience}
Target Word Count: {word_count_target}

Define the transformation promise, core problem, and value proposition."""
    
    ideation_result = execute_agent(ideation_agent, ideation_query)
    results["ideation"] = ideation_result
    print(ideation_result[:500] + "..." if len(ideation_result) > 500 else ideation_result)
    
    if not run_all_stages:
        return results
    
    # STAGE 2: TITLE GENERATION
    print("\n📚 STAGE 2: TITLE GENERATION")
    print("-" * 80)
    title_agent = create_title_agent(model)
    title_query = f"""Generate 3 Amazon-optimized title + subtitle combinations:
Topic: {topic}
Target Audience: {target_audience}

Focus on market appeal, SEO, and reader engagement."""
    
    title_result = execute_agent(title_agent, title_query)
    results["title"] = title_result
    print(title_result[:500] + "..." if len(title_result) > 500 else title_result)
    
    # STAGE 3: STRUCTURE
    print("\n🗂️  STAGE 3: STRUCTURE & OUTLINE")
    print("-" * 80)
    structure_agent = create_structure_agent(model)
    structure_query = f"""Create a hierarchical table of contents:
Topic: {topic}
Target Word Count: {word_count_target}
Target Audience: {target_audience}

Generate a didactic outline in Markdown format with section weights based on word count."""
    
    structure_result = execute_agent(structure_agent, structure_query)
    results["structure"] = structure_result
    print(structure_result[:500] + "..." if len(structure_result) > 500 else structure_result)
    
    # STAGE 4: CHAPTER WRITING
    print("\n✍️  STAGE 4: CHAPTER WRITING")
    print("-" * 80)
    chapter_agent = create_chapter_agent(model)
    chapter_words = word_count_target // 8
    chapter_query = f"""Write an introduction chapter:
Topic: {topic}
Target Word Count: approximately {chapter_words} words
Target Audience: {target_audience}

Use RAG context when available. Make content didactic and engaging."""
    
    chapter_result = execute_agent(chapter_agent, chapter_query)
    results["chapter"] = chapter_result
    print(chapter_result[:500] + "..." if len(chapter_result) > 500 else chapter_result)
    
    # STAGE 5: SPECIALIZED REVIEW WITH 5 PERSONAS
    print("\n🔍 STAGE 5: SPECIALIZED REVIEW (5 PERSONAS)")
    print("-" * 80)
    
    review_sample = chapter_result[:2000]  # Use excerpt for efficiency
    
    print("  Executing 5 specialized reviewers:")
    persona_feedback = execute_review_personas(model, review_sample)
    results["review_personas"] = persona_feedback
    
    for reviewer_name, feedback in persona_feedback.items():
        print(f"\n  ▸ {reviewer_name.upper()} FEEDBACK:")
        print("    " + feedback[:300] + "..." if len(feedback) > 300 else "    " + feedback)
    
    # STAGE 6: EDITING
    print("\n🎨 STAGE 6: EDITING & FORMATTING")
    print("-" * 80)
    editing_agent = create_editing_agent(model)
    editing_query = """Validate Markdown formatting:
- Check heading hierarchy (H1, H2, H3)
- Verify code block formatting
- Ensure list consistency
- Validate link structure

Provide formatting improvement suggestions."""
    
    editing_result = execute_agent(editing_agent, editing_query)
    results["editing"] = editing_result
    print(editing_result[:500] + "..." if len(editing_result) > 500 else editing_result)
    
    # STAGE 7: FINALIZATION
    print("\n✨ STAGE 7: FINALIZATION & COVER")
    print("-" * 80)
    finalization_agent = create_finalization_agent(model)
    finalization_query = f"""Generate cover concept and validate metadata:
Topic: {topic}
Target Audience: {target_audience}

Create an attractive cover concept and validate all metadata requirements."""
    
    finalization_result = execute_agent(finalization_agent, finalization_query)
    results["finalization"] = finalization_result
    print(finalization_result[:500] + "..." if len(finalization_result) > 500 else finalization_result)
    
    # STAGE 8: PUBLICATION
    print("\n📦 STAGE 8: PUBLICATION & KDP EXPORT")
    print("-" * 80)
    publication_agent = create_publication_agent(model)
    publication_query = f"""Prepare for KDP publication:
Topic: {topic}
Author: Igor Medeiros
Target Word Count: {word_count_target}

Generate complete KDP metadata package (DOCX, EPUB, JSON)."""
    
    publication_result = execute_agent(publication_agent, publication_query)
    results["publication"] = publication_result
    print(publication_result[:500] + "..." if len(publication_result) > 500 else publication_result)
    
    # COMPLETION
    print("\n" + "=" * 80)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\nPipeline Summary:")
    print(f"  • Topic: {topic}")
    print(f"  • Target Audience: {target_audience}")
    print(f"  • Target Word Count: {word_count_target}")
    print(f"  • Stages Completed: 8/8")
    print(f"  • Review Personas: 5 specialized reviewers executed")
    
    return results


def main():
    """Main entry point - demonstration of the 8-stage pipeline."""
    topic = "Advanced Python with LangChain"
    target_audience = "Senior Python Developers and AI Engineers"
    word_count_target = 15000
    
    results = run_ebook_pipeline(
        topic=topic,
        target_audience=target_audience,
        word_count_target=word_count_target,
        run_all_stages=True
    )
    
    return results


if __name__ == "__main__":
    main()
