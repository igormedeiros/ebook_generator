"""
All 25 agents for Ebook Generator 1.0.

Agents are spec-driven from agents.yaml and include:
- 9 main pipeline agents
- 10 specialized review personas
- 5 virtual reader personas
"""

import time
from typing import Any, Callable, Dict, Optional
from langchain.agents import create_agent
from langchain_core.callbacks import BaseCallbackHandler
from langchain_google_genai import ChatGoogleGenerativeAI
from rich.console import Console
from rich.status import Status

from .config import get_agents_config, get_logger, get_personas_config
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

RETRYABLE_KEYWORDS = (
    "serviceunavailable",
    "failed to connect",
    "handshake read failed",
    "timeout",
    "deadline exceeded",
    "temporarily unavailable",
    "unavailable",
)

PERSONA_WRITE_MODEL_IDS = {
    "editorial_reviewer",
    "content_stylist",
    "author_stories_didactics",
}

VIRTUAL_READER_WRITE_MODEL_IDS = {
    "curious_beginner",
    "didactic_educator",
    "reflective_reader",
}

PIPELINE_AGENT_TOOLS: Dict[str, Callable[[], list]] = {
    "document_spec_agent": get_ideation_tools,
    "ideation_agent": get_ideation_tools,
    "title_agent": get_title_tools,
    "structure_agent": get_structure_tools,
    "deep_research_agent": get_deep_research_tools,
    "chapter_writing_agent": get_chapter_writing_tools,
    "review_coordinator_agent": get_review_tools,
    "critical_reading_coordinator_agent": get_review_tools,
    "editing_agent": get_editing_tools,
    "finalization_agent": get_finalization_tools,
    "publication_agent": get_publication_tools,
}


class StreamingCallbackHandler(BaseCallbackHandler):
    """Rich-powered callback handler that streams tokens in real time."""

    def __init__(self, console: Console, status_text: str):
        self.console = console
        self.status_text = status_text
        self._status: Optional[Status] = None
        self._buffer: list[str] = []
        self._stream_started = False
        self._enabled = getattr(console, "is_terminal", True)

    def __enter__(self) -> "StreamingCallbackHandler":
        self._status = self.console.status(self.status_text, spinner="dots")
        self._status.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._status:
            self._status.__exit__(exc_type, exc_val, exc_tb)
            self._status = None
        if self._stream_started:
            self.console.print()

    def _append_text(self, text: str) -> None:
        if not text:
            return
        self._buffer.append(text)
        if self._enabled:
            self.console.print(text, end="", style="white", highlight=False)
            self.console.file.flush()
            self._stream_started = True

    def on_llm_start(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        if self._status:
            self._status.update("[bold cyan]🟢 Streaming da IA...[/bold cyan]")

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self._append_text(token)

    def on_llm_end(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        if self._status:
            self._status.update("[bold green]✅ Resposta recebida[/bold green]")

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        if self._status:
            self._status.update("[bold red]❌ Erro no modelo[/bold red]")

    @property
    def streamed_text(self) -> str:
        """Return concatenated streamed tokens."""

        return "".join(self._buffer)

    @property
    def has_stream(self) -> bool:
        """Return True when at least one token was streamed."""

        return bool(self._buffer)


def _error_matches(error: Exception, keywords: tuple[str, ...]) -> bool:
    """Check whether error text contains any keyword."""

    text = f"{type(error)} {error}".lower()
    return any(keyword in text for keyword in keywords)


def _is_retryable_error(error: Exception) -> bool:
    """Return True when the exception is transient and worth retrying."""

    return _error_matches(error, RETRYABLE_KEYWORDS)


def _create_pipeline_agent(agent_key: str, model: ChatGoogleGenerativeAI) -> Any:
    """Create an agent using YAML specs and mapped tools."""

    agents_config = get_agents_config()
    spec = agents_config["main_pipeline_agents"][agent_key]
    tools_factory = PIPELINE_AGENT_TOOLS.get(agent_key)
    if not tools_factory:
        raise ValueError(f"No tools configured for agent {agent_key}")

    system_prompt = _build_system_prompt(spec)
    return create_agent(
        model=model,
        tools=tools_factory(),
        system_prompt=system_prompt,
    )


def _build_persona_prompt(persona_id: str, persona_spec: dict) -> str:
    """Create a system prompt for review personas."""

    name = persona_spec.get("name", persona_id)
    role = persona_spec.get("role", "Reviewer")
    expertise = persona_spec.get("expertise_areas", [])
    criteria = persona_spec.get("evaluation_criteria", [])
    rag_source = persona_spec.get("rag_source")

    expertise_text = "\n".join(f"- {item}" for item in expertise) or "- General expertise"
    criteria_text = "\n".join(f"- {item}" for item in criteria) or "- Evaluate overall quality"
    rag_text = (
        f"\nUse the '{rag_source}' RAG source whenever you need additional context."
        if rag_source
        else ""
    )

    return (
        f"You are {name}, acting as a {role}.\n"
        f"Focus Areas:\n{expertise_text}\n\n"
        f"Evaluation Criteria:\n{criteria_text}{rag_text}\n\n"
        "Return JSON with keys score (0-100), feedback (string), highlights (array), issues (array)."
    )


def _build_virtual_reader_prompt(reader_id: str, reader_spec: dict) -> str:
    """Create prompt for virtual reader personas."""

    name = reader_spec.get("name", reader_id)
    profile = reader_spec.get("profile", "Reader persona")
    focus_areas = reader_spec.get("focus_areas", [])
    validation_focus = reader_spec.get("validation_focus", [])

    focus_text = "\n".join(f"- {item}" for item in focus_areas) or "- General comprehension"
    validation_text = (
        "\n".join(f"- {item}" for item in validation_focus)
        if validation_focus
        else "- Flag confusing or weak sections"
    )

    return (
        f"You are {name}, {profile}.\n"
        f"Focus Areas:\n{focus_text}\n\nValidation Focus:\n{validation_text}\n\n"
        "Return JSON with keys score (0-100), positives (array), concerns (array), suggestions (array)."
    )


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


def execute_agent(agent: Any, query: str, max_retries: int = 2) -> str:
    """Execute an agent with basic retry logic."""
    console = Console()
    max_attempts = max(1, max_retries) + 1
    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"🤖 Pensamento do agente... (tentativa {attempt}/{max_attempts})")
            payload = {"messages": [{"role": "user", "content": query}]}
            handler = StreamingCallbackHandler(console, "[bold cyan]⏳ Processando com IA...[/bold cyan]")
            with handler:
                response = agent.invoke(payload, config={"callbacks": [handler]})

            if isinstance(response, dict):
                if "output" in response:
                    result = response["output"]
                    logger.info("✅ Agente concluiu processamento")
                    return result
                if "messages" in response:
                    messages = response.get("messages", [])
                    if messages:
                        result = messages[-1].content
                        logger.info("✅ Agente concluiu processamento")
                        return result

            logger.info("✅ Agente concluiu processamento")
            return str(response)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            error_msg = str(exc)
            if attempt < max_attempts and _is_retryable_error(exc):
                wait_seconds = min(5 * attempt, 20)
                logger.warning(
                    "🔁 Erro transitório (tentativa %s/%s): %s",
                    attempt,
                    max_attempts,
                    error_msg[:140],
                )
                logger.info(f"⏳ Aguardando {wait_seconds}s antes de tentar novamente...")
                time.sleep(wait_seconds)
                continue

            logger.warning(f"⚠️  Erro na execução do agente: {error_msg[:160]}")
            return f"Error executing agent: {error_msg}"

    if last_error:
        return f"Error executing agent: {last_error}"
    return "Error executing agent: unknown failure"


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


def create_document_spec_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 1: Documento de Especificação (DEL)."""

    return _create_pipeline_agent("document_spec_agent", model)


def create_ideation_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 2: Agente de Ideação."""

    return _create_pipeline_agent("ideation_agent", model)


def create_title_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 3: Estratégia de Título."""

    return _create_pipeline_agent("title_agent", model)


def create_structure_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 4: Arquitetura de Estrutura."""

    return _create_pipeline_agent("structure_agent", model)


def create_deep_research_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 5: Integrador de Pesquisa."""

    return _create_pipeline_agent("deep_research_agent", model)


def create_chapter_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 6: Agente de Escrita."""

    return _create_pipeline_agent("chapter_writing_agent", model)


def create_review_coordinator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 7: Coordenação de Revisão."""

    return _create_pipeline_agent("review_coordinator_agent", model)


def create_critical_reading_coordinator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 8: Coordenação de Leitura Crítica."""

    return _create_pipeline_agent("critical_reading_coordinator_agent", model)


def create_editing_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 9: Edição e validação."""

    return _create_pipeline_agent("editing_agent", model)


def create_finalization_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 10: Finalização editorial."""

    return _create_pipeline_agent("finalization_agent", model)


def create_publication_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Etapa 11: Publicação e exportação."""

    return _create_pipeline_agent("publication_agent", model)


def create_technical_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Persona de Revisão: Avaliador Técnico."""

    personas_config = get_personas_config()
    spec = personas_config['review_personas']['technical_reviewer']
    system_prompt = _build_persona_prompt("technical_reviewer", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_editorial_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Persona de Revisão: Revisora Editorial."""

    personas_config = get_personas_config()
    spec = personas_config['review_personas']['editorial_reviewer']
    system_prompt = _build_persona_prompt("editorial_reviewer", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_content_stylist_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Persona de Revisão: Estilista de Conteúdo."""

    personas_config = get_personas_config()
    spec = personas_config['review_personas']['content_stylist']
    system_prompt = _build_persona_prompt("content_stylist", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_governance_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Persona de Revisão: Governança e Conformidade."""

    personas_config = get_personas_config()
    spec = personas_config['review_personas']['governance_qa']
    system_prompt = _build_persona_prompt("governance_qa", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_ethics_validator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Persona de Revisão: Guardiã de Ética."""

    personas_config = get_personas_config()
    spec = personas_config['review_personas']['ethics_validator']
    system_prompt = _build_persona_prompt("ethics_validator", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_author_stories_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Persona de Revisão: Histórias do Autor."""

    personas_config = get_personas_config()
    spec = personas_config['review_personas']['author_stories_didactics']
    system_prompt = _build_persona_prompt("author_stories_didactics", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_author_positioning_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Persona de Revisão: Posicionamento do Autor."""

    personas_config = get_personas_config()
    spec = personas_config['review_personas']['author_positioning']
    system_prompt = _build_persona_prompt("author_positioning", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_author_vision_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Persona de Revisão: Visão do Autor."""

    personas_config = get_personas_config()
    spec = personas_config['review_personas']['author_vision_opinions']
    system_prompt = _build_persona_prompt("author_vision_opinions", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_code_examples_reviewer_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Persona de Revisão: Validador de Código."""

    personas_config = get_personas_config()
    spec = personas_config['review_personas']['code_exercises_reviewer']
    system_prompt = _build_persona_prompt("code_exercises_reviewer", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_research_validator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Persona de Revisão: Validação de Pesquisa."""

    personas_config = get_personas_config()
    spec = personas_config['review_personas']['research_references_validator']
    system_prompt = _build_persona_prompt("research_references_validator", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_curious_beginner_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Leitor Virtual: Iniciante Curioso."""

    personas_config = get_personas_config()
    spec = personas_config['virtual_readers']['curious_beginner']
    system_prompt = _build_virtual_reader_prompt("curious_beginner", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_technical_professional_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Leitor Virtual: Profissional Técnico."""

    personas_config = get_personas_config()
    spec = personas_config['virtual_readers']['technical_professional']
    system_prompt = _build_virtual_reader_prompt("technical_professional", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_didactic_educator_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Leitor Virtual: Educador Didático."""

    personas_config = get_personas_config()
    spec = personas_config['virtual_readers']['didactic_educator']
    system_prompt = _build_virtual_reader_prompt("didactic_educator", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_domain_specialist_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Leitor Virtual: Especialista em Domínio."""

    personas_config = get_personas_config()
    spec = personas_config['virtual_readers']['domain_specialist']
    system_prompt = _build_virtual_reader_prompt("domain_specialist", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


def create_reflective_reader_agent(model: ChatGoogleGenerativeAI) -> Any:
    """Leitor Virtual: Leitora Reflexiva."""

    personas_config = get_personas_config()
    spec = personas_config['virtual_readers']['reflective_reader']
    system_prompt = _build_virtual_reader_prompt("reflective_reader", spec)

    return create_agent(model=model, tools=get_review_tools(), system_prompt=system_prompt)


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
