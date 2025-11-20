import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from supabase import create_client, Client
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

# Load env
load_dotenv()

# Setup Rich Console
console = Console()

# Setup Supabase
url = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not url or not key:
    # Fallback for testing if env vars are missing in this context
    console.print("[yellow]Warning: Supabase credentials not found in env. Using placeholders if not provided.[/yellow]")
    # In a real run this would fail, but for creating the file it's fine.

try:
    supabase: Client = create_client(url, key)
except Exception as e:
    console.print(f"[red]Supabase init failed: {e}[/red]")
    supabase = None

@tool
def search_author_context(query: str) -> str:
    """
    Searches for author's stories, positioning, and vision in the database.
    Useful for understanding the author's background and style.
    """
    if not supabase:
        return "Database connection unavailable."
        
    results = []
    
    try:
        # Search stories (content OR author_name)
        # Note: Supabase-py 'or' syntax is "column.ilike.val,column2.ilike.val"
        stories = supabase.table("rag_author_stories").select("*").or_(f"story.ilike.%{query}%,author_name.ilike.%{query}%").execute()
        for item in stories.data:
            results.append(f"[Story] {item['story']}")
            
        # Search positioning
        pos = supabase.table("rag_author_positioning").select("*").or_(f"positioning_statement.ilike.%{query}%,author_name.ilike.%{query}%").execute()
        for item in pos.data:
            results.append(f"[Positioning] {item['positioning_statement']}")
            
        # Search vision
        vis = supabase.table("rag_author_vision").select("*").or_(f"vision_or_opinion.ilike.%{query}%,author_name.ilike.%{query}%").execute()
        for item in vis.data:
            results.append(f"[Vision] {item['vision_or_opinion']}")
    except Exception as e:
        return f"Error searching author context: {e}"
        
    return "\n".join(results) if results else "No relevant author context found."

@tool
def search_technical_content(query: str) -> str:
    """
    Searches for technical content in the knowledge base.
    Useful for finding specific technical details about LangChain, RAG, etc.
    """
    if not supabase:
        return "Database connection unavailable."

    try:
        # Search external/kb content
        content = supabase.table("rag_external").select("topic, content").or_(f"content.ilike.%{query}%,topic.ilike.%{query}%").limit(3).execute()
        
        results = []
        for item in content.data:
            snippet = item['content'][:500] + "..." # Truncate for context window
            results.append(f"[Topic: {item['topic']}]\n{snippet}")
    except Exception as e:
        return f"Error searching technical content: {e}"
        
    return "\n".join(results) if results else "No relevant technical content found."

def main():
    # Setup Model
    model_name = "gemini-2.5-flash" 
    
    console.print(Panel(f"[bold green]Ebook Generator Agent[/bold green]\nModel: {model_name}", subtitle="PoC"))

    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0
        )
    except Exception as e:
        console.print(f"[red]Error initializing model: {e}[/red]")
        return
    
    tools = [search_author_context, search_technical_content]
    
    system_prompt = """You are a helpful assistant writing an ebook. 
Your responsibility is to answer questions using the available tools to look up context from the database.
YOU MUST USE THE TOOLS to find information. Do not answer from your own knowledge if you can find it in the database.

IMPORTANT: When using search tools, use SIMPLE KEYWORDS only. Do not use full sentences.
Example: Instead of "What is the author's vision on AI?", use "vision AI" or just "AI".
Example: Instead of "What is LangChain?", use "LangChain".

Focus Areas:
1. Author's personal stories and vision
2. Technical content about LangChain and RAG

Process:
1. Analyze the user query
2. Extract key terms
3. Use tools with those key terms
4. Synthesize the answer
"""

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    
    while True:
        try:
            query = Prompt.ask("\n[bold cyan]You[/bold cyan]")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        
        if query.lower() in ["exit", "quit", "sair"]:
            console.print("[yellow]Goodbye![/yellow]")
            break
            
        if not query.strip():
            continue

        with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
            try:
                response = agent.invoke({
                    "messages": [{"role": "user", "content": query}]
                })
                
                output = response["messages"][-1].content
                if isinstance(output, list):
                    # Handle case where content is a list of blocks (e.g. text + tool_use)
                    text_parts = []
                    for block in output:
                        if isinstance(block, dict) and block.get('type') == 'text':
                            text_parts.append(block.get('text', ''))
                        elif isinstance(block, str):
                            text_parts.append(block)
                    output = "\n".join(text_parts)
                
                console.print(Panel(Markdown(str(output)), title="[bold blue]Agent[/bold blue]", border_style="blue"))
                
                # Optional: Debug tool calls
                for msg in response["messages"]:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        console.print(f"[dim]Tool Calls: {msg.tool_calls}[/dim]")

            except Exception as e:
                import traceback
                console.print(f"[red]Agent execution failed: {e}[/red]")
                console.print(traceback.format_exc())

if __name__ == "__main__":
    main()
