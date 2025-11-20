"""
Helper functions for pipeline observability and optimization.
"""

import json
import ast
from typing import List, Optional, Any, Union, Dict
from .config import get_config, print_error_panel, print_panel
from .observability import DetailedAgentObserver
from .llm_fallback import get_llm_fallback


def create_observability_callbacks(agent_name: str) -> Optional[List]:
    """
    Create observability callbacks based on config.yaml settings.
    
    Args:
        agent_name: Name of the agent for display
    
    Returns:
        List of callbacks if observability is enabled, None otherwise
    """
    obs_config = get_config("observability") or {}
    
    if not obs_config.get("enabled", False):
        return None
    
    observer = DetailedAgentObserver(
        agent_name=agent_name,
        show_tokens=obs_config.get("show_tokens", True),
        show_timing=obs_config.get("show_timing", True)
    )
    
    return [observer]


def should_use_parallel_review() -> bool:
    """
    Check if parallel review execution is enabled in config.
    
    Returns:
        bool: True if parallel review is enabled
    """
    obs_config = get_config("observability") or {}
    return obs_config.get("parallel_review", True)



def _extract_from_message_obj(msg_obj: Any) -> str:
    """Recursively extract markdown text from a message-like object.
    Handles dicts with 'content' or 'text', lists of messages, and raw strings.
    """
    if isinstance(msg_obj, dict):
        # Prefer 'content' then 'text'
        if 'content' in msg_obj:
            return _extract_from_message_obj(msg_obj['content'])
        if 'text' in msg_obj:
            return _extract_from_message_obj(msg_obj['text'])
        # Fallback: stringify dict
        return str(msg_obj)
    if isinstance(msg_obj, list) and len(msg_obj) > 0:
        return _extract_from_message_obj(msg_obj[-1])
    # Base case: assume string
    return str(msg_obj)

def extract_markdown_content(response: Union[str, List, Any]) -> str:
    """Robustly extract pure markdown from various LLM response formats.
    Handles:
    - Direct string markdown
    - Dict with 'messages' list (LangChain style)
    - JSON strings (single or list) with keys like 'content', 'text', 'markdown'
    - Python literal dict strings (e.g. "{'messages':[{'content':'...'}]}")
    """
    # 1. Direct dict with messages
    if isinstance(response, dict) and 'messages' in response:
        return _extract_from_message_obj(response['messages'])

    # 2. If it's a list (Gemini style) return first element's text if present
    if isinstance(response, list) and len(response) > 0:
        first = response[0]
        if isinstance(first, dict) and 'text' in first:
            return str(first['text'])
        return str(first)

    # 3. If it's a string, try to parse JSON or Python literal
    if isinstance(response, str):
        stripped = response.strip()
        # Try JSON first
        if (stripped.startswith('{') and stripped.endswith('}')) or (stripped.startswith('[') and stripped.endswith(']')):
            try:
                parsed = json.loads(stripped)
                return extract_markdown_content(parsed)
            except Exception:
                # Not valid JSON, try Python literal
                try:
                    parsed = ast.literal_eval(stripped)
                    return extract_markdown_content(parsed)
                except Exception:
                    pass
        # Not JSON/py literal, return as is
        return stripped

    # 4. Fallback: stringify
    return str(response)


def invoke_agent(
    agent: Any,
    input_data: Dict[str, Any],
    agent_name: str,
    mode: str = "write",
    agent_factory: Optional[Any] = None
) -> Any:
    """
    Invokes an agent with robust fallback and observability.
    
    Args:
        agent: The LangChain agent instance
        input_data: Input dictionary (usually {"messages": [...]})
        agent_name: Name for logging
        mode: 'write' or 'research' (determines fallback sequence)
        agent_factory: Optional factory function to recreate agent with new model
        
    Returns:
        The agent response
    """
    fallback_manager = get_llm_fallback()
    
    # Setup callbacks
    callbacks = create_observability_callbacks(agent_name)
    if callbacks:
        input_data["callbacks"] = callbacks
        
    # Extract query from input_data for fallback manager
    query = ""
    if "messages" in input_data:
        msgs = input_data["messages"]
        if msgs and isinstance(msgs, list):
            query = msgs[-1].get("content", "") if isinstance(msgs[-1], dict) else getattr(msgs[-1], "content", str(msgs[-1]))
            
    try:
        # Try direct invocation first (primary model)
        return agent.invoke(input_data)
    except Exception as e:
        print_error_panel(f"Erro no agente {agent_name}", f"Falha no modelo primário: {e}. Iniciando fallback...")
        
        # Trigger fallback mechanism
        # Note: execute_with_fallback returns the extracted string, not the full response object
        # We need to wrap it back to match expected format if possible, or handle it downstream
        result_str = fallback_manager.execute_with_fallback(
            query=query,
            agent=agent,
            agent_factory=agent_factory,
            mode=mode
        )
        
        # Return in a format compatible with extract_markdown_content
        return {"messages": [{"content": result_str}]}


def get_test_mock_content(chapter_name: str) -> str:
    """Returns a large, structured Markdown content for testing."""
    return f"""# {chapter_name}

## Introdução
Este é um conteúdo gerado automaticamente em **modo de teste** para validar a formatação Markdown e a estrutura do ebook.

## Seção Técnica
Aqui demonstramos um bloco de código Python para validação:

```python
def hello_world():
    print("Hello from Test Mode!")
    return True
```

### Lista de Verificação
- [x] Formatação Markdown
- [x] Blocos de código
- [x] Listas e tabelas

| Recurso | Status |
|---------|--------|
| Mock | Ativo |
| Tamanho | Grande |

## Conclusão
O teste foi concluído com sucesso. Este texto deve ser longo o suficiente para validar a paginação e o layout.
"""


def verify_python_code(content: str) -> List[str]:
    """
    Verifies Python code blocks in the content.
    
    Args:
        content: Markdown content
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    lines = content.split('\n')
    in_code_block = False
    code_lines = []
    
    for line in lines:
        if line.strip().startswith('```python'):
            in_code_block = True
            code_lines = []
            continue
        
        if line.strip().startswith('```') and in_code_block:
            in_code_block = False
            code_block = '\n'.join(code_lines)
            try:
                ast.parse(code_block)
            except SyntaxError as e:
                errors.append(f"SyntaxError in code block: {e}")
            continue
            
        if in_code_block:
            code_lines.append(line)
            
    return errors


__all__ = [
    "create_observability_callbacks",
    "should_use_parallel_review",
    "extract_markdown_content",
    "invoke_agent",
    "get_test_mock_content",
    "verify_python_code"
]
