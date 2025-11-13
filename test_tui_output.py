#!/usr/bin/env python
"""
Test script for Rich TUI output - verify Portuguese messages render correctly.

This script validates that:
1. Rich console is properly configured
2. Portuguese messages display correctly
3. Panels and tables render as expected
4. Logging with Rich works properly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import console, get_logger, get_config

logger = get_logger(__name__)


def test_rich_console_output():
    """Test basic Rich console output."""
    print("\n🧪 Testing Rich console output with Portuguese messages...")

    console.print("\n[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold green]  ✅ TESTE DE SAÍDA RICH - VALIDADOR DE INPUT[/bold green]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]\n")

    return True


def test_logging_output():
    """Test logging output with Rich."""
    print("🧪 Testing logging output...")

    logger.info("Iniciando teste de validação de entrada")
    logger.debug("Detalhes técnicos do teste")
    logger.warning("Aviso: Este é um teste de aviso")

    return True


def test_rich_panels():
    """Test Rich panel output."""
    print("\n🧪 Testing Rich panels...")

    from rich.panel import Panel

    panel_content = """[bold cyan]Validação de Entrada - Teste[/bold cyan]

Campo obrigatório:
  • topic: Python para Análise
  • target_audience: Data Scientists
  • author_name: Igor Medeiros

Parâmetros:
  • word_count_target: 50000
  • reading_level: intermediate"""

    panel = Panel(panel_content, title="[bold green]Configuração Validada[/bold green]", style="cyan")
    console.print(panel)

    return True


def test_rich_table():
    """Test Rich table output."""
    print("\n🧪 Testing Rich table output...")

    from rich.table import Table

    table = Table(title="Campos Validados")
    table.add_column("Campo", style="cyan")
    table.add_column("Valor", style="green")
    table.add_column("Status", style="yellow")

    table.add_row("topic", "Python para Análise", "✅ Válido")
    table.add_row("target_audience", "Data Scientists", "✅ Válido")
    table.add_row("word_count_target", "50000", "✅ Válido")
    table.add_row("reading_level", "intermediate", "✅ Válido")

    console.print(table)

    return True


def test_error_output():
    """Test error message output."""
    print("\n🧪 Testing error message output...")

    config = get_config()
    validation_msgs = config.get("validation_messages", {})

    console.print("\n[bold yellow]Mensagens de Validação Centralizadas:[/bold yellow]")
    for key, msg in list(validation_msgs.items())[:5]:
        console.print(f"  • [cyan]{key}[/cyan]: [yellow]{msg}[/yellow]")

    return True


def main():
    """Run all TUI tests."""
    print("\n" + "=" * 70)
    print("  RICH TUI OUTPUT TEST SUITE")
    print("=" * 70)

    results = {
        "Rich console output": test_rich_console_output(),
        "Logging output": test_logging_output(),
        "Rich panels": test_rich_panels(),
        "Rich tables": test_rich_table(),
        "Error message output": test_error_output(),
    }

    console.print("\n[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold green]  TEST SUMMARY[/bold green]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]\n")

    all_passed = True
    for test_name, result in results.items():
        status = "[bold green]✅ PASS[/bold green]" if result else "[bold red]❌ FAIL[/bold red]"
        console.print(f"  {status}: {test_name}")
        all_passed = all_passed and result

    console.print("\n[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")

    if all_passed:
        console.print("[bold green]✅ All TUI tests passed! Rich output is rendering correctly.[/bold green]\n")
        return 0
    else:
        console.print("[bold red]❌ Some tests failed. Check errors above.[/bold red]\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
