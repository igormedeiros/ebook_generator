"""
Sistema de UI com Rich para TUI bonito no terminal.
Responsável por toda exibição de informações formatadas.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich import box

console = Console()

def print_header(title: str, subtitle: str = ""):
    """Exibe um header bonito com título e subtítulo."""
    if subtitle:
        content = f"[bold cyan]{title}[/bold cyan]\n[dim]{subtitle}[/dim]"
    else:
        content = f"[bold cyan]{title}[/bold cyan]"
    
    panel = Panel(
        Align.center(content),
        border_style="cyan",
        padding=(1, 2),
        box=box.ROUNDED
    )
    console.print(panel)

def print_section(title: str, content: str = ""):
    """Exibe uma seção com título."""
    if content:
        panel_content = f"[bold green]{title}[/bold green]\n{content}"
    else:
        panel_content = f"[bold green]{title}[/bold green]"
    
    panel = Panel(
        panel_content,
        border_style="green",
        padding=(1, 2),
        box=box.ROUNDED
    )
    console.print(panel)

def print_ebook_info(title: str, description: str, target_audience: str):
    """Exibe informações do ebook em formato tabular."""
    table = Table(title="📚 Informações do Ebook", box=box.ROUNDED, border_style="cyan")
    table.add_column("Campo", style="bold cyan")
    table.add_column("Valor", style="white")
    
    table.add_row("Título", title)
    table.add_row("Descrição", description)
    table.add_row("Público-alvo", target_audience)
    
    console.print(table)

def print_chapters_preview(chapters: list):
    """Exibe preview dos capítulos em formato tabular."""
    table = Table(title="📖 Capítulos a Gerar", box=box.ROUNDED, border_style="yellow")
    table.add_column("#", style="bold yellow", justify="center", width=3)
    table.add_column("Nome", style="cyan")
    table.add_column("Propósito", style="white", width=50)
    
    for i, chapter in enumerate(chapters, 1):
        table.add_row(
            str(i),
            chapter['name'],
            chapter['purpose'][:47] + "..." if len(chapter['purpose']) > 50 else chapter['purpose']
        )
    
    console.print(table)

def get_confirmation(prompt_text: str = "Deseja prosseguir com a geração?", default: bool = True, skip_prompt: bool = False, phase: str = None):
    """
    Obtém confirmação do usuário de forma bonita.
    
    Args:
        prompt_text: Texto do prompt
        default: Valor padrão se usuário apenas pressionar Enter
        skip_prompt: Se True, pula o prompt e retorna default
        phase: Nome da fase para verificar auto-approve (ex: 'deep_research', 'content_generation')
    
    Returns:
        bool: True se confirmado, False caso contrário
    """
    # Verifica se deve auto-aprovar baseado na configuração
    if phase:
        from .config import get_config
        phase_auto_approve = get_config("phase_auto_approve") or {}
        auto_approve_value = phase_auto_approve.get(phase, "no")
        
        # Se configurado como "yes", auto-aprova
        if auto_approve_value == "yes":
            console.print(f"[dim]⚡ Auto-aprovado (phase_auto_approve.{phase} = yes)[/dim]")
            return True
        # Se configurado como "no", sempre pergunta (comportamento padrão)
        # Qualquer outro valor também pergunta
    
    if skip_prompt:
        return default
    
    default_str = "(S/n)" if default else "(s/N)"
    
    panel = Panel(
        Align.center(f"[bold yellow]{prompt_text}[/bold yellow]\n[dim]{default_str}[/dim]"),
        border_style="yellow",
        padding=(1, 2),
        box=box.ROUNDED
    )
    console.print(panel)
    
    while True:
        response = console.input("[bold cyan]>>> [/bold cyan]").strip().lower()
        
        if not response:
            return default
            
        if response in ['s', 'sim', 'y', 'yes']:
            console.print("[green]✓ Confirmado[/green]")
            return True
        elif response in ['n', 'não', 'nao', 'no']:
            console.print("[yellow]✗ Negado[/yellow]")
            return False
        else:
            console.print("[yellow]⚠ Digite 's' para sim ou 'n' para não[/yellow]")

def print_phase_header(phase_num: int, phase_name: str, description: str = ""):
    """Exibe header de uma fase da geração."""
    phase_text = f"FASE {phase_num}: {phase_name}"
    if description:
        content = f"[bold white]{phase_text}[/bold white]\n[dim]{description}[/dim]"
    else:
        content = f"[bold white]{phase_text}[/bold white]"
    
    panel = Panel(
        Align.center(content),
        border_style="magenta",
        padding=(1, 2),
        box=box.ROUNDED
    )
    console.print(panel)

def create_progress_bar(description: str, total: int):
    """Cria uma barra de progresso."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("[cyan]{task.completed}/{task.total}"),
        TimeRemainingColumn(),
        console=console,
        transient=True
    )

def print_research_start(chapter_name: str, index: int, total: int):
    """Exibe início da pesquisa de um capítulo."""
    console.print(f"\n[cyan][{index}/{total}][/cyan] [bold]Pesquisando[/bold] {chapter_name}")

def print_research_saved(kb_path: str, size: int):
    """Exibe confirmação de salvamento em kb/."""
    console.print(f"  [green]✓ Salvo[/green] em: [dim]{kb_path}[/dim]")
    console.print(f"  [dim]Tamanho: {size:,} caracteres[/dim]")

def print_content_generation_start(chapter_name: str, index: int, total: int, words: int):
    """Exibe início da geração de conteúdo de um capítulo."""
    console.print(f"\n[magenta][{index}/{total}][/magenta] [bold]Gerando[/bold] {chapter_name} (~{words} palavras)")

def print_content_generated(size: int):
    """Exibe confirmação de geração de conteúdo."""
    console.print(f"  [green]✓ Gerado[/green] [dim]({size:,} caracteres)[/dim]")

def print_success_message(message: str):
    """Exibe mensagem de sucesso."""
    panel = Panel(
        Align.center(f"[bold green]✓ {message}[/bold green]"),
        border_style="green",
        padding=(1, 2),
        box=box.ROUNDED
    )
    console.print(panel)

def print_error_message(message: str):
    """Exibe mensagem de erro."""
    panel = Panel(
        Align.center(f"[bold red]✗ {message}[/bold red]"),
        border_style="red",
        padding=(1, 2),
        box=box.ROUNDED
    )
    console.print(panel)

def print_completion_summary(ebook_title: str, chapters_count: int, output_file: str):
    """Exibe resumo de conclusão."""
    table = Table(title="✨ Ebook Gerado com Sucesso!", box=box.ROUNDED, border_style="green")
    table.add_column("", style="green")
    table.add_column("")
    
    table.add_row("Título", f"[bold cyan]{ebook_title}[/bold cyan]")
    table.add_row("Capítulos", f"[bold cyan]{chapters_count}[/bold cyan]")
    table.add_row("Arquivo", f"[bold cyan]{output_file}[/bold cyan]")
    
    console.print(table)

def print_kb_summary(kb_files: list):
    """Exibe resumo dos arquivos em kb/."""
    table = Table(title="📚 Arquivos em KB/", box=box.ROUNDED, border_style="blue")
    table.add_column("Arquivo", style="cyan")
    table.add_column("Tamanho", style="white", justify="right")
    
    total_size = 0
    for file_info in kb_files:
        file_path, size = file_info
        table.add_row(file_path.name, f"{size:,} bytes")
        total_size += size
    
    console.print(table)
    console.print(f"\n[dim]Total: {total_size:,} bytes[/dim]")

def print_separator():
    """Exibe separador visual."""
    console.print()

def print_info(message: str):
    """Exibe mensagem informativa."""
    console.print(f"[cyan]ℹ {message}[/cyan]")

def print_warning(message: str):
    """Exibe mensagem de aviso."""
    console.print(f"[yellow]⚠ {message}[/yellow]")
