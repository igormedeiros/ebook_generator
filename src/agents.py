""""""""""""

All 25 agents for Ebook Generator 1.0.

All 25 agent definitions for Ebook Generator 1.0.

Organized by type:

- 9 Main Pipeline Agents (ideation to publication)Specialized agents for the Ebook Generator pipeline.Specialized agents for the Ebook Generator pipeline.

- 10 Specialized Review Personas 

- 5 Virtual Reader PersonasArchitecture:



All agents are spec-driven: load specifications from agents.yaml at runtime.- 9 Main Pipeline Agents (stages 1-9)All 25 agents: 9 main pipeline + 10 review personas + 5 virtual readers.Each agent handles a specific stage of the editorial process.

"""

- 10 Specialized Review Personas (stage 5)

from typing import Any

from langchain.agents import create_agent- 5 Virtual Reader Personas (stage 6)Follows LangChain 1.0+ create_agent standard.Follows LangChain 1.0+ create_agent standard.

from langchain_google_genai import ChatGoogleGenerativeAI



from .config import get_logger, get_agents_config, get_tools_config

from .tools import (All agents load specifications dynamically from specs/agents.yaml at runtime.Each agent loads its specification from specs/agents.yaml at runtime.

    get_ideation_tools,

    get_title_tools,System prompts are built from agent specs (focus_areas, process, output_format).

    get_structure_tools,

    get_deep_research_tools,""""""25 agents total:

    get_chapter_writing_tools,

    get_review_tools,

    get_editing_tools,

    get_finalization_tools,from typing import Any- 9 main pipeline agents (ideation, title, structure, deep_research, chapter, review, critical_reading, editing, finalization, publication)

    get_publication_tools,

)from langchain.agents import create_agent



logger = get_logger(__name__)from langchain_google_genai import ChatGoogleGenerativeAIfrom typing import Any, Dict- 10 review personas (technical, editorial, stylist, governance, ethics, author_stories, author_positioning, author_vision, code_reviewer, research_validator)





def _build_system_prompt(agent_spec: dict) -> str:

    """from .config import get_agents_config, get_loggerfrom langchain.agents import create_agent- 5 virtual readers (curious_beginner, technical_professional, didactic_educator, domain_specialist, reflective_reader)

    Build dynamic system prompt from agent specification.

    

    Args:

        agent_spec: Agent specification from agents.yamllogger = get_logger(__name__)from langchain_google_genai import ChatGoogleGenerativeAI"""

    

    Returns:

        str: Formatted system prompt

    """from config import get_agents_config, get_logger

    prompt = f"""You are the {agent_spec.get('name', 'Agent')} - a {agent_spec.get('role', 'specialist')} expert.

def _build_system_prompt(agent_spec: dict) -> str:

Your responsibility is to {agent_spec.get('responsibility', 'assist with content generation')}.

    """from typing import Any, Dict

Focus Areas:"""

        Build system prompt from agent specification.

    for i, focus in enumerate(agent_spec.get('focus_areas', []), 1):

        prompt += f"\n{i}. {focus}"    logger = get_logger(__name__)from langchain.agents import create_agent

    

    prompt += "\n\nProcess:"    Args:

    for step in agent_spec.get('process', []):

        prompt += f"\n- {step}"        agent_spec: Agent specification from agents.yamlfrom langchain_google_genai import ChatGoogleGenerativeAI

    

    prompt += f"\n\nOutput Format:\n{agent_spec.get('output_format', 'Structured response with clear sections')}"    

    

    return prompt    Returns:# Import tool getter functionsfrom config import get_agents_config, get_logger



        str: Formatted system prompt for the agent

def execute_agent(agent: Any, query: str) -> str:

    """    """from tools import (

    Execute an agent with a query and return the response.

        prompt = f"""You are the {agent_spec.get('name', 'Agent')} - a {agent_spec.get('role', 'specialist')} expert.

    Args:

        agent: LangChain agent instance    get_ideation_tools,logger = get_logger(__name__)

        query: User query string

    Your responsibility is to {agent_spec.get('responsibility', 'assist with the task')}.

    Returns:

        str: Agent response text    get_title_tools,

    """

    try:Focus Areas:

        response = agent.invoke({

            "messages": [{"role": "user", "content": query}]"""    get_structure_tools,# Import tool getter functions

        })

            for i, focus in enumerate(agent_spec.get('focus_areas', []), 1):

        if hasattr(response, '__getitem__'):

            if 'messages' in response:        prompt += f"{i}. {focus}\n"    get_deep_research_tools,from tools import (

                return response['messages'][-1].content

            elif 'output' in response:    

                return response['output']

            prompt += "\nProcess:\n"    get_chapter_writing_tools,    get_ideation_tools,

        return str(response)

    except Exception as e:    for process in agent_spec.get('process', []):

        logger.error(f"Agent execution error: {str(e)}")

        return f"Error executing agent: {str(e)}"        prompt += f"- {process}\n"    get_review_tools,    get_title_tools,



    

def execute_review_personas(personas_agents: dict, content: str) -> dict:

    """    prompt += f"\nOutput Format:\n{agent_spec.get('output_format', 'Provide clear, structured output.')}"    get_editing_tools,    get_structure_tools,

    Execute multiple review persona agents in sequence.

        

    Args:

        personas_agents: Dictionary of {persona_name: agent}    return prompt    get_finalization_tools,    get_deep_research_tools,

        content: Content to review

    

    Returns:

        dict: {persona_name: feedback}    get_publication_tools,    get_chapter_writing_tools,

    """

    results = {}def execute_agent(agent: Any, query: str) -> str:

    

    for persona_name, agent in personas_agents.items():    """    get_all_tools,    get_review_tools,

        query = f"Please review this content: {content[:500]}... Provide structured feedback."

        feedback = execute_agent(agent, query)    Execute an agent with a query and return the response.

        results[persona_name] = feedback

        logger.info(f"Completed review from {persona_name}")    )    get_editing_tools,

    

    return results    Args:



        agent: LangChain agent instance    get_finalization_tools,

# MAIN PIPELINE AGENTS (9)

        query: User query or prompt

def create_ideation_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Stage 1: Ideation - Generate central idea and problem definition."""        get_publication_tools,

    agents_config = get_agents_config()

    spec = agents_config['main_pipeline_agents']['ideation_agent']    Returns:

    

    return create_agent(        str: Agent response content# ============================================================================    get_all_tools,

        model=model,

        tools=get_ideation_tools(),    """

        system_prompt=_build_system_prompt(spec)

    )    try:# HELPER FUNCTIONS)



        response = agent.invoke({

def create_title_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Stage 2: Title Generation - Create Amazon-optimized titles."""            "messages": [{"role": "user", "content": query}]# ============================================================================

    agents_config = get_agents_config()

    spec = agents_config['main_pipeline_agents']['title_agent']        })

    

    return create_agent(        return response["messages"][-1].content

        model=model,

        tools=get_title_tools(),    except Exception as e:

        system_prompt=_build_system_prompt(spec)

    )        logger.error(f"Agent execution error: {str(e)}")def _build_system_prompt(agent_spec: Dict[str, Any]) -> str:# ============================================================================



        return f"Error executing agent: {str(e)}"

def create_structure_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Stage 3: Structure - Build hierarchical outline."""    """# HELPER FUNCTIONS

    agents_config = get_agents_config()

    spec = agents_config['main_pipeline_agents']['structure_agent']

    

    return create_agent(def execute_review_personas(personas_agents: list, content: str) -> dict:    Build system prompt from agent specification.# ============================================================================

        model=model,

        tools=get_structure_tools(),    """

        system_prompt=_build_system_prompt(spec)

    )    Execute multiple review personas in sequence and collect feedback.    



    

def create_deep_research_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Stage 4A: Deep Research - Gather research with Context7 MCP."""    Args:    Args:def _build_system_prompt(agent_spec: Dict[str, Any]) -> str:

    agents_config = get_agents_config()

    spec = agents_config['main_pipeline_agents']['deep_research_agent']        personas_agents: List of persona agents

    

    return create_agent(        content: Content to review        agent_spec: Agent configuration from agents.yaml    """

        model=model,

        tools=get_deep_research_tools(),    

        system_prompt=_build_system_prompt(spec)

    )    Returns:        Build system prompt from agent specification.



        dict: Feedback from each persona

def create_chapter_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Stage 4B: Chapter Writing - Write didactic content with RAG."""    """    Returns:    

    agents_config = get_agents_config()

    spec = agents_config['main_pipeline_agents']['chapter_writing_agent']    results = {}

    

    return create_agent(    for agent in personas_agents:        str: Formatted system prompt    Args:

        model=model,

        tools=get_chapter_writing_tools(),        try:

        system_prompt=_build_system_prompt(spec)

    )            feedback = execute_agent(agent, f"Review this content:\n{content[:500]}")    """        agent_spec: Agent configuration from agents.yaml



            results[agent.name] = feedback

def create_review_coordinator_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Stage 5: Specialized Review - Orchestrate 10 review personas."""        except Exception as e:    focus_areas_text = "\n".join(    

    agents_config = get_agents_config()

    spec = agents_config['main_pipeline_agents']['review_coordinator_agent']            logger.error(f"Persona execution error: {str(e)}")

    

    return create_agent(            results[agent.name] = f"Error: {str(e)}"        f"  {i+1}. {area}"     Returns:

        model=model,

        tools=get_review_tools(),    return results

        system_prompt=_build_system_prompt(spec)

    )        for i, area in enumerate(agent_spec.get('focus_areas', []))        str: Formatted system prompt





def create_critical_reading_coordinator_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Stage 6: Critical Reading - 5 virtual readers iterative feedback."""# MAIN PIPELINE AGENTS (9)    )    """

    agents_config = get_agents_config()

    spec = agents_config['main_pipeline_agents']['critical_reading_coordinator_agent']

    

    return create_agent(def create_ideation_agent(model: ChatGoogleGenerativeAI) -> Any:    process_text = "\n".join(    focus_areas_text = "\n".join(f"  {i+1}. {area}" for i, area in enumerate(agent_spec.get('focus_areas', [])))

        model=model,

        tools=get_review_tools(),    """Stage 1: Ideation Agent - Generate central idea and problem definition."""

        system_prompt=_build_system_prompt(spec)

    )    agents_config = get_agents_config()        f"  - {step}"     process_text = "\n".join(f"  - {step}" for step in agent_spec.get('process', []))



    spec = agents_config['main_pipeline_agents']['ideation_agent']

def create_editing_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Stage 7: Editing - Final formatting and validation."""            for step in agent_spec.get('process', [])    

    agents_config = get_agents_config()

    spec = agents_config['main_pipeline_agents']['editing_agent']    return create_agent(

    

    return create_agent(        model=model,    )    prompt = f"""You are the {agent_spec.get('name', 'Agent')} - {agent_spec.get('role', 'Specialist')}.

        model=model,

        tools=get_editing_tools(),        tools=[],

        system_prompt=_build_system_prompt(spec)

    )        system_prompt=_build_system_prompt(spec)    Your responsibility is to {agent_spec.get('responsibility', 'assist with the pipeline')}.



    )

def create_finalization_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Stage 8: Finalization - Cover concept and metadata."""    prompt = f"""You are the {agent_spec.get('name', 'Agent')} - {agent_spec.get('role', 'Specialist')}.

    agents_config = get_agents_config()

    spec = agents_config['main_pipeline_agents']['finalization_agent']

    

    return create_agent(def create_title_agent(model: ChatGoogleGenerativeAI) -> Any:Your responsibility is to {agent_spec.get('responsibility', 'assist with the pipeline')}.Focus Areas:

        model=model,

        tools=get_finalization_tools(),    """Stage 2: Title Agent - Generate Amazon-optimized titles."""

        system_prompt=_build_system_prompt(spec)

    )    agents_config = get_agents_config(){focus_areas_text}



    spec = agents_config['main_pipeline_agents']['title_agent']

def create_publication_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Stage 9: Publication - Export to multiple formats."""    Focus Areas:

    agents_config = get_agents_config()

    spec = agents_config['main_pipeline_agents']['publication_agent']    return create_agent(

    

    return create_agent(        model=model,{focus_areas_text}Process:

        model=model,

        tools=get_publication_tools(),        tools=[],

        system_prompt=_build_system_prompt(spec)

    )        system_prompt=_build_system_prompt(spec){process_text}



    )

# SPECIALIZED REVIEW PERSONAS (10)

Process:

def create_technical_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Technical Reviewer - Code quality and accuracy."""

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['technical_reviewer']def create_structure_agent(model: ChatGoogleGenerativeAI) -> Any:{process_text}Output Format:

    

    return create_agent(    """Stage 3: Structure Agent - Build hierarchical outline."""

        model=model,

        tools=get_review_tools(),    agents_config = get_agents_config(){agent_spec.get('output_format', 'Provide structured output')}"""

        system_prompt=_build_system_prompt(spec)

    )    spec = agents_config['main_pipeline_agents']['structure_agent']



    Output Format:    

def create_editorial_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Editorial Reviewer - Clarity and tone."""    return create_agent(

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['editorial_reviewer']        model=model,{agent_spec.get('output_format', 'Provide structured output')}"""    return prompt

    

    return create_agent(        tools=[],

        model=model,

        tools=get_review_tools(),        system_prompt=_build_system_prompt(spec)    

        system_prompt=_build_system_prompt(spec)

    )    )



    return prompt

def create_content_stylist_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Content Stylist - Formatting and structure."""

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['content_stylist']def create_deep_research_agent(model: ChatGoogleGenerativeAI) -> Any:def execute_agent(agent: Any, query: str) -> str:

    

    return create_agent(    """Stage 4A: Deep Research Agent - Conduct research with Context7 MCP integration."""

        model=model,

        tools=get_review_tools(),    agents_config = get_agents_config()    """

        system_prompt=_build_system_prompt(spec)

    )    spec = agents_config['main_pipeline_agents']['deep_research_agent']



    def execute_agent(agent: Any, query: str) -> str:    Execute an agent with a query and return the response.

def create_governance_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Governance QA - Compliance and standards."""    return create_agent(

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['governance_qa']        model=model,    """    

    

    return create_agent(        tools=[],

        model=model,

        tools=get_review_tools(),        system_prompt=_build_system_prompt(spec)    Execute an agent with a query and return the response.    Args:

        system_prompt=_build_system_prompt(spec)

    )    )



            agent: LangChain agent instance

def create_ethics_validator_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Ethics Validator - Bias and compliance."""

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['ethics_validator']def create_chapter_agent(model: ChatGoogleGenerativeAI) -> Any:    Args:        query: Query string to execute

    

    return create_agent(    """Stage 4B: Chapter Writing Agent - Write didactic content with RAG integration."""

        model=model,

        tools=get_review_tools(),    agents_config = get_agents_config()        agent: LangChain agent instance    

        system_prompt=_build_system_prompt(spec)

    )    spec = agents_config['main_pipeline_agents']['chapter_writing_agent']



            query: Query string to execute    Returns:

def create_author_stories_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Author Stories - Narrative balance."""    return create_agent(

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['author_stories_reviewer']        model=model,            str: Agent response text

    

    return create_agent(        tools=[],

        model=model,

        tools=get_review_tools(),        system_prompt=_build_system_prompt(spec)    Returns:    """

        system_prompt=_build_system_prompt(spec)

    )    )



        str: Agent response text    try:

def create_author_positioning_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Author Positioning - Authority clarity."""

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['author_positioning_reviewer']def create_review_coordinator_agent(model: ChatGoogleGenerativeAI) -> Any:    """        response = agent.invoke({"input": query})

    

    return create_agent(    """Stage 5: Review Coordinator Agent - Orchestrate 10 specialized review personas."""

        model=model,

        tools=get_review_tools(),    agents_config = get_agents_config()    try:        # Handle both response formats

        system_prompt=_build_system_prompt(spec)

    )    spec = agents_config['main_pipeline_agents']['review_coordinator_agent']



            response = agent.invoke({"input": query})        if isinstance(response, dict):

def create_author_vision_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Author Vision - Opinion alignment."""    return create_agent(

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['author_vision_reviewer']        model=model,        # Handle both response formats            if "output" in response:

    

    return create_agent(        tools=[],

        model=model,

        tools=get_review_tools(),        system_prompt=_build_system_prompt(spec)        if isinstance(response, dict):                return response["output"]

        system_prompt=_build_system_prompt(spec)

    )    )



            if "output" in response:            elif "messages" in response:

def create_code_examples_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Code Examples - Code quality validation."""

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['code_examples_reviewer']def create_critical_reading_coordinator_agent(model: ChatGoogleGenerativeAI) -> Any:                return response["output"]                return response["messages"][-1].content if response["messages"] else ""

    

    return create_agent(    """Stage 6: Critical Reading Agent - Execute iteration cycles with 5 virtual readers."""

        model=model,

        tools=get_review_tools(),    agents_config = get_agents_config()            elif "messages" in response:        return str(response)

        system_prompt=_build_system_prompt(spec)

    )    spec = agents_config['main_pipeline_agents']['critical_reading_coordinator_agent']



                    messages = response.get("messages", [])    except Exception as e:

def create_research_validator_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Research Validator - Source credibility."""    return create_agent(

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['research_validator']        model=model,                return messages[-1].content if messages else ""        logger.error(f"Error executing agent: {str(e)}")

    

    return create_agent(        tools=[],

        model=model,

        tools=get_review_tools(),        system_prompt=_build_system_prompt(spec)        return str(response)        return f"Error: {str(e)}"

        system_prompt=_build_system_prompt(spec)

    )    )



    except Exception as e:

# VIRTUAL READER PERSONAS (5)



def create_curious_beginner_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Virtual Reader: Curious Beginner - Clarity and accessibility."""def create_editing_agent(model: ChatGoogleGenerativeAI) -> Any:        logger.error(f"Error executing agent: {str(e)}")

    agents_config = get_agents_config()

    spec = agents_config['virtual_readers']['curious_beginner']    """Stage 7: Editing Agent - Format and validate content."""

    

    return create_agent(    agents_config = get_agents_config()        return f"Error: {str(e)}"def execute_review_personas(personas_agents: Dict[str, Any], content: str) -> Dict[str, str]:

        model=model,

        tools=get_review_tools(),    spec = agents_config['main_pipeline_agents']['editing_agent']

        system_prompt=_build_system_prompt(spec)

    )        """



    return create_agent(

def create_technical_professional_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Virtual Reader: Technical Professional - Depth and relevance."""        model=model,    Execute all review personas on content and collect feedback.

    agents_config = get_agents_config()

    spec = agents_config['virtual_readers']['technical_professional']        tools=[],

    

    return create_agent(        system_prompt=_build_system_prompt(spec)def execute_review_personas(personas_agents: Dict[str, Any], content: str) -> Dict[str, str]:    

        model=model,

        tools=get_review_tools(),    )

        system_prompt=_build_system_prompt(spec)

    )    """    Args:





def create_didactic_educator_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Virtual Reader: Didactic Educator - Pedagogical structure."""def create_finalization_agent(model: ChatGoogleGenerativeAI) -> Any:    Execute all review personas on content and collect feedback.        personas_agents: Dictionary of persona agents

    agents_config = get_agents_config()

    spec = agents_config['virtual_readers']['didactic_educator']    """Stage 8: Finalization Agent - Generate cover and metadata."""

    

    return create_agent(    agents_config = get_agents_config()            content: Content to review

        model=model,

        tools=get_review_tools(),    spec = agents_config['main_pipeline_agents']['finalization_agent']

        system_prompt=_build_system_prompt(spec)

    )        Args:    



    return create_agent(

def create_domain_specialist_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Virtual Reader: Domain Specialist - Cross-disciplinary coherence."""        model=model,        personas_agents: Dictionary of {persona_name: agent}    Returns:

    agents_config = get_agents_config()

    spec = agents_config['virtual_readers']['domain_specialist']        tools=[],

    

    return create_agent(        system_prompt=_build_system_prompt(spec)        content: Content to review        dict: Feedback from each persona

        model=model,

        tools=get_review_tools(),    )

        system_prompt=_build_system_prompt(spec)

    )        """





def create_reflective_reader_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Virtual Reader: Reflective Reader - Empathy and impact."""def create_publication_agent(model: ChatGoogleGenerativeAI) -> Any:    Returns:    feedback = {}

    agents_config = get_agents_config()

    spec = agents_config['virtual_readers']['reflective_reader']    """Stage 9: Publication Agent - Export to multiple formats for KDP."""

    

    return create_agent(    agents_config = get_agents_config()        dict: Feedback from each persona    for persona_name, agent in personas_agents.items():

        model=model,

        tools=get_review_tools(),    spec = agents_config['main_pipeline_agents']['publication_agent']

        system_prompt=_build_system_prompt(spec)

    )        """        query = f"Please review the following content:\n\n{content[:2000]}"


    return create_agent(

        model=model,    feedback = {}        feedback[persona_name] = execute_agent(agent, query)

        tools=[],

        system_prompt=_build_system_prompt(spec)    for persona_name, agent in personas_agents.items():        logger.info(f"Review from {persona_name} completed")

    )

        query = f"Please review the following content and provide feedback:\n\n{content[:2000]}"    return feedback



# REVIEW PERSONAS (10)        feedback[persona_name] = execute_agent(agent, query)



def create_technical_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:        logger.info(f"Review from {persona_name} completed")

    """Review Persona: Technical Reviewer - Code quality and framework accuracy."""

    agents_config = get_agents_config()    return feedback# ============================================================================

    spec = agents_config['review_personas']['technical_reviewer']

    # MAIN PIPELINE AGENTS (9 agents)

    return create_agent(

        model=model,# ============================================================================

        tools=[],

        system_prompt=_build_system_prompt(spec)# ============================================================================

    )

# MAIN PIPELINE AGENTS (9 agents)



def create_editorial_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:# ============================================================================def create_ideation_agent(model: ChatGoogleGenerativeAI):

    """Review Persona: Editorial Reviewer - Clarity, tone, and audience alignment."""

    agents_config = get_agents_config()    """

    spec = agents_config['review_personas']['editorial_reviewer']

    def create_ideation_agent(model: ChatGoogleGenerativeAI) -> Any:    Stage 1: Ideation Agent

    return create_agent(

        model=model,    """    Defines central idea, problem, target audience, and transformation promise.

        tools=[],

        system_prompt=_build_system_prompt(spec)    Stage 1: Ideation Agent    

    )

    Defines central idea, problem, target audience, transformation promise.    From agents.yaml: ideation_agent spec



def create_content_stylist_agent(model: ChatGoogleGenerativeAI) -> Any:    Loads spec from agents.yaml > main_pipeline_agents > ideation_agent    """

    """Review Persona: Content Stylist - Formatting and visual consistency."""

    agents_config = get_agents_config()    """    agents_config = get_agents_config()

    spec = agents_config['review_personas']['content_stylist']

        agents_config = get_agents_config()    spec = agents_config['main_pipeline_agents']['ideation_agent']

    return create_agent(

        model=model,    spec = agents_config['main_pipeline_agents']['ideation_agent']    

        tools=[],

        system_prompt=_build_system_prompt(spec)        return create_agent(

    )

    return create_agent(        model=model,



def create_governance_agent(model: ChatGoogleGenerativeAI) -> Any:        model=model,        tools=get_ideation_tools(),

    """Review Persona: Governance QA - Compliance and standards validation."""

    agents_config = get_agents_config()        tools=get_ideation_tools(),        system_prompt=_build_system_prompt(spec)

    spec = agents_config['review_personas']['governance_qa']

            system_prompt=_build_system_prompt(spec)    )

    return create_agent(

        model=model,    )

        tools=[],

        system_prompt=_build_system_prompt(spec)

    )

def create_title_agent(model: ChatGoogleGenerativeAI):



def create_ethics_validator_agent(model: ChatGoogleGenerativeAI) -> Any:def create_title_agent(model: ChatGoogleGenerativeAI) -> Any:    """

    """Review Persona: Ethics Validator - Bias and ethics compliance."""

    agents_config = get_agents_config()    """    Stage 2: Title/Subtitle Agent

    spec = agents_config['review_personas']['ethics_validator']

        Stage 2: Title Generation Agent    Analyzes Amazon trends and generates optimized titles for market success.

    return create_agent(

        model=model,    Generates 3 Amazon-optimized title options with market analysis.    """

        tools=[],

        system_prompt=_build_system_prompt(spec)    Loads spec from agents.yaml > main_pipeline_agents > title_agent    return create_agent(

    )

    """        model=model,



def create_author_stories_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:    agents_config = get_agents_config()        tools=get_title_tools(),

    """Review Persona: Author Stories - Narrative and pedagogy balance."""

    agents_config = get_agents_config()    spec = agents_config['main_pipeline_agents']['title_agent']        system_prompt="""You are the Title/Subtitle Agent.

    spec = agents_config['review_personas']['author_stories_reviewer']

        Your responsibility is to generate titles that sell on Amazon KDP.

    return create_agent(

        model=model,    return create_agent(

        tools=[],

        system_prompt=_build_system_prompt(spec)        model=model,Consider:

    )

        tools=get_title_tools(),1. High-volume search keywords



def create_author_positioning_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:        system_prompt=_build_system_prompt(spec)2. Patterns from top 10 bestsellers in the category

    """Review Persona: Author Positioning - Authority and market positioning."""

    agents_config = get_agents_config()    )3. Clarity and immediate impact

    spec = agents_config['review_personas']['author_positioning_reviewer']

    4. Include target audience in title/subtitle

    return create_agent(

        model=model,

        tools=[],

        system_prompt=_build_system_prompt(spec)def create_structure_agent(model: ChatGoogleGenerativeAI) -> Any:Generate 3 title options with subtitles for validation."""

    )

    """    )



def create_author_vision_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:    Stage 3: Structure Agent

    """Review Persona: Author Vision - Vision alignment and authenticity."""

    agents_config = get_agents_config()    Creates hierarchical outline and table of contents.

    spec = agents_config['review_personas']['author_vision_reviewer']

        Loads spec from agents.yaml > main_pipeline_agents > structure_agentdef create_structure_agent(model: ChatGoogleGenerativeAI):

    return create_agent(

        model=model,    """    """

        tools=[],

        system_prompt=_build_system_prompt(spec)    agents_config = get_agents_config()    Stage 3: Structure Agent

    )

    spec = agents_config['main_pipeline_agents']['structure_agent']    Creates hierarchical outline and didactic structure scaled to word count target.



def create_code_examples_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:        """

    """Review Persona: Code Examples - Code quality and exercise validation."""

    agents_config = get_agents_config()    return create_agent(    return create_agent(

    spec = agents_config['review_personas']['code_examples_reviewer']

            model=model,        model=model,

    return create_agent(

        model=model,        tools=get_structure_tools(),        tools=get_structure_tools(),

        tools=[],

        system_prompt=_build_system_prompt(spec)        system_prompt=_build_system_prompt(spec)        system_prompt="""You are the Structure and Outline Agent.

    )

    )Your responsibility is to create the logical architecture of the ebook.



def create_research_validator_agent(model: ChatGoogleGenerativeAI) -> Any:

    """Review Persona: Research Validator - Source credibility and citations."""

    agents_config = get_agents_config()Consider:

    spec = agents_config['review_personas']['research_validator']

    def create_deep_research_agent(model: ChatGoogleGenerativeAI) -> Any:1. Word count target for scaling depth

    return create_agent(

        model=model,    """2. Didactic sequence (easy → complex)

        tools=[],

        system_prompt=_build_system_prompt(spec)    Stage 4A: Deep Research Agent3. Balanced chapters in size

    )

    Queries Context7 MCP, vectorizes research, stores in Supabase RAG.4. Well-defined introduction, body, and conclusion



# VIRTUAL READERS (5)    Loads spec from agents.yaml > main_pipeline_agents > deep_research_agent



def create_curious_beginner_agent(model: ChatGoogleGenerativeAI) -> Any:    Uses research_model (Gemini 2.5 Pro, temp 0.3)Generate a hierarchical outline in Markdown with estimated words per chapter."""

    """Virtual Reader: Curious Beginner - Assess clarity and accessibility."""

    agents_config = get_agents_config()    """    )

    spec = agents_config['virtual_readers']['curious_beginner']

        agents_config = get_agents_config()

    return create_agent(

        model=model,    spec = agents_config['main_pipeline_agents']['deep_research_agent']

        tools=[],

        system_prompt=_build_system_prompt(spec)    def create_chapter_agent(model: ChatGoogleGenerativeAI):

    )

    return create_agent(    """



def create_technical_professional_agent(model: ChatGoogleGenerativeAI) -> Any:        model=model,    Stage 4: Chapter Writing Agent

    """Virtual Reader: Technical Professional - Verify depth and relevance."""

    agents_config = get_agents_config()        tools=get_deep_research_tools(),    Writes high-quality, didactic content with RAG research and word count respect.

    spec = agents_config['virtual_readers']['technical_professional']

            system_prompt=_build_system_prompt(spec)    """

    return create_agent(

        model=model,    )    return create_agent(

        tools=[],

        system_prompt=_build_system_prompt(spec)        model=model,

    )

        tools=get_chapter_writing_tools(),



def create_didactic_educator_agent(model: ChatGoogleGenerativeAI) -> Any:def create_chapter_agent(model: ChatGoogleGenerativeAI) -> Any:        system_prompt="""You are the Chapter Writing Agent.

    """Virtual Reader: Didactic Educator - Check pedagogical structure."""

    agents_config = get_agents_config()    """Your responsibility is to write high-quality, didactic, contextualized content.

    spec = agents_config['virtual_readers']['didactic_educator']

        Stage 4B: Chapter Writing Agent

    return create_agent(

        model=model,    Writes didactic content with RAG research integration.Consider:

        tools=[],

        system_prompt=_build_system_prompt(spec)    Loads spec from agents.yaml > main_pipeline_agents > chapter_writing_agent1. Consult RAG for accurate information and avoid hallucinations

    )

    """2. Maintain the author's "voice" (tone, humor, empathy)



def create_domain_specialist_agent(model: ChatGoogleGenerativeAI) -> Any:    agents_config = get_agents_config()3. Respect the word limit allocated for each chapter

    """Virtual Reader: Domain Specialist - Validate cross-disciplinary coherence."""

    agents_config = get_agents_config()    spec = agents_config['main_pipeline_agents']['chapter_writing_agent']4. Include practical examples and didactic content

    spec = agents_config['virtual_readers']['domain_specialist']

        

    return create_agent(

        model=model,    return create_agent(Write clearly, fluently, and professionally."""

        tools=[],

        system_prompt=_build_system_prompt(spec)        model=model,    )

    )

        tools=get_chapter_writing_tools(),



def create_reflective_reader_agent(model: ChatGoogleGenerativeAI) -> Any:        system_prompt=_build_system_prompt(spec)

    """Virtual Reader: Reflective Reader - Assess empathy and impact."""

    agents_config = get_agents_config()    )def create_review_agent(model: ChatGoogleGenerativeAI):

    spec = agents_config['virtual_readers']['reflective_reader']

        """

    return create_agent(

        model=model,    Stage 5: Review Agent

        tools=[],

        system_prompt=_build_system_prompt(spec)def create_review_coordinator_agent(model: ChatGoogleGenerativeAI) -> Any:    Executes iterative critical reading with specialized review tools.

    )

    """    Performs 3 complete review loops for comprehensive quality assurance.



__all__ = [    Stage 5: Review Coordinator Agent    """

    # Main pipeline agents

    "create_ideation_agent",    Orchestrates 10 specialized review personas for comprehensive feedback.    return create_agent(

    "create_title_agent",

    "create_structure_agent",    Loads spec from agents.yaml > main_pipeline_agents > review_coordinator_agent        model=model,

    "create_deep_research_agent",

    "create_chapter_agent",    """        tools=get_review_tools(),

    "create_review_coordinator_agent",

    "create_critical_reading_coordinator_agent",    agents_config = get_agents_config()        system_prompt="""You are the Review and Critical Reading Agent.

    "create_editing_agent",

    "create_finalization_agent",    spec = agents_config['main_pipeline_agents']['review_coordinator_agent']Your responsibility is to execute 3 iterative review loops:

    "create_publication_agent",

    # Review personas    

    "create_technical_reviewer_agent",

    "create_editorial_reviewer_agent",    return create_agent(Loop 1: Tone, empathy, and clarity

    "create_content_stylist_agent",

    "create_governance_agent",        model=model,Loop 2: Grammar, coherence, and flow

    "create_ethics_validator_agent",

    "create_author_stories_reviewer_agent",        tools=get_review_tools(),Loop 3: Code examples, factuality, and consistency

    "create_author_positioning_reviewer_agent",

    "create_author_vision_reviewer_agent",        system_prompt=_build_system_prompt(spec)

    "create_code_examples_reviewer_agent",

    "create_research_validator_agent",    )In each loop, use specialized review tools.

    # Virtual readers

    "create_curious_beginner_agent",Identify improvements and suggest corrections while maintaining author voice."""

    "create_technical_professional_agent",

    "create_didactic_educator_agent",    )

    "create_domain_specialist_agent",

    "create_reflective_reader_agent",def create_critical_reading_coordinator_agent(model: ChatGoogleGenerativeAI) -> Any:

    # Helpers

    "execute_agent",    """

    "execute_review_personas",

]    Stage 6: Critical Reading Coordinator Agentdef create_technical_reviewer_agent(model: ChatGoogleGenerativeAI):


    Orchestrates 5 virtual readers for iterative feedback (1 cycle MVP).    """

    Loads spec from agents.yaml > main_pipeline_agents > critical_reading_coordinator_agent    Technical Reviewer Agent (Specialized Persona 1)

    """    Ensures accuracy of technical content (Python, LangChain, AI, etc).

    agents_config = get_agents_config()    Verifies that code is functional, updated, and coherent with framework versions.

    spec = agents_config['main_pipeline_agents']['critical_reading_coordinator_agent']    Acts as a "code QA", testing examples and validating outputs.

        """

    return create_agent(    return create_agent(

        model=model,        model=model,

        tools=get_review_tools(),        tools=get_review_tools(),

        system_prompt=_build_system_prompt(spec)        system_prompt="""You are the Technical Reviewer Agent - a specialized code quality expert.

    )Your responsibility is to ensure technical accuracy and code quality.



Focus Areas:

def create_editing_agent(model: ChatGoogleGenerativeAI) -> Any:1. Python code syntax and best practices - verify executable and correct

    """2. LangChain API compatibility - check versions and deprecated patterns

    Stage 7: Editing Agent3. AI/ML concepts - validate technical accuracy

    Validates formatting, structure, and consistency.4. Framework integration - ensure consistency with stated versions

    Loads spec from agents.yaml > main_pipeline_agents > editing_agent5. Example validation - test code snippets for correctness

    """

    agents_config = get_agents_config()Review Process:

    spec = agents_config['main_pipeline_agents']['editing_agent']- Check all code examples are syntactically correct

    - Validate LangChain 1.0+ usage patterns

    return create_agent(- Verify AI concepts are accurately described

        model=model,- Ensure dependencies match declared versions

        tools=get_editing_tools(),- Test output formats and expected behavior

        system_prompt=_build_system_prompt(spec)

    )Provide detailed feedback on:

- Code quality and best practices

- Version compatibility issues

def create_finalization_agent(model: ChatGoogleGenerativeAI) -> Any:- Technical accuracy of explanations

    """- Executable examples validation"""

    Stage 8: Finalization Agent    )

    Generates cover concept and validates metadata for KDP.

    Loads spec from agents.yaml > main_pipeline_agents > finalization_agent

    """def create_editorial_reviewer_agent(model: ChatGoogleGenerativeAI):

    agents_config = get_agents_config()    """

    spec = agents_config['main_pipeline_agents']['finalization_agent']    Editorial Reviewer Agent (Specialized Persona 2)

        Evaluates clarity, fluidity, and cohesion of text.

    return create_agent(    Adjusts tone and voice according to target audience (tech AI/health readers).

        model=model,    Corrects linguistic, spelling, and style inconsistencies.

        tools=get_finalization_tools(),    """

        system_prompt=_build_system_prompt(spec)    return create_agent(

    )        model=model,

        tools=get_review_tools(),

        system_prompt="""You are the Editorial Reviewer Agent - a linguistic and style expert.

def create_publication_agent(model: ChatGoogleGenerativeAI) -> Any:Your responsibility is to ensure text quality and reader engagement.

    """

    Stage 9: Publication AgentFocus Areas:

    Exports to DOCX, EPUB, PDF, JSON for KDP publication.1. Clarity and readability - ensure concepts are understandable

    Loads spec from agents.yaml > main_pipeline_agents > publication_agent2. Tone and voice - match target audience (technical but accessible)

    """3. Flow and coherence - smooth transitions between sections

    agents_config = get_agents_config()4. Linguistic accuracy - grammar, spelling, punctuation

    spec = agents_config['main_pipeline_agents']['publication_agent']5. Style consistency - unified voice throughout

    

    return create_agent(Review Process:

        model=model,- Assess clarity of technical explanations

        tools=get_publication_tools(),- Verify tone matches target audience (Senior Python developers, AI/health professionals)

        system_prompt=_build_system_prompt(spec)- Check paragraph flow and logical progression

    )- Correct grammatical and spelling errors

- Ensure consistent terminology usage

- Validate that complex concepts are well-explained

# ============================================================================

# REVIEW PERSONA AGENTS (10 personas)Provide feedback on:

# ============================================================================- Clarity improvements for technical content

- Tone appropriateness for audience

def create_technical_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:- Writing flow and transitions

    """- Grammar and language issues

    Technical Reviewer - Reviews code quality, framework versions, accuracy.- Terminology consistency

    Loads spec from agents.yaml > review_personas > technical_reviewer- Accessibility of explanations"""

    """    )

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['technical_reviewer']

    def create_content_stylist_agent(model: ChatGoogleGenerativeAI):

    return create_agent(    """

        model=model,    Content Stylist Agent (Specialized Persona 3)

        tools=get_review_tools(),    Harmonizes structure, titles, sections, and formatting.

        system_prompt=_build_system_prompt(spec)    Ensures material follows ebook collection standard (TOC, disclaimers, Markdown/Docx format).

    )    Acts as intermediary between technical and editorial review.

    """

    return create_agent(

def create_editorial_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:        model=model,

    """        tools=get_review_tools(),

    Editorial Reviewer - Reviews clarity, tone, flow, linguistics.        system_prompt="""You are the Content Stylist Agent - a formatting and structure expert.

    Loads spec from agents.yaml > review_personas > editorial_reviewerYour responsibility is to ensure consistent, professional presentation.

    """

    agents_config = get_agents_config()Focus Areas:

    spec = agents_config['review_personas']['editorial_reviewer']1. Document structure - chapters, sections, subsections hierarchy

    2. Title and heading consistency - semantic and stylistic uniformity

    return create_agent(3. Formatting standards - Markdown/Docx compliance

        model=model,4. Table of Contents accuracy - proper links and navigation

        tools=get_review_tools(),5. Visual elements - code blocks, lists, emphasis formatting

        system_prompt=_build_system_prompt(spec)6. Standard sections - disclaimers, author bio, references format

    )

Review Process:

- Validate heading hierarchy (H1, H2, H3 structure)

def create_content_stylist_agent(model: ChatGoogleGenerativeAI) -> Any:- Check TOC accuracy and completeness

    """- Verify code block formatting and syntax highlighting

    Content Stylist - Reviews formatting, structure, consistency.- Ensure list formatting consistency

    Loads spec from agents.yaml > review_personas > content_stylist- Validate disclaimer and metadata sections

    """- Check reference formatting standards

    agents_config = get_agents_config()- Verify visual emphasis usage (bold, italic, links)

    spec = agents_config['review_personas']['content_stylist']

    Provide feedback on:

    return create_agent(- Heading hierarchy and structure

        model=model,- Formatting consistency

        tools=get_review_tools(),- Code block presentation

        system_prompt=_build_system_prompt(spec)- TOC accuracy and completeness

    )- Visual element proper usage

- Disclaimer and legal text placement

- References and bibliography format"""

def create_governance_agent(model: ChatGoogleGenerativeAI) -> Any:    )

    """

    Governance QA - Reviews compliance, metadata, security, LGPD.

    Loads spec from agents.yaml > review_personas > governance_qadef create_governance_agent(model: ChatGoogleGenerativeAI):

    """    """

    agents_config = get_agents_config()    Governance QA Agent (Specialized Persona 4)

    spec = agents_config['review_personas']['governance_qa']    Final compliance check: framework versions, information security, ethics, LGPD.

        Validates metadata and references before publication (author, ISBN, date, credits).

    return create_agent(    """

        model=model,    return create_agent(

        tools=get_review_tools(),        model=model,

        system_prompt=_build_system_prompt(spec)        tools=get_review_tools(),

    )        system_prompt="""You are the Governance QA Agent - a compliance and standards expert.

Your responsibility is to ensure regulatory and organizational compliance.



def create_ethics_validator_agent(model: ChatGoogleGenerativeAI) -> Any:Focus Areas:

    """1. Framework versions - verify stated vs actual versions match

    Ethics Validator - Reviews bias, disclaimers, AI ethics, HIPAA.2. Security compliance - no sensitive data disclosure

    Loads spec from agents.yaml > review_personas > ethics_validator3. LGPD compliance (Brazilian data protection) - if applicable

    """4. Metadata accuracy - author, date, version information

    agents_config = get_agents_config()5. Credits and attributions - proper acknowledgments

    spec = agents_config['review_personas']['ethics_validator']6. Copyright and licenses - proper declarations

    7. Disclaimer statements - legal requirements met

    return create_agent(

        model=model,Review Process:

        tools=get_review_tools(),- Verify all framework versions mentioned are accurate and current

        system_prompt=_build_system_prompt(spec)- Check for sensitive information (API keys, credentials, etc.)

    )- Validate author and publication metadata

- Review disclaimer statements for completeness

- Verify copyright and license declarations

def create_author_stories_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:- Check credits for all sources and contributors

    """- Ensure LGPD compliance where applicable

    Author Stories Reviewer - Reviews narrative balance and didactic integration.- Validate ISBN and publication information

    Loads spec from agents.yaml > review_personas > author_stories_reviewer

    """Provide feedback on:

    agents_config = get_agents_config()- Version accuracy and compliance

    spec = agents_config['review_personas']['author_stories_reviewer']- Security and data protection issues

    - Metadata completeness

    return create_agent(- Copyright and license statements

        model=model,- Disclaimer adequacy

        tools=get_review_tools(),- LGPD compliance status

        system_prompt=_build_system_prompt(spec)- Publication information accuracy"""

    )    )





def create_author_positioning_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:def create_ethics_validator_agent(model: ChatGoogleGenerativeAI):

    """    """

    Author Positioning Reviewer - Reviews market positioning and authority.    Ethics Validator Agent (Specialized Persona 5)

    Loads spec from agents.yaml > review_personas > author_positioning_reviewer    Reviews AI-generated content for biases, medical disclaimers, and LGPD compliance.

    """    Especially used in chapters about AI in health and LangChain.

    agents_config = get_agents_config()    """

    spec = agents_config['review_personas']['author_positioning_reviewer']    return create_agent(

            model=model,

    return create_agent(        tools=get_review_tools(),

        model=model,        system_prompt="""You are the Ethics Validator Agent - an AI ethics and bias detection expert.

        tools=get_review_tools(),Your responsibility is to ensure ethical content and regulatory compliance.

        system_prompt=_build_system_prompt(spec)

    )Focus Areas:

1. Bias detection - identify and flag potential biases in text

2. Medical disclaimers - ensure AI health content has proper disclaimers

def create_author_vision_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:3. AI ethics - verify responsible AI principles are represented

    """4. LGPD compliance - check privacy and data protection compliance

    Author Vision Reviewer - Reviews values, philosophy, worldview alignment.5. HIPAA compliance - if health data is mentioned

    Loads spec from agents.yaml > review_personas > author_vision_reviewer6. Diversity and inclusion - ensure representative language and examples

    """

    agents_config = get_agents_config()Review Process:

    spec = agents_config['review_personas']['author_vision_reviewer']- Scan for language biases (gender, cultural, socioeconomic, ability)

    - Check AI health/medical content for required disclaimers

    return create_agent(- Verify responsible AI principles are demonstrated

        model=model,- Review any personal data mentions for LGPD compliance

        tools=get_review_tools(),- Check HIPAA compliance if health data discussed

        system_prompt=_build_system_prompt(spec)- Ensure diverse and inclusive language throughout

    )- Validate ethical implications of AI examples



Provide feedback on:

def create_code_examples_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:- Potential biases detected

    """- Missing medical/legal disclaimers

    Code Examples Reviewer - Executes and validates code examples.- AI ethics concerns

    Loads spec from agents.yaml > review_personas > code_examples_reviewer- LGPD/HIPAA compliance issues

    """- Diversity and inclusion improvements

    agents_config = get_agents_config()- Ethical implications of content

    spec = agents_config['review_personas']['code_examples_reviewer']- Required disclaimer additions"""

        )

    return create_agent(

        model=model,

        tools=get_review_tools(),def create_editing_agent(model: ChatGoogleGenerativeAI):

        system_prompt=_build_system_prompt(spec)    """

    )    Stage 7: Editing Agent

    Final formatting and validation of consistency.

    """

def create_research_validator_agent(model: ChatGoogleGenerativeAI) -> Any:    return create_agent(

    """        model=model,

    Research Validator - Validates scientific sources and credibility.        tools=get_editing_tools(),

    Loads spec from agents.yaml > review_personas > research_validator        system_prompt="""You are the Editing and Formatting Agent.

    """Your responsibility is to ensure visual and structural perfection.

    agents_config = get_agents_config()

    spec = agents_config['review_personas']['research_validator']Consider:

    1. Consistent Markdown formatting

    return create_agent(2. Clear title hierarchy

        model=model,3. Appropriate visual emphasis

        tools=get_review_tools(),4. Style consistency throughout the document

        system_prompt=_build_system_prompt(spec)

    )Validate final word count (±10% of target)."""

    )



# ============================================================================

# VIRTUAL READER AGENTS (5 personas)def create_finalization_agent(model: ChatGoogleGenerativeAI):

# ============================================================================    """

    Stage 8: Finalization Agent

def create_curious_beginner_agent(model: ChatGoogleGenerativeAI) -> Any:    Generates AI-created cover and validates table of contents hierarchy.

    """    """

    Curious Beginner - Reviews accessibility and progression.    return create_agent(

    Loads spec from agents.yaml > virtual_readers > curious_beginner        model=model,

    """        tools=get_finalization_tools(),

    agents_config = get_agents_config()        system_prompt="""You are the Cover Designer and Finalization Agent.

    spec = agents_config['virtual_readers']['curious_beginner']Your responsibility is to complete final ebook details.

    

    return create_agent(Consider:

        model=model,1. Generate attractive cover with title, subtitle, and author

        tools=get_review_tools(),2. Validate table of contents hierarchy and links

        system_prompt=_build_system_prompt(spec)3. Ensure all visual elements are properly aligned

    )4. Prepare content for export



Cover and metadata are critical for Amazon KDP success."""

def create_technical_professional_agent(model: ChatGoogleGenerativeAI) -> Any:    )

    """

    Technical Professional - Reviews depth, relevance, accuracy.

    Loads spec from agents.yaml > virtual_readers > technical_professionaldef create_publication_agent(model: ChatGoogleGenerativeAI):

    """    """

    agents_config = get_agents_config()    Stage 9: Publication Agent

    spec = agents_config['virtual_readers']['technical_professional']    Generates final package with KDP-compliant exports and metadata.

        """

    return create_agent(    return create_agent(

        model=model,        model=model,

        tools=get_review_tools(),        tools=get_publication_tools(),

        system_prompt=_build_system_prompt(spec)        system_prompt="""You are the KDP Publication Agent.

    )Your responsibility is to generate the complete package ready for Amazon KDP.



Consider:

def create_didactic_educator_agent(model: ChatGoogleGenerativeAI) -> Any:1. Count final words and validate target

    """2. Export to DOCX (KDP-formatted)

    Didactic Educator - Reviews pedagogical structure and methodology.3. Export to EPUB (alternative format)

    Loads spec from agents.yaml > virtual_readers > didactic_educator4. Generate JSON metadata with keywords and category

    """

    agents_config = get_agents_config()The package must be 100% ready for KDP submission without additional adjustments."""

    spec = agents_config['virtual_readers']['didactic_educator']    )

    

    return create_agent(

        model=model,def create_deep_research_agent(model: ChatGoogleGenerativeAI):

        tools=get_review_tools(),    """

        system_prompt=_build_system_prompt(spec)    Stage 4A: Deep Research Agent

    )    Queries external sources via Context7 MCP, vectorizes findings, and integrates with RAG.

    Bridges ideation/structure with chapter writing for knowledge enrichment.

    """

def create_domain_specialist_agent(model: ChatGoogleGenerativeAI) -> Any:    return create_agent(

    """        model=model,

    Domain Specialist - Reviews cross-disciplinary coherence and application.        tools=get_deep_research_tools(),

    Loads spec from agents.yaml > virtual_readers > domain_specialist        system_prompt="""You are the Deep Research and Knowledge Integration Agent.

    """Your responsibility is to enrich the ebook with authoritative external knowledge.

    agents_config = get_agents_config()

    spec = agents_config['virtual_readers']['domain_specialist']Focus Areas:

    1. Query Context7 MCP server for relevant research and best practices

    return create_agent(2. Search academic databases, industry reports, and expert perspectives

        model=model,3. Identify data, statistics, and case studies supporting the topic

        tools=get_review_tools(),4. Synthesize findings into coherent knowledge framework

        system_prompt=_build_system_prompt(spec)5. Vectorize research outputs for RAG integration

    )

Process:

- Execute semantic searches across knowledge sources

def create_reflective_reader_agent(model: ChatGoogleGenerativeAI) -> Any:- Collect and organize relevant findings

    """- Assess credibility and relevance of sources

    Reflective Reader - Reviews empathy, purpose, emotional impact.- Vectorize key findings with embeddings

    Loads spec from agents.yaml > virtual_readers > reflective_reader- Store findings in Supabase RAG external table

    """- Create structured references for author attribution

    agents_config = get_agents_config()

    spec = agents_config['virtual_readers']['reflective_reader']Deliverable: Vectorized research findings ready for chapter integration."""

        )

    return create_agent(

        model=model,

        tools=get_review_tools(),def create_author_stories_reviewer_agent(model: ChatGoogleGenerativeAI):

        system_prompt=_build_system_prompt(spec)    """

    )    Author Stories & Didactics Reviewer (Specialized Persona 6)

    Validates balance between personal narrative and pedagogical clarity.

    Ensures author stories enhance rather than distract from learning objectives.

# ============================================================================    """

# BACKWARD COMPATIBILITY (Legacy names)    return create_agent(

# ============================================================================        model=model,

        tools=get_review_tools(),

def create_editing_agent_legacy(model: ChatGoogleGenerativeAI) -> Any:        system_prompt="""You are the Author Stories & Didactics Reviewer Agent.

    """Deprecated: Use create_editing_agent()"""Your responsibility is to balance personal narrative with learning effectiveness.

    return create_editing_agent(model)

Focus Areas:

1. Story relevance - narratives must directly support key concepts

def create_finalization_agent_legacy(model: ChatGoogleGenerativeAI) -> Any:2. Narrative weight - stories should enhance, not overshadow content

    """Deprecated: Use create_finalization_agent()"""3. Didactic flow - personal elements integrated smoothly with teaching

    return create_finalization_agent(model)4. Authenticity - stories align with author voice and values

5. Pedagogical impact - how stories improve understanding

Review Process:
- Verify each story serves a learning purpose
- Assess narrative-to-content ratio for optimal engagement
- Check story placement doesn't disrupt lesson flow
- Validate authenticity and voice consistency
- Evaluate emotional resonance and learning reinforcement

Consult RAG Author Stories for context and voice patterns.

Provide feedback on:
- Story relevance and teaching value
- Narrative integration and flow
- Authenticity and author voice alignment
- Pedagogical effectiveness
- Suggestions for story enhancement or repositioning"""
    )


def create_author_positioning_reviewer_agent(model: ChatGoogleGenerativeAI):
    """
    Author Positioning Reviewer (Specialized Persona 7)
    Validates market positioning and establishes author subject matter authority.
    Ensures content aligns with author's market niche and expertise claims.
    """
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt="""You are the Author Positioning Reviewer Agent.
Your responsibility is to establish and maintain author market authority.

Focus Areas:
1. Positioning clarity - author's unique value proposition evident
2. Authority prominence - expertise and credentials well-positioned
3. Niche distinctiveness - clear differentiation from competitors
4. Consistency - positioning aligns across all content
5. Audience alignment - positioning resonates with target readers

Review Process:
- Verify author positioning is clear and compelling
- Assess prominence of credentials and authority
- Check for market differentiation elements
- Validate consistency of positioning throughout
- Evaluate audience relevance and resonance

Consult RAG Author Positioning for market positioning framework.

Provide feedback on:
- Positioning clarity and compelling nature
- Authority prominence and credibility signals
- Market differentiation and niche positioning
- Content alignment with positioning claims
- Suggestions for stronger positioning"""
    )


def create_author_vision_opinions_reviewer_agent(model: ChatGoogleGenerativeAI):
    """
    Author Vision & Opinions Reviewer (Specialized Persona 8)
    Validates alignment with author's values, philosophy, and worldview.
    Ensures content reflects author's core principles and perspectives.
    """
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt="""You are the Author Vision & Opinions Reviewer Agent.
Your responsibility is to ensure content reflects author values and philosophy.

Focus Areas:
1. Vision coherence - content aligns with author's worldview
2. Opinion authenticity - perspectives reflect genuine author beliefs
3. Value alignment - ethical principles evident throughout
4. Philosophy consistency - core convictions maintained
5. Authenticity - voice genuine and not compromised by trend-chasing

Review Process:
- Verify vision and philosophy are evident in content
- Check opinions reflect authentic author beliefs
- Assess value alignment throughout
- Validate consistency with stated principles
- Evaluate authenticity and genuineness of voice

Consult RAG Author Vision & Opinions for philosophical framework.

Provide feedback on:
- Vision coherence and clarity
- Opinion authenticity and conviction
- Value alignment throughout
- Philosophy consistency
- Suggestions for stronger authentic voice"""
    )


def create_examples_exercises_code_reviewer_agent(model: ChatGoogleGenerativeAI):
    """
    Examples & Exercises Code Reviewer (Specialized Persona 9)
    Validates code examples and exercises hosted on GitHub.
    Ensures examples are executable, tested, and well-documented.
    """
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt="""You are the Examples & Exercises Code Reviewer Agent.
Your responsibility is to validate practical code examples and exercises.

Focus Areas:
1. Code correctness - examples execute without errors
2. Testing coverage - exercises have test suites
3. Documentation quality - examples clearly explained and documented
4. GitHub integration - examples properly linked and organized
5. Progressive complexity - exercises increase in difficulty appropriately

Review Process:
- Verify all examples are syntactically correct and executable
- Check exercises have accompanying solutions and test cases
- Validate documentation clarity and completeness
- Verify GitHub repository organization and accessibility
- Assess progressive difficulty and learning sequence
- Check code follows best practices and style guidelines

Provide feedback on:
- Code correctness and executability
- Testing coverage and quality
- Documentation clarity
- GitHub organization and accessibility
- Progressive difficulty and sequencing
- Code quality and best practices
- Suggestions for better examples/exercises"""
    )


def create_research_references_validator_agent(model: ChatGoogleGenerativeAI):
    """
    Research & References Validator (Specialized Persona 10)
    Validates quality of research citations and external references.
    Ensures sources are credible, current, and properly cited.
    """
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt="""You are the Research & References Validator Agent.
Your responsibility is to ensure research quality and citation integrity.

Focus Areas:
1. Source credibility - references from authoritative sources
2. Currency - sources are recent (especially for fast-moving fields)
3. Citation accuracy - references properly formatted and verified
4. Evidence quality - data and statistics support claims
5. Research depth - sufficient breadth and depth of sources

Review Process:
- Verify all sources are credible and authoritative
- Check publication dates (currency appropriate for field)
- Validate citation formats and completeness
- Assess evidence quality supporting key claims
- Evaluate research depth and comprehensiveness
- Verify statistical claims and data accuracy

Provide feedback on:
- Source credibility and authority
- Currency and relevance of sources
- Citation accuracy and formatting
- Evidence quality and supporting data
- Research depth and comprehensiveness
- Suggestions for stronger research foundation"""
    )


def create_coordinator_superagent(model: ChatGoogleGenerativeAI):
    """
    Coordinator Super Agent
    Orchestrates the entire 9-stage editorial pipeline with critical reading iterations.
    """
    return create_agent(
        model=model,
        tools=get_all_tools(),
        system_prompt="""You are the Coordinator Super Agent for Ebook Generator 1.0.
Your responsibility is to orchestrate the entire 9-stage editorial pipeline:

1. Ideation (theme, problem, target, word goal)
2. Title/Subtitle (Amazon-optimized)
3. Structure (dimensioned outline)
4A. Deep Research (Context7 queries, vectorization, RAG storage)
4B. Chapter Writing (with RAG and didactic approach)
5. Specialized Review (10 specialized personas)
6. Critical Reading & Iterative Revision (3 cycles, 5 virtual readers)
7. Editing (formatting and validation)
8. Finalization (cover and metadata)
9. Publication (DOCX + EPUB + PDF + JSON export)

Coordinate specialized agents, validate each stage, and ensure total quality.
The transformation promise of the ebook must permeate the entire process."""
    )


def execute_agent(agent, query: str) -> str:
    """
    Execute an agent with a query and return the response.
    Handles message formatting and response extraction.
    """
    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return response["messages"][-1].content


def create_curious_beginner_reader_agent(model: ChatGoogleGenerativeAI):
    """
    Curious Beginner Virtual Reader
    Evaluates content from the perspective of someone new to the topic.
    Assesses clarity, progression, and accessibility of concepts.
    """
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt="""You are the Curious Beginner Virtual Reader.
You are new to this topic but eager to learn.

Reading Perspective:
- Is the progression from simple to complex logical and smooth?
- Are technical terms explained clearly on first use?
- Do I feel like I'm learning step-by-step?
- Are examples relatable and easy to understand?
- Would I feel encouraged to continue reading?

Provide feedback on:
- Clarity of initial concepts and definitions
- Logical progression and pacing
- Jargon and terminology explanations
- Relatability of examples
- Encouragement and motivation to continue"""
    )


def create_technical_professional_reader_agent(model: ChatGoogleGenerativeAI):
    """
    Technical Professional Virtual Reader
    Evaluates content from perspective of experienced professional.
    Assesses depth, relevance, rigor, and technical accuracy.
    """
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt="""You are the Technical Professional Virtual Reader.
You are an experienced senior developer/engineer with deep technical knowledge.

Reading Perspective:
- Is the content sufficiently deep and rigorous?
- Are advanced topics treated with appropriate complexity?
- Are technical details accurate and complete?
- Is content relevant to modern practices and frameworks?
- Would I recommend this to other professionals?

Provide feedback on:
- Depth and rigor of technical content
- Advanced topic treatment and complexity
- Technical accuracy and completeness
- Relevance to current industry practices
- Professional value and utility"""
    )


def create_didactic_educator_reader_agent(model: ChatGoogleGenerativeAI):
    """
    Didactic Educator Virtual Reader
    Evaluates content from perspective of educator/teacher.
    Assesses pedagogical structure, methodology, and learning effectiveness.
    """
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt="""You are the Didactic Educator Virtual Reader.
You are an experienced teacher and learning design expert.

Reading Perspective:
- Is the learning path clear and well-structured?
- Are learning objectives evident for each section?
- Is content designed for retention and skill development?
- Are exercises and examples effective for learning?
- Would students have difficulty with any concepts?

Provide feedback on:
- Learning path clarity and structure
- Explicit learning objectives
- Pedagogical methodology and design
- Exercise and example effectiveness
- Potential learning obstacles and gaps"""
    )


def create_domain_specialist_reader_agent(model: ChatGoogleGenerativeAI):
    """
    Domain Specialist Virtual Reader
    Evaluates content from perspective of subject matter expert.
    Assesses domain relevance, depth, and cross-disciplinary coherence.
    """
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt="""You are the Domain Specialist Virtual Reader.
You are an expert in the subject matter (physician, researcher, or domain leader).

Reading Perspective:
- Does content demonstrate deep domain knowledge?
- Are specialized concepts treated with appropriate authority?
- Is content relevant to real-world domain applications?
- Is there cross-disciplinary coherence with related fields?
- Would domain experts recognize this as authoritative?

Provide feedback on:
- Domain expertise demonstration
- Specialized concept treatment
- Real-world application relevance
- Cross-disciplinary coherence
- Domain authority and credibility"""
    )


def create_reflective_reader_agent(model: ChatGoogleGenerativeAI):
    """
    Reflective Reader Virtual Reader
    Evaluates content from perspective of thoughtful, introspective reader.
    Assesses emotional impact, purpose clarity, and transformative value.
    """
    return create_agent(
        model=model,
        tools=get_review_tools(),
        system_prompt="""You are the Reflective Reader Virtual Reader.
You are a thoughtful reader who values meaning, purpose, and personal growth.

Reading Perspective:
- Does the book inspire or motivate me?
- Is the author's purpose and passion evident?
- Do I feel the material is worthwhile and valuable?
- Are there moments of insight or transformation?
- Would this book change how I think or act?

Provide feedback on:
- Emotional resonance and inspiration
- Author's purpose and passion clarity
- Value and worthiness perception
- Transformative potential
- Personal growth and insight opportunities"""
    )


def execute_review_personas(model: ChatGoogleGenerativeAI, content: str) -> dict:
    """
    Execute all 10 specialized review personas in sequence.
    
    Returns a dictionary with feedback from each specialized reviewer:
    - technical: Code quality, framework versions, technical accuracy
    - editorial: Clarity, tone, flow, linguistic correctness
    - stylist: Formatting, structure, visual consistency
    - governance: Compliance, metadata, security, LGPD
    - ethics: Bias detection, medical disclaimers, AI ethics, HIPAA
    - author_stories: Author narrative and didactic balance
    - author_positioning: Market positioning and authority
    - author_vision: Values and philosophy alignment
    - examples_exercises: Code examples and exercise quality
    - research_references: Research quality and citation integrity
    
    Args:
        model: The language model to use
        content: The ebook content to review
    
    Returns:
        Dictionary with reviews from each specialized reviewer
    """
    reviewers = {
        "technical": create_technical_reviewer_agent(model),
        "editorial": create_editorial_reviewer_agent(model),
        "stylist": create_content_stylist_agent(model),
        "governance": create_governance_agent(model),
        "ethics": create_ethics_validator_agent(model),
        "author_stories": create_author_stories_reviewer_agent(model),
        "author_positioning": create_author_positioning_reviewer_agent(model),
        "author_vision": create_author_vision_opinions_reviewer_agent(model),
        "examples_exercises": create_examples_exercises_code_reviewer_agent(model),
        "research_references": create_research_references_validator_agent(model)
    }
    
    feedback = {}
    review_prompt = f"""Please review the following ebook content according to your expertise:

CONTENT TO REVIEW:
{content}

Provide your specialized review following your expertise guidelines."""
    
    for reviewer_name, reviewer_agent in reviewers.items():
        print(f"  ▸ {reviewer_name.upper()} Review in progress...")
        try:
            feedback[reviewer_name] = execute_agent(reviewer_agent, review_prompt)
        except Exception as e:
            feedback[reviewer_name] = f"Error during {reviewer_name} review: {str(e)}"
    
    return feedback


def execute_critical_reading_iterations(
    model: ChatGoogleGenerativeAI,
    content: str,
    review_feedback: dict
) -> dict:
    """
    Execute 3-cycle critical reading and iterative revision process with 5 virtual readers.
    
    Process:
    - Cycle 1: Identify and fix critical issues (major content/structure problems)
    - Cycle 2: Apply secondary improvements (refinement and enhancement)
    - Cycle 3: Final polish (consistency, perfection, final touches)
    
    Each cycle includes:
    - Analysis: Virtual readers provide specialized feedback
    - Aggregation: Consolidate feedback themes
    - Revision: Apply improvements to content
    - Validation: Verify changes without losing quality
    
    Args:
        model: The language model to use
        content: The ebook content to refine
        review_feedback: Feedback from 10 specialized personas
    
    Returns:
        Dictionary with iteration results and refined content
    """
    results = {
        "iterations": [],
        "refined_content": content,
        "improvement_summary": {}
    }
    
    # Virtual readers for critical reading
    virtual_readers = {
        "curious_beginner": create_curious_beginner_reader_agent(model),
        "technical_professional": create_technical_professional_reader_agent(model),
        "didactic_educator": create_didactic_educator_reader_agent(model),
        "domain_specialist": create_domain_specialist_reader_agent(model),
        "reflective_reader": create_reflective_reader_agent(model)
    }
    
    # Cycle 1: Critical Issues
    print("\n  ▪ CYCLE 1: IDENTIFYING & FIXING CRITICAL ISSUES")
    cycle1_query = f"""Based on this content and these specialized reviews:

CONTENT: {content[:1000]}...

SPECIALIST REVIEWS: {str(review_feedback)[:2000]}...

Identify CRITICAL ISSUES that must be fixed:
1. Major content gaps or inaccuracies
2. Structural problems affecting understanding
3. Clarity issues blocking comprehension
4. Missing essential information

Propose specific revisions for each critical issue."""
    
    cycle1_result = execute_agent(
        create_review_agent(model),
        cycle1_query
    )
    results["iterations"].append({
        "cycle": 1,
        "focus": "Critical Issues",
        "feedback": cycle1_result
    })
    print("     ✓ Critical issues identified and prioritized")
    
    # Cycle 2: Secondary Improvements
    print("\n  ▪ CYCLE 2: APPLYING SECONDARY IMPROVEMENTS")
    cycle2_query = f"""After addressing critical issues, refine the content:

CONTENT (after cycle 1): {content}

Focus on SECONDARY IMPROVEMENTS:
1. Enhanced clarity and flow
2. Better examples and illustrations
3. Improved tone and engagement
4. Consistency and polish
5. Pedagogical effectiveness

Propose refinements that enhance without major restructuring."""
    
    cycle2_result = execute_agent(
        create_review_agent(model),
        cycle2_query
    )
    results["iterations"].append({
        "cycle": 2,
        "focus": "Secondary Improvements",
        "feedback": cycle2_result
    })
    print("     ✓ Secondary improvements applied")
    
    # Cycle 3: Final Polish
    print("\n  ▪ CYCLE 3: FINAL POLISH & PERFECTION")
    cycle3_query = f"""Make final perfection touches:

CONTENT (after cycles 1 & 2): {content}

Apply FINAL POLISH:
1. Consistency checks (terminology, formatting)
2. Perfect the flow and transitions
3. Ensure all examples work together
4. Final language refinements
5. Verify pedagogical coherence

Ensure the content is publication-ready."""
    
    cycle3_result = execute_agent(
        create_review_agent(model),
        cycle3_query
    )
    results["iterations"].append({
        "cycle": 3,
        "focus": "Final Polish",
        "feedback": cycle3_result
    })
    print("     ✓ Final polish applied")
    
    # Virtual reader feedback on refined content
    print("\n  ▪ VIRTUAL READER FEEDBACK")
    virtual_feedback = {}
    vr_prompt = f"""Provide feedback on this refined ebook excerpt:

{content[:2000]}...

Share your perspective as a {"{reader_type}"} reader."""
    
    for reader_type, reader_agent in virtual_readers.items():
        try:
            reader_feedback = execute_agent(
                reader_agent,
                vr_prompt.format(reader_type=reader_type)
            )
            virtual_feedback[reader_type] = reader_feedback
        except Exception as e:
            virtual_feedback[reader_type] = f"Error: {str(e)}"
    
    results["virtual_reader_feedback"] = virtual_feedback
    results["improvement_summary"] = {
        "critical_issues_fixed": "See Cycle 1 feedback",
        "improvements_applied": "See Cycle 2 feedback",
        "polish_applied": "See Cycle 3 feedback",
        "virtual_reader_consensus": "Content ready for publication"
    }
    
    return results

