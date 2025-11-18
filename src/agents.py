"""LangChain agent factory functions and execution helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_google_genai import ChatGoogleGenerativeAI

from .config import (
    get_agents_config,
    get_model,
    get_personas_config,
    get_research_model,
)
from .tools import (
    get_all_tools,
    get_editing_tools,
    get_finalization_tools,
    get_ideation_tools,
    get_publication_tools,
    get_research_tools,
    get_review_tools,
    get_structure_tools,
    get_title_tools,
    get_writing_tools,
)

load_dotenv()


# ============================================================================
# Callback + Helpers
# ============================================================================


class AgentExecutionLogger(BaseCallbackHandler):
    """Minimal callback handler used during agent execution in tests."""

    def on_llm_start(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401, ANN401
        """No-op hook required by BaseCallbackHandler."""

    def on_llm_end(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401, ANN401
        """No-op hook required by BaseCallbackHandler."""


@dataclass
class LazyAgentProxy:
    """Lazy loader for heavyweight LangChain agents."""

    factory: Callable[[], Any]
    _agent: Optional[Any] = None

    def _ensure(self) -> Any:
        if self._agent is None:
            self._agent = self.factory()
        return self._agent

    def __getattr__(self, item: str) -> Any:  # noqa: D401
        return getattr(self._ensure(), item)


def _render_prompt(agent_key: str, section: str = "main_pipeline_agents") -> str:
    config = get_agents_config()
    section_cfg = config.get(section, {})
    prompt = section_cfg.get(agent_key, {}).get("system_prompt")
    if prompt:
        return prompt
    # Fallback prompt for missing entries
    return f"You are {agent_key.replace('_', ' ')} for the Ebook Generator pipeline."


def _create_agent_from_config(
    agent_key: str,
    model: Any,
    tools_factory: Callable[[], Iterable[Any]],
    section: str = "main_pipeline_agents",
) -> Any:
    system_prompt = _render_prompt(agent_key, section)
    tools = list(tools_factory())
    return create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
    )


def _build_persona_prompt(persona_key: str) -> str:
    personas = get_personas_config().get("review_personas", {})
    persona = personas.get(persona_key, {})
    name = persona.get("name", persona_key.replace("_", " ").title())
    role = persona.get("role", "Specialist")
    expertise = persona.get("expertise_areas", [])
    criteria = persona.get("evaluation_criteria", [])
    expertise_lines = "\n".join(f"- {item}" for item in expertise) or "- Provide expert review"
    criteria_lines = "\n".join(f"- {item}" for item in criteria) or "- Share actionable feedback"
    return (
        f"You are {persona_key} - {name}, acting as a {role}.\n"
        f"Focus your review on the following expertise areas:\n{expertise_lines}\n\n"
        f"Evaluation criteria:\n{criteria_lines}\n\n"
        "Return concise Markdown feedback that the coordinator can merge into the master report."
    )


def _build_reader_prompt(reader_key: str) -> str:
    readers = get_personas_config().get("virtual_readers", {})
    reader = readers.get(reader_key, {})
    name = reader.get("name", reader_key.replace("_", " ").title())
    profile = reader.get("profile", "Reader persona")
    focus = reader.get("focus_areas", [])
    focus_lines = "\n".join(f"- {item}" for item in focus) or "- Overall clarity"
    validation = reader.get("validation_focus", [])
    validation_lines = "\n".join(f"- {item}" for item in validation) or "- Provide suggestions"
    return (
        f"You are {name}, {profile}.\n"
        f"Focus areas:\n{focus_lines}\n\n"
        f"Validation checklist:\n{validation_lines}\n\n"
        "Respond with empathetic, reader-friendly feedback highlighting confusing sections and actionable improvements."
    )


# ============================================================================
# Stage Agent Factories
# ============================================================================


def create_document_spec_agent(model: Any) -> Any:
    return _create_agent_from_config("document_spec_agent", model, get_research_tools)


def create_ideation_agent(model: Any) -> Any:
    return _create_agent_from_config("ideation_agent", model, get_ideation_tools)


def create_title_agent(model: Any) -> Any:
    return _create_agent_from_config("title_agent", model, get_title_tools)


def create_structure_agent(model: Any) -> Any:
    return _create_agent_from_config("structure_agent", model, get_structure_tools)


def create_deep_research_agent(model: Any) -> Any:
    return _create_agent_from_config("deep_research_agent", model, get_research_tools)


def create_chapter_agent(model: Any) -> Any:
    return _create_agent_from_config("chapter_writing_agent", model, get_writing_tools)


def create_review_coordinator_agent(model: Any) -> Any:
    return _create_agent_from_config("review_coordinator_agent", model, get_review_tools)


def create_critical_reading_coordinator_agent(model: Any) -> Any:
    return _create_agent_from_config("critical_reading_coordinator_agent", model, get_review_tools)


def create_editing_agent(model: Any) -> Any:
    return _create_agent_from_config("editing_agent", model, get_editing_tools)


def create_finalization_agent(model: Any) -> Any:
    return _create_agent_from_config("finalization_agent", model, get_finalization_tools)


def create_publication_agent(model: Any) -> Any:
    return _create_agent_from_config("publication_agent", model, get_publication_tools)


def create_technical_reviewer_agent(model: Any) -> Any:
    prompt = _build_persona_prompt("technical_reviewer")
    return create_agent(model=model, tools=list(get_review_tools()), system_prompt=prompt)


def create_curious_beginner_agent(model: Any) -> Any:
    prompt = _build_reader_prompt("curious_beginner")
    return create_agent(model=model, tools=list(get_review_tools()), system_prompt=prompt)


# ============================================================================
# Agent Execution Utilities
# ============================================================================


def _extract_text_from_response(response: Any) -> str:
    if isinstance(response, Mapping) and "messages" in response:
        messages = response["messages"] or []
        if messages:
            last = messages[-1]
            content = getattr(last, "content", None)
            if content:
                return content if isinstance(content, str) else str(content)
    return response if isinstance(response, str) else str(response)


def execute_agent(agent: Any, query: str) -> str:
    """Execute an agent safely and normalize the response."""

    messages = [{"role": "user", "content": query}]
    callbacks = [AgentExecutionLogger()]
    try:
        result = agent.invoke({"messages": messages}, config={"callbacks": callbacks})
        return _extract_text_from_response(result)
    except Exception as exc:  # noqa: BLE001
        return f"Error executing agent: {exc}"


def execute_review_personas(primary_agent: Any, content: str, personas: Dict[str, Any]) -> Dict[str, str]:
    """Execute a set of persona agents and collect their feedback."""

    feedback: Dict[str, str] = {}
    for persona_name, persona_agent in personas.items():
        prompt = f"[{persona_name}] Review and provide specialized feedback:\n\n{content}"
        feedback[persona_name] = execute_agent(persona_agent, prompt)
    return feedback


# ============================================================================
# Legacy Lazy Agents (used by the classic pipeline)
# ============================================================================

_WRITER_PROMPT = """Você é um Especialista em Escrita de Ebooks Técnicos sobre LangChain na Saúde Clínica.
Sua responsabilidade é gerar conteúdo de alta qualidade sobre implementação de agentes LangChain em contextos clínicos com foco em compliance, ética e responsabilidade.
"""

_RESEARCH_PROMPT = """Você é um Especialista em Research sobre Saúde Clínica e Agentes de IA.
Conduza pesquisas profundas, rigorosas e contextualizadas sobre implementação de IA em ambientes clínicos.
"""

_THEMATIC_RESEARCH_PROMPT = """Você é um Especialista em Pesquisa Temática Abrangente para Ebooks Técnicos.
Crie documentos de referência completos e reutilizáveis para múltiplos capítulos.
"""


def _build_writer_agent() -> Any:
    model = get_model()
    return create_agent(
        model=model,
        tools=list(get_all_tools()),
        system_prompt=_WRITER_PROMPT,
    )


def _build_research_agent() -> Any:
    model = get_research_model()
    return create_agent(
        model=model,
        tools=list(get_research_tools()),
        system_prompt=_RESEARCH_PROMPT,
    )


def _build_thematic_research_agent() -> Any:
    model = get_research_model()
    return create_agent(
        model=model,
        tools=list(get_research_tools()),
        system_prompt=_THEMATIC_RESEARCH_PROMPT,
    )


writer_agent = LazyAgentProxy(_build_writer_agent)
research_agent = LazyAgentProxy(_build_research_agent)
thematic_research_agent = LazyAgentProxy(_build_thematic_research_agent)


__all__ = [
    "create_document_spec_agent",
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
    "create_curious_beginner_agent",
    "execute_agent",
    "execute_review_personas",
    "writer_agent",
    "research_agent",
    "thematic_research_agent",
]
