from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from brain.orchestrator import think
from brain.agent_router import AgentRouter
from config import OS_NAME, OS_VERSION
import json, os
from datetime import datetime

console = Console()
router = AgentRouter()
session_history = []

def boot_screen():
    console.print(Panel(
        f"[bold cyan]{OS_NAME} v{OS_VERSION}[/bold cyan]\n"
        f"[dim]Agentic AI Operating System[/dim]\n"
        f"[dim]Built by Arivu — Aarvan Technology[/dim]\n\n"
        f"[green]Brain: Online (gemma3:4b)[/green]\n"
        f"[green]Agents: File | System | Memory[/green]",
        title="🚀 BOOTING",
        border_style="cyan"
    ))
    console.print()

def main():
    boot_screen()
    console.print("[dim]Type anything. Say 'exit' to quit.[/dim]\n")
    
    while True:
        try:
            user_input = console.input("[bold cyan]You → [/bold cyan]").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                console.print("[yellow]AARVAN OS shutting down... da 👋[/yellow]")
                break
            
            # Think
            console.print("[dim]🧠 Thinking...[/dim]")
            brain_output = think(user_input, session_history)
            
            # Route to agent
            result = router.route(brain_output)
            
            # Display response
            console.print(Panel(
                result,
                title=f"[green]AARVAN OS[/green] [dim]({brain_output.get('agent', 'chat')} agent)[/dim]",
                border_style="green"
            ))
            
            # Save to session history
            session_history.append({
                "user": user_input,
                "brain": brain_output,
                "timestamp": datetime.now().isoformat()
            })
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit da[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()