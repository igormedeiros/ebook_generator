"""
Configuration module for Ebook Generator.

Handles:
1. Environment setup and model initialization
2. YAML configuration loading from specs/
3. Centralized logging with Rich formatting
4. Message localization (Portuguese strings)

Supports dual-model strategy:
- Gemini 2.5 Flash (writing, temp=0.7)
- Gemini 2.5 Pro (research, temp=0.3)
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

load_dotenv()

# Inicializar console Rich
console = Console()

# Caminho base do projeto
PROJECT_ROOT = Path(__file__).parent.parent
SPECS_DIR = PROJECT_ROOT / "specs"


# ============================================================================
# YAML Configuration Loading
# ============================================================================


def load_yaml_config(filename: str) -> Dict[str, Any]:
    """
    Carrega arquivo YAML de configuração.
    
    Args:
        filename: Nome do arquivo YAML (com ou sem extensão)
    
    Returns:
        dict: Conteúdo do arquivo YAML parseado
    
    Raises:
        FileNotFoundError: Se o arquivo não existir
        yaml.YAMLError: Se houver erro ao parsear YAML
    """
    if not filename.endswith(".yaml"):
        filename += ".yaml"
    
    config_path = SPECS_DIR / filename
    
    if not config_path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Erro ao parsear {filename}: {str(e)}")


def get_config(section: Optional[str] = None) -> Dict[str, Any]:
    """
    Carrega configuração centralizada (config.yaml).
    
    Args:
        section: Seção específica (ex: 'messages', 'labels', 'input_prompts')
    
    Returns:
        dict: Configuração completa ou seção específica
    """
    config = load_yaml_config("config.yaml")
    
    if section:
        return config.get(section, {})
    
    return config


def get_message(key: str, default: str = "") -> str:
    """
    Obtém mensagem localizada em português.
    
    Args:
        key: Chave da mensagem (ex: 'pipeline_start')
        default: Valor padrão se chave não existir
    
    Returns:
        str: Mensagem em português
    """
    messages = get_config("messages")
    return messages.get(key, default)


def get_pipeline_config() -> Dict[str, Any]:
    """
    Carrega configuração do pipeline (pipeline.yaml).
    
    Returns:
        dict: Configuração de todos os 9 estágios
    """
    return load_yaml_config("pipeline.yaml")


def get_models_config() -> Dict[str, Any]:
    """
    Carrega configuração de modelos IA (models.yaml).

    Returns:
        dict: Configuração Gemini, embeddings e APIs
    """
    return load_yaml_config("models.yaml")


def get_llm_profiles(profile: Optional[str] = None) -> Dict[str, Any]:
    """Return LLM profile configuration defined in config.yaml."""

    profiles = get_config("llm_profiles")
    if profile:
        return profiles.get(profile, {})
    return profiles


def _get_model_settings(model_key: str) -> Dict[str, Any]:
    """Return model configuration block for a given key."""

    models_cfg = get_models_config()
    models = models_cfg.get("models", {})
    return models.get(model_key, {})


def get_personas_config() -> Dict[str, Any]:
    """
    Carrega configuração de personas (personas.yaml).
    
    Returns:
        dict: Personas de revisão + leitores virtuais
    """
    return load_yaml_config("personas.yaml")


def get_tools_config() -> Dict[str, Any]:
    """
    Carrega configuração de tools (tools.yaml).
    
    Returns:
        dict: Especificação de todas as tools
    """
    return load_yaml_config("tools.yaml")


def get_agents_config() -> Dict[str, Any]:
    """
    Carrega configuração de agents (agents.yaml).
    
    Returns:
        dict: Especificação de todos os 25 agents (9 pipeline + 10 review + 5 readers)
    """
    return load_yaml_config("agents.yaml")


def get_agent_for_stage(stage_name: str) -> str:
    """
    Retorna o agent ID para um dado estágio do pipeline.
    
    Args:
        stage_name: Nome do estágio (e.g., 'stage_1_ideation')
        
    Returns:
        str: Agent ID (e.g., 'ideation_agent')
        
    Raises:
        ValueError: Se o estágio não existir
    """
    pipeline_config = get_pipeline_config()
    if stage_name not in pipeline_config.get("stages", {}):
        raise ValueError(f"Unknown stage: {stage_name}")
    
    return pipeline_config["stages"][stage_name].get("agent")


# ============================================================================
# Models (Dual-Model Strategy)
# ============================================================================


def get_model(
    timeout: Optional[int] = None,
    max_retries: Optional[int] = None,
) -> ChatGoogleGenerativeAI:
    """
    Initialize and return the writing model (Gemini 2.5 Flash).
    Uses Gemini 2.5 Flash for fast, creative text generation and iterative refinement.
    
    NOTE: Now with automatic fallback support. If this fails, system will try
    Gemini Pro, then Groq as fallback.
    
    Configuration:
    - Model: gemini-2.5-flash
    - Temperature: 0.7 (balanced creativity/consistency)
    - top_p: 0.95
    - top_k: 40
    
    Used for: Writing, chapter generation, title generation, creative tasks
    
    Args:
        timeout: Optional timeout override for API calls (seconds)
        max_retries: Optional retry override before triggering fallback

    Returns:
        ChatGoogleGenerativeAI: Configured Gemini 2.5 Flash model
    
    Raises:
        ValueError: If GOOGLE_API_KEY environment variable not set
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    settings = _get_model_settings("write_model")
    resolved_timeout = timeout if timeout is not None else settings.get("timeout")
    resolved_retries = max_retries if max_retries is not None else settings.get("max_retries")
    model_kwargs = {
        "model": settings.get("model_id", "gemini-2.5-flash"),
        "google_api_key": api_key,
        "temperature": settings.get("temperature", 0.7),
        "top_p": settings.get("top_p", 0.95),
        "top_k": settings.get("top_k", 40),
    }
    max_tokens = settings.get("max_tokens")
    if max_tokens:
        model_kwargs["max_output_tokens"] = max_tokens
    if resolved_timeout is not None:
        model_kwargs["timeout"] = resolved_timeout
    if resolved_retries is not None:
        model_kwargs["max_retries"] = resolved_retries

    return ChatGoogleGenerativeAI(**model_kwargs)


def get_research_model(
    timeout: Optional[int] = None,
    max_retries: Optional[int] = None,
) -> ChatGoogleGenerativeAI:
    """
    Initialize and return the research model (Gemini 2.5 Pro for analytical tasks).
    
    NOTE: Using Gemini 2.5 Pro for deeper analysis and RAG integration.
    
    Configuration:
    - Model: gemini-2.5-pro
    - Temperature: 0.3 (focused on precision and factuality)
    - top_p: 0.95
    - top_k: 40
    
    Used for: Research, RAG integration, fact-checking, semantic analysis
    
    Args:
        timeout: Optional timeout override for API calls (seconds)
        max_retries: Optional retry override before triggering fallback

    Returns:
        ChatGoogleGenerativeAI: Configured Gemini 2.5 Pro model
    
    Raises:
        ValueError: If GOOGLE_API_KEY environment variable not set
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    settings = _get_model_settings("research_model")
    resolved_timeout = timeout if timeout is not None else settings.get("timeout")
    resolved_retries = max_retries if max_retries is not None else settings.get("max_retries")
    model_kwargs = {
        "model": settings.get("model_id", "gemini-2.5-pro"),
        "google_api_key": api_key,
        "temperature": settings.get("temperature", 0.3),
        "top_p": settings.get("top_p", 0.95),
        "top_k": settings.get("top_k", 40),
    }
    max_tokens = settings.get("max_tokens")
    if max_tokens:
        model_kwargs["max_output_tokens"] = max_tokens
    if resolved_timeout is not None:
        model_kwargs["timeout"] = resolved_timeout
    if resolved_retries is not None:
        model_kwargs["max_retries"] = resolved_retries
    
    return ChatGoogleGenerativeAI(**model_kwargs)


def get_model_with_fallback():
    """
    Get writing model with automatic fallback to multiple providers.
    
    Sequence:
    1. Gemini 2.5 Flash (primary)
    2. Gemini 2.5 Pro (secondary)
    3. Groq LLaMA 3 70B (fallback)
    
    Returns:
        LLM model from the first available provider
    
    Raises:
        RuntimeError: If all providers are unavailable
    """
    from .llm_fallback import get_write_model_with_fallback
    return get_write_model_with_fallback()


def get_research_model_with_fallback():
    """
    Get research model with automatic fallback to multiple providers.
    
    Sequence:
    1. Gemini 2.5 Pro (primary - high accuracy)
    2. Gemini 2.5 Flash (secondary)
    3. Groq LLaMA 3 70B (fallback)
    
    Returns:
        LLM model from the first available provider
    
    Raises:
        RuntimeError: If all providers are unavailable
    """
    from .llm_fallback import get_research_model_with_fallback
    return get_research_model_with_fallback()


# ============================================================================
# Logging with Rich
# ============================================================================


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configura logging com Rich e arquivo opcional.
    
    Args:
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Caminho para arquivo de log (opcional)
    
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger("ebook_generator")
    logger.setLevel(level)
    
    # Limpar handlers existentes
    logger.handlers.clear()
    
    # Handler Rich para console
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        show_level=True,
        show_path=False,
        markup=True
    )
    rich_handler.setLevel(level)
    
    # Formato
    formatter = logging.Formatter(
        fmt="[%(name)s] %(message)s",
        datefmt="[%X]"
    )
    rich_handler.setFormatter(formatter)
    logger.addHandler(rich_handler)
    
    # Handler arquivo opcional
    if log_file:
        os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "ebook_generator") -> logging.Logger:
    """
    Obtém logger configurado para uso.
    
    Args:
        name: Nome do logger
    
    Returns:
        logging.Logger: Logger para uso
    """
    return logging.getLogger(name)


# ============================================================================
# Rich Output Formatting
# ============================================================================


def print_panel(
    title: str,
    content: str,
    style: str = "cyan"
) -> None:
    """
    Exibe conteúdo em painel formatado com Rich.
    
    Args:
        title: Título do painel
        content: Conteúdo do painel
        style: Estilo (cyan, green, yellow, red, etc)
    """
    panel = Panel(
        content,
        title=title,
        style=style,
        expand=False
    )
    console.print(panel)


def print_table(
    title: str,
    headers: list,
    rows: list,
    style: str = "cyan"
) -> None:
    """
    Exibe tabela formatada com Rich.
    
    Args:
        title: Título da tabela
        headers: Lista de cabeçalhos
        rows: Lista de linhas [['col1', 'col2'], ...]
        style: Estilo de linha
    """
    table = Table(title=title, style=style)
    
    for header in headers:
        table.add_column(header)
    
    for row in rows:
        table.add_row(*row)
    
    console.print(table)


def truncate_text(text: str, limit: int = 1000) -> str:
    """Return text truncated to limit with ellipsis when needed."""

    if len(text) <= limit:
        return text
    return f"{text[:limit].rstrip()}..."


def print_agent_status(
    agent_name: str,
    stage_label: str,
    model_name: str,
    objective: str,
) -> None:
    """Show which agent/model is running for a stage."""

    content = (
        f"[bold white]Agente:[/bold white] {agent_name}\n"
        f"[bold white]Estágio:[/bold white] {stage_label}\n"
        f"[bold white]Modelo:[/bold white] {model_name}\n"
        f"[bold white]Objetivo:[/bold white] {objective}"
    )
    panel = Panel(
        content,
        title="🤖 Execução do Agente",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)


def print_agent_thought(agent_name: str, thought: str) -> None:
    """Display a short 'thinking aloud' message for the running agent."""

    panel = Panel(
        f"[italic]{truncate_text(thought, 600)}[/italic]",
        title=f"🧠 Pensamento - {agent_name}",
        border_style="magenta",
        padding=(1, 2),
    )
    console.print(panel)


def print_agent_output(stage_label: str, output: Any, max_chars: int = 1200) -> None:
    """Render the agent output in a Rich panel with truncation."""

    if isinstance(output, str):
        rendered = output
    else:
        try:
            rendered = json.dumps(output, ensure_ascii=False, indent=2)
        except Exception:  # noqa: BLE001
            rendered = str(output)

    preview = truncate_text(rendered, max_chars)
    panel = Panel(
        preview or "(sem saída)",
        title=f"📤 Resultado - {stage_label}",
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)


def print_progress(
    total: int,
    description: str = "Processando"
) -> Progress:
    """
    Cria barra de progresso com Rich.
    
    Args:
        total: Total de itens
        description: Descrição
    
    Returns:
        Progress: Objeto de progresso para usar com `with`
    """
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    )


# ============================================================================
# TUI - Terminal User Interface (Colorida & Bonita)
# ============================================================================


def print_stage_header(stage_num: int, stage_title: str, stage_description: str) -> None:
    """
    Exibe cabeçalho colorido para estágio.
    
    Args:
        stage_num: Número do estágio (1-9)
        stage_title: Título (ex: "Ideação")
        stage_description: Descrição detalhada
    """
    colors = ["cyan", "blue", "magenta", "bright_cyan", "bright_blue", 
              "bright_magenta", "yellow", "bright_yellow", "green"]
    color = colors[stage_num - 1] if stage_num <= 9 else "white"
    
    panel = Panel(
        f"[bold {color}]Estágio {stage_num}[/bold {color}]\n\n[white]{stage_description}[/white]",
        title=f"[bold {color}]{stage_title}[/bold {color}]",
        border_style=color,
        padding=(1, 2),
    )
    console.print(panel)


def print_stage_complete(stage_num: int, elapsed_seconds: float = None) -> None:
    """
    Exibe conclusão do estágio com tempo decorrido.
    
    Args:
        stage_num: Número do estágio
        elapsed_seconds: Tempo em segundos (opcional)
    """
    time_str = f" em {elapsed_seconds:.1f}s" if elapsed_seconds else ""
    console.print(f"[green]✓ Estágio {stage_num} concluído com sucesso{time_str}[/green]")


def print_pipeline_start(topic: str, audience: str, word_count: int) -> None:
    """
    Exibe splash screen do início do pipeline.
    
    Args:
        topic: Tópico do ebook
        audience: Público-alvo
        word_count: Meta de palavras
    """
    panel = Panel(
        f"[bold cyan]Tópico:[/bold cyan] {topic}\n"
        f"[bold yellow]Público-alvo:[/bold yellow] {audience}\n"
        f"[bold magenta]Meta de Palavras:[/bold magenta] {word_count:,}",
        title="[bold bright_cyan]🚀 Ebook Generator 1.0[/bold bright_cyan]",
        subtitle="[bright_yellow]Automação Editorial com IA[/bright_yellow]",
        border_style="bright_cyan",
        padding=(1, 3),
    )
    console.print(panel)
    console.print()  # Espaço


def print_pipeline_complete(results: Dict[str, Any]) -> None:
    """
    Exibe tela final de sucesso com resumo.
    
    Args:
        results: Dicionário com resultados do pipeline
    """
    summary = results.get("summary", {})
    total_stages = summary.get("total_stages", 11)
    final_path = summary.get("final_ebook_path")
    final_line = ""
    if final_path:
        final_line = f"[green]Arquivo Final:[/green] {final_path}\n"
    panel = Panel(
        f"[bold green]✅ Pipeline Completado com Sucesso![/bold green]\n\n"
        f"[cyan]Tópico:[/cyan] {summary.get('topic', 'N/A')}\n"
        f"[yellow]Público-alvo:[/yellow] {summary.get('target_audience', 'N/A')}\n"
        f"[magenta]Estágios Concluídos:[/magenta] {summary.get('stages_completed', 0)}/{total_stages}\n"
        f"{final_line}\n"
        f"[bright_yellow]🎉 Seu ebook está pronto para publicação no KDP![/bright_yellow]",
        title="[bold green]CONCLUSÃO[/bold green]",
        border_style="green",
        padding=(2, 3),
    )
    console.print(panel)


def print_error_panel(error_title: str, error_message: str) -> None:
    """
    Exibe painel de erro com destaque.
    
    Args:
        error_title: Título do erro
        error_message: Mensagem detalhada
    """
    panel = Panel(
        f"[bright_red]{error_message}[/bright_red]",
        title=f"[bold bright_red]❌ {error_title}[/bold bright_red]",
        border_style="bright_red",
        padding=(1, 2),
    )
    console.print(panel)


# Configuração inicial de logging
_logger = setup_logging()


__all__ = [
    "console",
    "get_model",
    "get_research_model",
    "load_yaml_config",
    "get_config",
    "get_message",
    "get_pipeline_config",
    "get_models_config",
    "get_personas_config",
    "get_tools_config",
    "get_agents_config",
    "get_agent_for_stage",
    "setup_logging",
    "get_logger",
    "print_panel",
    "print_table",
    "truncate_text",
    "print_agent_status",
    "print_agent_thought",
    "print_agent_output",
    "print_progress",
    "print_stage_header",
    "print_stage_complete",
    "print_pipeline_start",
    "print_pipeline_complete",
    "print_error_panel",
]
