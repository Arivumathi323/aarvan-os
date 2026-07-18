from rich.console import Console
from rich.panel import Panel
from brain.orchestrator import think
from brain.agent_router import AgentRouter
from voice_input import listen, load_whisper
from config import OS_NAME, OS_VERSION
from datetime import datetime
import json

console = Console()
router = AgentRouter()
session_history = []

def boot_screen():
    console.print(Panel(
        f"[bold cyan]{OS_NAME} v{OS_VERSION}[/bold cyan]\n"
        f"[dim]Agentic AI Operating System — VOICE MODE[/dim]\n"
        f"[dim]Built by Arivu — Aarvan Technology[/dim]\n\n"
        f"[green]Brain: Online (llama3:latest)[/green]\n"
        f"[green]Voice: Whisper base (local)[/green]\n"
        f"[green]Agents: File | System | Memory[/green]\n\n"
        f"[yellow]Commands:[/yellow]\n"
        f"  [cyan]v[/cyan] or [cyan]voice[/cyan] → speak to OS\n"
        f"  [cyan]t[/cyan] or just type → text mode\n"
        f"  [cyan]exit[/cyan] → shutdown",
        title="🚀 BOOTING — VOICE MODE",
        border_style="cyan"
    ))
    console.print()

def process_input(user_input: str):
    """Send input through brain and agents, display result"""
    console.print("[dim]🧠 Thinking...[/dim]")
    brain_output = think(user_input, session_history)
    result = router.route(brain_output)

    console.print(Panel(
        result,
        title=f"[green]AARVAN OS[/green] [dim]({brain_output.get('agent', 'chat')} agent)[/dim]",
        border_style="green"
    ))

    session_history.append({
        "user": user_input,
        "brain": brain_output,
        "timestamp": datetime.now().isoformat()
    })

def main():
    boot_screen()

    # Pre-load Whisper so first voice command is fast
    load_whisper()

    console.print("[dim]Ready! Type or press 'v' to use voice.[/dim]\n")

    while True:
        try:
            user_input = console.input("[bold cyan]You → [/bold cyan]").strip()

            if not user_input:
                continue

            # EXIT
            if user_input.lower() in ['exit', 'quit', 'bye']:
                console.print("[yellow]AARVAN OS shutting down... da 👋[/yellow]")
                break

            # VOICE MODE — user types 'v' or 'voice'
            if user_input.lower() in ['v', 'voice']:
                spoken = listen(duration=5)

                if not spoken:
                    console.print("[red]Didn't catch that da. Try again.[/red]")
                    continue

                # Show what was heard
                console.print(Panel(
                    f"[italic]{spoken}[/italic]",
                    title="🎙️  You said",
                    border_style="yellow"
                ))

                process_input(spoken)

            # TEXT MODE — normal typing
            else:
                process_input(user_input)

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit da[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()