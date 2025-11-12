"""
Configuração centralizada e logging do Ebook Generator.

Este módulo carrega todas as configurações de specs/ e fornece
logging formatado com Rich para toda a aplicação.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Inicializar console Rich
console = Console()

# Caminho base do projeto
PROJECT_ROOT = Path(__file__).parent.parent
SPECS_DIR = PROJECT_ROOT / "specs"


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
    Carrega configuração centralizada.
    
    Args:
        section: Seção específica (ex: 'messages', 'labels')
    
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
    Carrega configuração do pipeline.
    
    Returns:
        dict: Configuração de todos os 9 estágios
    """
    return load_yaml_config("pipeline.yaml")


def get_models_config() -> Dict[str, Any]:
    """
    Carrega configuração de modelos IA.
    
    Returns:
        dict: Configuração Gemini, embeddings e APIs
    """
    return load_yaml_config("models.yaml")


def get_personas_config() -> Dict[str, Any]:
    """
    Carrega configuração de personas e leitores.
    
    Returns:
        dict: Personas de revisão + leitores virtuais
    """
    return load_yaml_config("personas.yaml")


def get_tools_config() -> Dict[str, Any]:
    """
    Carrega configuração de tools.
    
    Returns:
        dict: Especificação de todas as tools
    """
    return load_yaml_config("tools.yaml")


def load_example_config(example_name: str) -> Dict[str, Any]:
    """
    Carrega configuração de exemplo pré-pronta.
    
    Args:
        example_name: Nome do exemplo (sem .yaml)
    
    Returns:
        dict: Configuração de exemplo
    
    Raises:
        FileNotFoundError: Se exemplo não existir
    """
    example_path = SPECS_DIR / "examples" / f"{example_name}.yaml"
    
    if not example_path.exists():
        available = [f.stem for f in (SPECS_DIR / "examples").glob("*.yaml")]
        raise FileNotFoundError(
            f"Exemplo não encontrado: {example_name}\n"
            f"Exemplos disponíveis: {', '.join(available)}"
        )
    
    with open(example_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


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


# Configuração inicial de logging
_logger = setup_logging()


__all__ = [
    "console",
    "load_yaml_config",
    "get_config",
    "get_message",
    "get_pipeline_config",
    "get_models_config",
    "get_personas_config",
    "get_tools_config",
    "load_example_config",
    "setup_logging",
    "get_logger",
    "print_panel",
    "print_table",
    "print_progress",
]
