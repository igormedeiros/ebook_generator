"""
Sistema de observabilidade detalhada para agentes LangChain.
Permite visualizar pensamentos, chamadas de tools, operações RAG e cada etapa da execução.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich import box
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.agents import AgentAction, AgentFinish

console = Console()


class DetailedAgentObserver(BaseCallbackHandler):
    """
    Callback handler que captura e exibe cada detalhe da execução do agente:
    - Pensamentos do agente (chain of thought)
    - Chamadas de tools com argumentos
    - Resultados de tools
    - Operações RAG (retrieval)
    - Tokens usados
    - Tempo de execução
    """
    
    def __init__(self, agent_name: str = "Agent", show_tokens: bool = True, show_timing: bool = True):
        super().__init__()
        self.agent_name = agent_name
        self.show_tokens = show_tokens
        self.show_timing = show_timing
        self.step_count = 0
        self.tool_calls = []
        self.thoughts = []
        self.start_time = None
        self.total_tokens = 0
        
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Chamado quando o LLM começa a processar."""
        self.start_time = datetime.now()
        
        panel = Panel(
            f"[dim]Modelo: {serialized.get('name', 'Unknown')}[/dim]\n"
            f"[dim]Prompt length: {len(prompts[0]) if prompts else 0} chars[/dim]",
            title=f"[cyan]🧠 {self.agent_name} - Iniciando Pensamento[/cyan]",
            border_style="cyan",
            box=box.ROUNDED
        )
        console.print(panel)
    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Chamado quando o LLM termina de processar."""
        if self.start_time and self.show_timing:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            console.print(f"[dim]⏱️  Tempo de resposta: {elapsed:.2f}s[/dim]")
        
        # Extrai tokens se disponível
        if self.show_tokens and response.llm_output:
            token_usage = response.llm_output.get("token_usage", {})
            if token_usage:
                prompt_tokens = token_usage.get("prompt_tokens", 0)
                completion_tokens = token_usage.get("completion_tokens", 0)
                total = token_usage.get("total_tokens", 0)
                self.total_tokens += total
                
                console.print(
                    f"[dim]🎫 Tokens: {prompt_tokens} prompt + {completion_tokens} completion = {total} total[/dim]"
                )
    
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Chamado para cada novo token gerado (streaming)."""
        # Podemos usar isso para streaming no futuro
        pass
    
    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Chamado quando uma chain começa."""
        chain_name = serialized.get("name", "Chain")
        console.print(f"\n[bold magenta]⛓️  Iniciando Chain: {chain_name}[/bold magenta]")
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Chamado quando uma chain termina."""
        console.print(f"[green]✓ Chain concluída[/green]\n")
    
    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Chamado quando uma tool é invocada."""
        self.step_count += 1
        tool_name = serialized.get("name", "Unknown Tool")
        
        # Trunca input muito longo
        display_input = input_str if len(input_str) < 200 else f"{input_str[:200]}..."
        
        panel = Panel(
            f"[bold white]Tool:[/bold white] {tool_name}\n"
            f"[bold white]Input:[/bold white]\n{display_input}",
            title=f"[yellow]🔧 Step {self.step_count}: Chamando Tool[/yellow]",
            border_style="yellow",
            box=box.ROUNDED
        )
        console.print(panel)
        
        self.tool_calls.append({
            "step": self.step_count,
            "tool": tool_name,
            "input": input_str,
            "timestamp": datetime.now()
        })
    
    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Chamado quando uma tool retorna resultado."""
        # Trunca output muito longo
        display_output = output if len(output) < 300 else f"{output[:300]}..."
        
        panel = Panel(
            f"{display_output}",
            title=f"[green]✓ Tool Result[/green]",
            border_style="green",
            box=box.ROUNDED
        )
        console.print(panel)
        
        if self.tool_calls:
            self.tool_calls[-1]["output"] = output
            self.tool_calls[-1]["end_time"] = datetime.now()
    
    def on_tool_error(self, error: Exception, **kwargs: Any) -> None:
        """Chamado quando uma tool gera erro."""
        panel = Panel(
            f"[bold red]{str(error)}[/bold red]",
            title=f"[red]❌ Tool Error[/red]",
            border_style="red",
            box=box.ROUNDED
        )
        console.print(panel)
    
    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> None:
        """Chamado quando o agente decide uma ação."""
        panel = Panel(
            f"[bold cyan]Pensamento:[/bold cyan]\n{action.log}\n\n"
            f"[bold yellow]Ação:[/bold yellow] {action.tool}\n"
            f"[bold yellow]Input:[/bold yellow] {action.tool_input}",
            title=f"[magenta]💭 Decisão do Agente[/magenta]",
            border_style="magenta",
            box=box.ROUNDED
        )
        console.print(panel)
        
        self.thoughts.append({
            "thought": action.log,
            "action": action.tool,
            "input": action.tool_input,
            "timestamp": datetime.now()
        })
    
    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Chamado quando o agente termina."""
        panel = Panel(
            f"[bold green]{finish.log}[/bold green]\n\n"
            f"[dim]Return values: {finish.return_values}[/dim]",
            title=f"[green]✅ {self.agent_name} - Conclusão[/green]",
            border_style="green",
            box=box.ROUNDED
        )
        console.print(panel)
    
    def on_text(self, text: str, **kwargs: Any) -> None:
        """Chamado para texto intermediário."""
        if text.strip():
            console.print(f"[dim]{text}[/dim]")
    
    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo da execução."""
        return {
            "agent_name": self.agent_name,
            "total_steps": self.step_count,
            "total_tokens": self.total_tokens,
            "tool_calls": self.tool_calls,
            "thoughts": self.thoughts
        }
    
    def print_summary(self) -> None:
        """Exibe resumo formatado da execução."""
        table = Table(title=f"📊 Resumo de Execução - {self.agent_name}", box=box.ROUNDED)
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="white")
        
        table.add_row("Total de Steps", str(self.step_count))
        table.add_row("Tools Chamadas", str(len(self.tool_calls)))
        table.add_row("Pensamentos Registrados", str(len(self.thoughts)))
        if self.show_tokens:
            table.add_row("Total de Tokens", str(self.total_tokens))
        
        console.print(table)


class RAGObserver:
    """
    Observer específico para operações RAG (Retrieval-Augmented Generation).
    Mostra queries, documentos recuperados, scores de similaridade, etc.
    """
    
    @staticmethod
    def log_retrieval(query: str, documents: List[Any], scores: Optional[List[float]] = None):
        """Loga operação de retrieval."""
        panel = Panel(
            f"[bold cyan]Query:[/bold cyan]\n{query}\n\n"
            f"[bold yellow]Documentos Recuperados:[/bold yellow] {len(documents)}",
            title="[blue]🔍 RAG Retrieval[/blue]",
            border_style="blue",
            box=box.ROUNDED
        )
        console.print(panel)
        
        # Mostra preview dos documentos
        for i, doc in enumerate(documents[:3], 1):  # Mostra apenas os 3 primeiros
            content = str(doc)[:200] + "..." if len(str(doc)) > 200 else str(doc)
            score_str = f" (score: {scores[i-1]:.4f})" if scores and i-1 < len(scores) else ""
            console.print(f"  [dim]{i}.{score_str}[/dim] {content}")
        
        if len(documents) > 3:
            console.print(f"  [dim]... e mais {len(documents) - 3} documentos[/dim]")
    
    @staticmethod
    def log_vectorization(text: str, vector_dim: int):
        """Loga operação de vetorização."""
        console.print(
            f"[blue]🧮 Vetorizando texto ({len(text)} chars) → vetor de dimensão {vector_dim}[/blue]"
        )
    
    @staticmethod
    def log_storage(collection_name: str, num_docs: int):
        """Loga armazenamento em vector store."""
        console.print(
            f"[green]💾 Armazenado {num_docs} documentos em '{collection_name}'[/green]"
        )


def create_agent_with_observability(
    agent_factory,
    agent_name: str,
    show_tokens: bool = True,
    show_timing: bool = True
):
    """
    Wrapper para criar agente com observabilidade completa.
    
    Args:
        agent_factory: Função que cria o agente
        agent_name: Nome do agente para display
        show_tokens: Se deve mostrar contagem de tokens
        show_timing: Se deve mostrar tempo de execução
    
    Returns:
        Agente configurado com callbacks de observabilidade
    """
    observer = DetailedAgentObserver(
        agent_name=agent_name,
        show_tokens=show_tokens,
        show_timing=show_timing
    )
    
    # Cria o agente
    agent = agent_factory()
    
    # Retorna agente e observer para poder acessar summary depois
    return agent, observer


__all__ = [
    "DetailedAgentObserver",
    "RAGObserver",
    "create_agent_with_observability"
]
