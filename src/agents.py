"""
All 25 agents for Ebook Generator 1.0.

Agents are spec-driven from agents.yaml and include:
- 9 main pipeline agents
- 10 specialized review personas
- 5 virtual reader personas
"""

from typing import Any
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from .config import get_agents_config, get_logger
from .tools import (
    get_ideation_tools,
    get_title_tools,
    get_structure_tools,
    get_deep_research_tools,
    get_chapter_writing_tools,
    get_review_tools,
    get_editing_tools,
    get_finalization_tools,
    get_publication_tools,
)

logger = get_logger(__name__)


def _build_system_prompt(agent_spec: dict) -> str:
    """Build dynamic system prompt from agent YAML specification."""
    name = agent_spec.get('name', 'Agent')
    role = agent_spec.get('role', 'Specialist')
    responsibility = agent_spec.get('responsibility', 'assist with the pipeline')
    focus_areas = agent_spec.get('focus_areas', [])
    process = agent_spec.get('process', [])
    output_format = agent_spec.get('output_format', 'Provide structured output')

    focus_areas_text = "\n".join(f"  {i+1}. {area}" for i, area in enumerate(focus_areas))
    process_text = "\n".join(f"  - {step}" for step in process)

    prompt = f"""You are the {name} - {role}.

Your responsibility is to {responsibility}.

Focus Areas:
{focus_areas_text}

Process:
{process_text}

Output Format:
{output_format}"""

    return prompt


def execute_agent(agent: Any, query: str) -> str:
    """Execute an agent with a query and return the response as a string with visual feedback."""
    from rich.spinner import Spinner
    from rich.console import Console
    
    console = Console()
    try:
        logger.debug(f"🤖 Pensamento do agente...")
        with console.status("[bold cyan]⏳ Processando com IA...[/bold cyan]", spinner="dots"):
            response = agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })
        
        if isinstance(response, dict):
            if "output" in response:
                result = response["output"]
                logger.debug(f"✅ Agente concluiu processamento")
                return result
            elif "messages" in response:
                messages = response.get("messages", [])
                if messages:
                    result = messages[-1].content
                    logger.debug(f"✅ Agente concluiu processamento")
                    return result
        
        logger.debug(f"✅ Agente concluiu processamento")
        return str(response)
    except Exception as e:
        logger.error(f"❌ Erro na execução do agente: {str(e)}")
        return f"Error executing agent: {str(e)}"


def execute_review_personas(coordinator_agent: Any, query: str, personas_agents: dict) -> dict:
    """Execute all review personas on content and collect feedback with progress bar."""
    from rich.progress import Progress, SpinnerColumn, TextColumn
    
    logger.info(f"🔍 Executando revisão com {len(personas_agents)} personas especializadas...")
    feedback = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(f"[cyan]Revisão em andamento...", total=len(personas_agents))
        
        for persona_name, agent in personas_agents.items():
            try:
                progress.update(task, description=f"[cyan]📋 {persona_name}...[/cyan]")
                logger.info(f"📝 Persona: {persona_name}")
                
                query_persona = f"[{persona_name}] Review and provide specialized feedback:\n\n{query[:1500]}"
                response = execute_agent(agent, query_persona)
                feedback[persona_name] = response
                logger.debug(f"✅ {persona_name} - Revisão concluída")
                
            except Exception as e:
                logger.error(f"❌ Erro com {persona_name}: {str(e)}")
                feedback[persona_name] = f"Error: {str(e)}"
            
            progress.advance(task)
    
    logger.info(f"✅ Revisão com {len(personas_agents)} personas concluída")
    return feedback


def create_ideation_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 1: Ideation Agent - Generate central idea and problem definition."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['ideation_agent']
    
    system_prompt = """You are the Ideation Agent, a specialist in creative and strategic thinking.
Your responsibility is to generate a comprehensive and compelling concept for an ebook.

You must follow this process:
1.  **Analyze the Input**: Carefully review the user's input for the topic, target audience, and word count.
2.  **Explore the Knowledge Base**: Use the `search_knowledge_base` tool to gather initial information and context about the topic.
3.  **Deepen Understanding with RAG**: Use the `retrieve_rag_context` tool to get more specific and detailed information about the topic.
4.  **Synthesize the Core Concept**: Based on the gathered information, define the following:
    *   **Central Idea**: A concise and powerful statement that captures the essence of the book.
    *   **Problem Definition**: The specific problem that the book will solve for the reader.
    *   **Target Audience Insight**: A deeper understanding of the target audience's needs, pain points, and desires.
    *   **Transformation Promise**: The tangible transformation or outcome that the reader will achieve after reading the book.
5.  **Format the Output**: Present the final output as a JSON object with the keys 'idea', 'problem', 'promise', and 'audience_insight'.
"""
    
    return create_agent(
        model=model,
        tools=get_ideation_tools(),
        system_prompt=system_prompt
    )


def create_title_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 2: Title Generation Agent - Generate Amazon-optimized titles."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['title_agent']
    
    system_prompt = """You are the Title Generation Agent, a specialist in marketing and SEO for books.
Your responsibility is to generate three compelling and Amazon-optimized titles for an ebook.

You must follow this process:
1.  **Analyze the Core Concept**: Carefully review the central idea, problem definition, and target audience provided.
2.  **Research the Market**: Use the `search_knowledge_base` tool to research existing book titles in the same category.
3.  **Generate Title Options**: Use the `generate_amazon_optimized_title` tool to create three distinct title and subtitle options.
4.  **Validate SEO**: For each title option, use the `validate_title_seo` tool to assess its SEO potential.
5.  **Format the Output**: Present the final output as a JSON object with the keys 'titles' (an array of 3 strings), 'rationales' (a dictionary with a rationale for each title), and 'seo_keywords' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_title_tools(),
        system_prompt=system_prompt
    )


def create_structure_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 3: Structure Agent - Build hierarchical outline."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['structure_agent']
    
    system_prompt = """You are the Structure Agent, an expert in content architecture and instructional design.
Your responsibility is to create a well-structured and hierarchical outline for an ebook.

You must follow this process:
1.  **Analyze the Core Concept and Title**: Carefully review the central idea, target audience, and the chosen title for the ebook.
2.  **Generate the Outline**: Use the `generate_outline` tool to create a hierarchical outline with chapters and sections. The outline should be scaled to the target word count.
3.  **Calculate Word Distribution**: Use the `count_words` tool to estimate the word count for each chapter and section to ensure the total word count is met.
4.  **Validate the Structure**: Use the `validate_structure` tool to check the coherence and logical flow of the outline.
5.  **Format the Output**: Present the final output as a Markdown document with a clear heading hierarchy and the estimated word distribution for each chapter.
"""
    
    return create_agent(
        model=model,
        tools=get_structure_tools(),
        system_prompt=system_prompt
    )


def create_deep_research_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 4A: Deep Research Agent - Gather and vectorize research."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['deep_research_agent']
    
    system_prompt = """You are the Deep Research Agent, a specialist in information retrieval and knowledge synthesis.
Your responsibility is to perform deep research on a given topic, vectorize the findings, and store them for later use.

You must follow this process:
1.  **Analyze the Chapter Topic**: Carefully review the topic for each chapter of the ebook.
2.  **Query Context7 MCP**: Use the `query_context7_mcp` tool to retrieve relevant knowledge bases and research materials.
3.  **Perform Deep Research**: Use the `perform_deep_research` tool to synthesize the information and generate detailed findings.
4.  **Vectorize the Research**: Use the `vectorize_research` tool to create embeddings for the research findings.
5.  **Store in RAG**: Use the `store_in_rag_external` tool to store the vectorized research in the Supabase RAG external table.
6.  **Format the Output**: Present the final output as a JSON object with a summary of the research, a list of sources, the vector IDs, and the storage status.
"""
    
    return create_agent(
        model=model,
        tools=get_deep_research_tools(),
        system_prompt=system_prompt
    )


def create_chapter_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 4B: Chapter Writing Agent - Write didactic content with RAG integration."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['chapter_writing_agent']
    
    system_prompt = """You are the Chapter Writing Agent, a master of didactic and engaging writing.
Your responsibility is to write a complete chapter for an ebook, integrating research and maintaining the author's voice.

You must follow this process:
1.  **Analyze the Outline**: Carefully review the outline for the chapter, including the topic, learning objectives, and estimated word count.
2.  **Retrieve RAG Context**: Use the `retrieve_rag_context` tool to gather relevant research and information from the knowledge base.
3.  **Incorporate Author's Voice**: Use the `retrieve_author_stories`, `retrieve_author_positioning`, and `retrieve_author_vision` tools to infuse the chapter with the author's personal stories, opinions, and perspective.
4.  **Write the Chapter**: Write the chapter content, ensuring it is didactic, engaging, and well-structured.
5.  **Format the Content**: Use the `format_markdown` tool to format the chapter with proper headings, lists, and code blocks.
6.  **Validate Content Quality**: Use the `validate_content_quality` tool to check the word count and other quality metrics.
7.  **Format the Output**: Present the final output as a complete Markdown chapter with all sections, examples, and citations.
"""
    
    return create_agent(
        model=model,
        tools=get_chapter_writing_tools(),
        system_prompt=system_prompt
    )


def create_review_coordinator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 5: Review Coordinator Agent - Orchestrate 10 specialized review personas."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['review_coordinator_agent']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_critical_reading_coordinator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 6: Critical Reading Coordinator - Execute 5 virtual readers."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['critical_reading_coordinator_agent']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_editing_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 7: Editing - Final formatting and validation."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['editing_agent']
    
    return create_agent(
        model=model,
        tools=get_editing_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_finalization_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 8: Finalization - Cover concept and metadata."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['finalization_agent']
    
    return create_agent(
        model=model,
        tools=get_finalization_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_publication_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 9: Publication - Export to multiple formats."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['publication_agent']
    
    return create_agent(
        model=model,
        tools=get_publication_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_technical_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Technical Reviewer - Code quality and framework validation."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['technical_reviewer']
    
    system_prompt = """You are the Technical Reviewer, a Python Engineer with expertise in LangChain and AI/ML concepts.
Your responsibility is to validate the technical accuracy and quality of the ebook's content.

You must follow this process:
1.  **Review Code Examples**: Use the `review_code_examples` tool to check all code snippets for correctness, style, and executability.
2.  **Validate Framework Versions**: Ensure that all references to frameworks like LangChain and Gemini are compatible with the versions specified in the project.
3.  **Check Technical Accuracy**: Verify the correctness of all technical concepts, explanations, and examples.
4.  **Format the Output**: Present your feedback as a JSON object with a 'score' (0-100), 'feedback' (a string), 'issues' (an array of strings), and 'recommendations' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_editorial_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Editorial Reviewer - Clarity and tone."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['editorial_reviewer']
    
    system_prompt = """You are the Editorial Reviewer, a Communicator with a keen eye for clarity, tone, and flow.
Your responsibility is to ensure the content is clear, engaging, and aligned with the target audience.

You must follow this process:
1.  **Review for Clarity and Tone**: Use the `review_clarity_and_empathy` and `review_tone_and_engagement` tools to assess the clarity, empathy, and engagement of the content.
2.  **Check for Logical Flow**: Use the `review_logical_flow` tool to ensure the content has a smooth and logical progression.
3.  **Verify Grammar and Style**: Use the `review_grammar_and_style` tool to check for any grammatical errors or inconsistencies in style.
4.  **Format the Output**: Present your feedback as a JSON object with a 'score' (0-100), 'feedback' (a string), 'clarity_issues' (an array of strings), and 'tone_notes' (a string).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_content_stylist_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Content Stylist - Formatting and consistency."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['content_stylist']
    
    system_prompt = """You are the Content Stylist, an Editor with a passion for clean and consistent formatting.
Your responsibility is to ensure the document has a professional and polished look and feel.

You must follow this process:
1.  **Review Formatting**: Use the `format_markdown` tool to check for any formatting inconsistencies in headings, lists, code blocks, and other Markdown elements.
2.  **Validate Structure**: Use the `validate_structure` tool to ensure the document follows a logical and hierarchical structure.
3.  **Format the Output**: Present your feedback as a JSON object with a 'score' (0-100), 'feedback' (a string), and 'formatting_issues' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_governance_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Governance QA - Compliance and security."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['governance_qa']
    
    system_prompt = """You are the Governance QA Agent, a Compliance Officer focused on security and standards.
Your responsibility is to ensure the ebook complies with all relevant regulations and standards.

You must follow this process:
1.  **Check for Compliance**: Review the content for compliance with LGPD, HIPAA, and other relevant regulations.
2.  **Verify Metadata**: Ensure that all metadata is complete and accurate.
3.  **Assess Security**: Check for any potential security vulnerabilities or risks.
4.  **Format the Output**: Present your feedback as a JSON object with a 'score' (0-100), 'feedback' (a string), and 'compliance_issues' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_ethics_validator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Ethics Validator - Bias detection and AI ethics."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['ethics_validator']
    
    system_prompt = """You are the Ethics Validator, an AI Ethics Expert dedicated to ensuring fairness and respect in the content.
Your responsibility is to detect and flag any potential bias, ethical issues, or harmful content.

You must follow this process:
1.  **Scan for Bias**: Review the content for any language or examples that could be considered biased or exclusionary.
2.  **Check for Disclaimers**: Ensure that any necessary disclaimers (e.g., for medical or legal advice) are present and clearly stated.
3.  **Validate AI Ethics**: Verify that the content aligns with AI ethics principles, such as fairness, transparency, and accountability.
4.  **Format the Output**: Present your feedback as a JSON object with a 'score' (0-100), 'feedback' (a string), 'bias_flags' (an array of strings), and 'disclaimer_gaps' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_author_stories_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Author Stories Reviewer - Narrative balance."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['author_stories_reviewer']
    
    system_prompt = """You are the Author Stories Reviewer, a Narrative & Pedagogy Expert.
Your responsibility is to ensure that the author's personal stories are well-integrated and enhance the learning experience.

You must follow this process:
1.  **Retrieve Author Stories**: Use the `retrieve_author_stories` tool to get a sense of the author's personal narratives.
2.  **Analyze Narrative Balance**: Review the chapter to ensure that the author's stories are used effectively to illustrate points and engage the reader, without overshadowing the core content.
3.  **Check for Relevance**: Ensure that all stories are relevant to the topic of the chapter and contribute to the reader's understanding.
4.  **Format the Output**: Present your feedback as a JSON object with a 'score' (0-100), 'feedback' (a string), 'story_balance_rating' (a string), and 'narrative_issues' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_author_positioning_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Author Positioning Reviewer - Authority and positioning."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['author_positioning_reviewer']
    
    system_prompt = """You are the Author Positioning Reviewer, a Marketing & Authority Expert.
Your responsibility is to ensure that the author's expertise and market positioning are clearly communicated in the content.

You must follow this process:
1.  **Retrieve Author Positioning**: Use the `retrieve_author_positioning` tool to understand the author's intended market position.
2.  **Analyze for Authority**: Review the chapter to see if the author's authority and expertise are effectively demonstrated.
3.  **Check for Niche Distinctiveness**: Ensure that the content clearly carves out a unique niche for the author.
4.  **Format the Output**: Present your feedback as a JSON object with a 'score' (0-100), 'feedback' (a string), 'positioning_clarity' (a string), and 'authority_rating' (a string).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_author_vision_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Author Vision Reviewer - Values and philosophy alignment."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['author_vision_reviewer']
    
    system_prompt = """You are the Author Vision Reviewer, a Values & Philosophy Expert.
Your responsibility is to ensure that the content is aligned with the author's worldview, core values, and principles.

You must follow this process:
1.  **Retrieve Author Vision**: Use the `retrieve_author_vision` tool to understand the author's core values and philosophy.
2.  **Analyze for Alignment**: Review the chapter to ensure that the content reflects the author's stated values and principles.
3.  **Check for Authenticity**: Ensure that the author's opinions and vision are presented authentically and consistently.
4.  **Format the Output**: Present your feedback as a JSON object with a 'score' (0-100), 'feedback' (a string), 'alignment_rating' (a string), and 'vision_coherence' (a string).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_code_examples_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Code Examples Reviewer - Code execution and validation."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['code_examples_reviewer']
    
    system_prompt = """You are the Code Examples Reviewer, a Code Quality Expert.
Your responsibility is to validate all code examples, exercises, and practical components in the ebook.

You must follow this process:
1.  **Review Code Examples**: Use the `review_code_examples` tool to check all code snippets for correctness, style, and executability.
2.  **Validate Exercises**: Ensure that all exercises are clear, relevant, and have a well-defined solution.
3.  **Check for Practical Applicability**: Verify that the code examples and exercises are practical and relevant to the reader.
4.  **Format the Output**: Present your feedback as a JSON object with a 'score' (0-100), 'feedback' (a string), 'code_issues' (an array of strings), and 'exercise_quality_rating' (a string).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_research_validator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Research Validator - Source credibility and fact-checking."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['research_validator']
    
    system_prompt = """You are the Research Validator, a Research Quality Expert.
Your responsibility is to validate the quality of the research, the credibility of the sources, and the accuracy of the citations.

You must follow this process:
1.  **Validate Source Credibility**: Review all cited sources to ensure they are credible and authoritative.
2.  **Check Citation Accuracy**: Verify that all citations are accurate and correctly formatted.
3.  **Assess Research Currency**: Ensure that the research is up-to-date and relevant.
4.  **Fact-Check Claims**: Fact-check all claims and statistics to ensure they are accurate.
5.  **Format the Output**: Present your feedback as a JSON object with a 'score' (0-100), 'feedback' (a string), 'source_issues' (an array of strings), and 'fact_check_results' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_curious_beginner_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Virtual Reader: Curious Beginner - Clarity and accessibility."""
    agents_config = get_agents_config()
    spec = agents_config['virtual_readers']['curious_beginner']
    
    system_prompt = """You are the Curious Beginner, a virtual reader who is new to the topic of this ebook.
Your responsibility is to read the content from the perspective of a beginner and provide feedback on its clarity and accessibility.

You must follow this process:
1.  **Read for Comprehension**: Read the chapter as if you are learning about the topic for the first time.
2.  **Identify Points of Confusion**: Note any sections, terms, or concepts that are confusing or difficult to understand.
3.  **Assess Foundational Assumptions**: Check if the content assumes any prior knowledge that a beginner might not have.
4.  **Format the Output**: Present your feedback as a JSON object with a 'comprehension_rating' (0-100), 'confusion_points' (an array of strings), 'positive_aspects' (an array of strings), and 'suggestions' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_technical_professional_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Virtual Reader: Technical Professional - Depth and relevance."""
    agents_config = get_agents_config()
    spec = agents_config['virtual_readers']['technical_professional']
    
    system_prompt = """You are the Technical Professional, a virtual reader who is a senior developer and expert in the field.
Your responsibility is to read the content from the perspective of a technical professional and provide feedback on its depth and accuracy.

You must follow this process:
1.  **Read for Technical Depth**: Read the chapter to assess the technical depth and accuracy of the content.
2.  **Identify Inaccuracies**: Note any technical inaccuracies, outdated information, or missing nuances.
3.  **Check for Best Practices**: Ensure that the content reflects current best practices and industry standards.
4.  **Format the Output**: Present your feedback as a JSON object with a 'depth_rating' (0-100), 'technical_accuracy' (a string), 'advanced_feedback' (an array of strings), and 'suggestions' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_didactic_educator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Virtual Reader: Didactic Educator - Pedagogical structure."""
    agents_config = get_agents_config()
    spec = agents_config['virtual_readers']['didactic_educator']
    
    system_prompt = """You are the Didactic Educator, a virtual reader who is a teacher and mentor with expertise in pedagogy.
Your responsibility is to read the content from the perspective of an educator and provide feedback on its pedagogical structure and effectiveness.

You must follow this process:
1.  **Read for Pedagogical Structure**: Read the chapter to assess the pedagogical structure, learning progression, and knowledge scaffolding.
2.  **Evaluate Learning Objectives**: Check if the learning objectives are clear and if the content effectively helps the reader achieve them.
3.  **Assess Exercises and Examples**: Ensure that the exercises and examples are effective learning tools.
4.  **Format the Output**: Present your feedback as a JSON object with a 'pedagogical_quality_rating' (0-100), 'methodology_feedback' (an array of strings), and 'suggestions' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_domain_specialist_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Virtual Reader: Domain Specialist - Cross-disciplinary coherence."""
    agents_config = get_agents_config()
    spec = agents_config['virtual_readers']['domain_specialist']
    
    system_prompt = """You are the Domain Specialist, a virtual reader who is an expert in a specific domain related to the ebook's topic.
Your responsibility is to read the content from the perspective of a domain specialist and provide feedback on its relevance and cross-disciplinary coherence.

You must follow this process:
1.  **Read for Domain Relevance**: Read the chapter to assess the relevance of the content to your specific domain.
2.  **Check for Cross-Disciplinary Coherence**: Ensure that the content is coherent with the knowledge and practices of your domain.
3.  **Identify Gaps and Inconsistencies**: Note any gaps, inconsistencies, or contextual misalignments.
4.  **Format the Output**: Present your feedback as a JSON object with a 'relevance_rating' (0-100), 'applicability_feedback' (an array of strings), and 'expert_suggestions' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


def create_reflective_reader_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Virtual Reader: Reflective Reader - Empathy and emotional impact."""
    agents_config = get_agents_config()
    spec = agents_config['virtual_readers']['reflective_reader']
    
    system_prompt = """You are the Reflective Reader, a virtual reader who values meaning, empathy, and emotional impact.
Your responsibility is to read the content from a reflective and personal perspective, providing feedback on its emotional resonance and purpose.

You must follow this process:
1.  **Read for Meaning and Impact**: Read the chapter to assess its emotional impact and the depth of its message.
2.  **Look for Emotional Connection**: Check if the content creates an emotional connection with the reader.
3.  **Assess the Sense of Purpose**: Ensure that the content has a clear sense of purpose and leaves the reader with a lasting impression.
4.  **Format the Output**: Present your feedback as a JSON object with a 'meaning_rating' (0-100), 'emotional_impact' (a string), 'reflective_feedback' (an array of strings), and 'suggestions' (an array of strings).
"""
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=system_prompt
    )


__all__ = [
    "create_ideation_agent",
    "create_title_agent",
    "create_structure_agent",
    "create_deep_research_agent",
    "create_chapter_agent",
    "create_review_coordinator_agent",
    "create_critical_reading_coordinator_agent",
    "create_editing_agent",
    "create_finalization_agent",
    "create_publication_agent",
    "create_technical_reviewer_agent",
    "create_editorial_reviewer_agent",
    "create_content_stylist_agent",
    "create_governance_agent",
    "create_ethics_validator_agent",
    "create_author_stories_reviewer_agent",
    "create_author_positioning_reviewer_agent",
    "create_author_vision_reviewer_agent",
    "create_code_examples_reviewer_agent",
    "create_research_validator_agent",
    "create_curious_beginner_agent",
    "create_technical_professional_agent",
    "create_didactic_educator_agent",
    "create_domain_specialist_agent",
    "create_reflective_reader_agent",
    "execute_agent",
    "execute_review_personas",
]
