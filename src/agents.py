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
    """Execute an agent with a query and return the response as a string."""
    try:
        response = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        
        if isinstance(response, dict):
            if "output" in response:
                return response["output"]
            elif "messages" in response:
                messages = response.get("messages", [])
                return messages[-1].content if messages else ""
        
        return str(response)
    except Exception as e:
        logger.error(f"Agent execution error: {str(e)}")
        return f"Error executing agent: {str(e)}"


def execute_review_personas(personas_agents: dict, content: str) -> dict:
    """Execute all review personas on content and collect feedback."""
    feedback = {}
    for persona_name, agent in personas_agents.items():
        try:
            query = f"Review the following content:\n\n{content[:1000]}\n\nProvide detailed feedback."
            response = execute_agent(agent, query)
            feedback[persona_name] = response
        except Exception as e:
            logger.error(f"Error executing {persona_name}: {str(e)}")
            feedback[persona_name] = f"Error: {str(e)}"
    return feedback


def create_ideation_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 1: Ideation Agent - Generate central idea and problem definition."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['ideation_agent']
    
    return create_agent(
        model=model,
        tools=get_ideation_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_title_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 2: Title Generation Agent - Generate Amazon-optimized titles."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['title_agent']
    
    return create_agent(
        model=model,
        tools=get_title_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_structure_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 3: Structure Agent - Build hierarchical outline."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['structure_agent']
    
    return create_agent(
        model=model,
        tools=get_structure_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_deep_research_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 4A: Deep Research Agent - Gather and vectorize research."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['deep_research_agent']
    
    return create_agent(
        model=model,
        tools=get_deep_research_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_chapter_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Stage 4B: Chapter Writing Agent - Write didactic content with RAG integration."""
    agents_config = get_agents_config()
    spec = agents_config['main_pipeline_agents']['chapter_writing_agent']
    
    return create_agent(
        model=model,
        tools=get_chapter_writing_tools(),
        system_prompt=_build_system_prompt(spec)
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
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_editorial_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Editorial Reviewer - Clarity and tone."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['editorial_reviewer']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_content_stylist_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Content Stylist - Formatting and consistency."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['content_stylist']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_governance_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Governance QA - Compliance and security."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['governance_qa']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_ethics_validator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Ethics Validator - Bias detection and AI ethics."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['ethics_validator']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_author_stories_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Author Stories Reviewer - Narrative balance."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['author_stories_reviewer']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_author_positioning_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Author Positioning Reviewer - Authority and positioning."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['author_positioning_reviewer']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_author_vision_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Author Vision Reviewer - Values and philosophy alignment."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['author_vision_reviewer']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_code_examples_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Code Examples Reviewer - Code execution and validation."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['code_examples_reviewer']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_research_validator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Review Persona: Research Validator - Source credibility and fact-checking."""
    agents_config = get_agents_config()
    spec = agents_config['review_personas']['research_validator']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_curious_beginner_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Virtual Reader: Curious Beginner - Clarity and accessibility."""
    agents_config = get_agents_config()
    spec = agents_config['virtual_readers']['curious_beginner']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_technical_professional_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Virtual Reader: Technical Professional - Depth and relevance."""
    agents_config = get_agents_config()
    spec = agents_config['virtual_readers']['technical_professional']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_didactic_educator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Virtual Reader: Didactic Educator - Pedagogical structure."""
    agents_config = get_agents_config()
    spec = agents_config['virtual_readers']['didactic_educator']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_domain_specialist_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Virtual Reader: Domain Specialist - Cross-disciplinary coherence."""
    agents_config = get_agents_config()
    spec = agents_config['virtual_readers']['domain_specialist']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
    )


def create_reflective_reader_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Virtual Reader: Reflective Reader - Empathy and emotional impact."""
    agents_config = get_agents_config()
    spec = agents_config['virtual_readers']['reflective_reader']
    
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt=_build_system_prompt(spec)
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
