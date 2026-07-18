# ============================================
# AARVAN OS — NOVA Voice Mode Entry Point
# Brain: llama3 via Ollama
# Voice IN: Groq Whisper (NOVA's voice_in.py)
# Voice OUT: ElevenLabs (NOVA's voice_out.py)
# Agents: File, System, Memory, Browser,
#         App, Calculator, Weather, Notes
# ============================================

from rich.console import Console
from rich.panel import Panel
from brain.orchestrator import think
from brain.agent_router import AgentRouter
from nova_bridge import nova_listen, nova_speak
from config import OS_NAME, OS_VERSION
from datetime import datetime

console = Console()
router = AgentRouter()
session_history = []

def boot_screen():
    console.print(Panel(
        f"[bold cyan]{OS_NAME} v0.1-alpha[/bold cyan]\n"
        f"[dim]Agentic AI Operating System — NOVA VOICE MODE[/dim]\n"
        f"[dim]Built by Arivu — Aarvan Technology[/dim]\n\n"
        f"[green]Brain    : Online (llama3:latest)[/green]\n"
        f"[green]Voice IN : Groq Whisper (cloud — 95%+ accuracy)[/green]\n"
        f"[green]Voice OUT: ElevenLabs — Vikram (Indian accent)[/green]\n"
        f"[green]Agents   : File | System | Memory | Browser[/green]\n"
        f"[green]           App | Calculator | Weather | Notes[/green]\n\n"
        f"[yellow]Commands:[/yellow]\n"
        f"  [cyan]v[/cyan] → speak to AARVAN OS\n"
        f"  [cyan]anything[/cyan] → type normally\n"
        f"  [cyan]exit[/cyan] → shutdown",
        title="🚀 AARVAN OS — NOVA MODE",
        border_style="cyan"
    ))
    console.print()

def clean_for_speech(text: str) -> str:
    """Remove JSON and technical content before speaking"""
    # If response contains JSON, extract just the response field
    if '{"intent"' in text or '"agent"' in text:
        import re
        # Try to find response field
        match = re.search(r'"response"\s*:\s*"([^"]*)"', text)
        if match and match.group(1).strip():
            return match.group(1).strip()
        return "I didn't understand that da. Please try again."

    # Remove pipe-separated technical data for speech
    # Keep it natural
    text = text.replace(" | ", ", ")
    return text.strip()

def process_input(user_input: str, speak_response: bool = False):
    """Send input through brain + agents, display + optionally speak result"""

    if not user_input.strip():
        return

    console.print("[dim]🧠 Thinking...[/dim]")
    brain_output = think(user_input, session_history)
    result = router.route(brain_output)

    # Display in terminal
    console.print(Panel(
        result,
        title=f"[green]AARVAN OS[/green] [dim]({brain_output.get('agent', 'chat')} agent)[/dim]",
        border_style="green"
    ))

    # Speak response through NOVA's ElevenLabs voice
   # Speak response through NOVA's ElevenLabs voice
    if speak_response:
        agent = brain_output.get("agent", "chat")
        response_text = brain_output.get("response", "")

        if agent in ["chat", "weather", "calculator"]:
            nova_speak(clean_for_speech(result))
        elif agent in ["notes", "memory"]:
            speak_text = response_text if response_text else result
            nova_speak(clean_for_speech(speak_text))
        elif agent == "system":
            lines = result.strip().split("\n")
            real_data = [l for l in lines if "%" in l or "GB" in l or "Battery" in l]
            if real_data:
                nova_speak(clean_for_speech(real_data[0]))
            else:
                nova_speak(clean_for_speech(response_text))
        else:
            speak_text = response_text if response_text else "Done da!"
            nova_speak(clean_for_speech(speak_text))
    elif agent in ["notes", "memory"]:
            # Speak short confirmation
        nova_speak(response_text if response_text else result)
    elif agent in ["system"]:
            # For system — speak actual data not placeholder
            # Extract just the real stats line from result
        lines = result.strip().split("\n")
        real_data = [l for l in lines if "%" in l or "GB" in l or "Battery" in l]
        if real_data:
                nova_speak(real_data[0])
        else:
                nova_speak(response_text)
    else:
            # browser, app, file — speak short confirmation only
            nova_speak(response_text if response_text else "Done da!")

    # Save to session history
    session_history.append({
        "user": user_input,
        "brain": brain_output,
        "timestamp": datetime.now().isoformat()
    })

def main():
    boot_screen()

    # Greet with NOVA's voice
    greeting = f"AARVAN OS is online da. I'm listening."
    console.print(f"[dim]{greeting}[/dim]")
    nova_speak(greeting)

    console.print("[dim]Type anything or press 'v' to speak. Say 'exit' to shutdown.[/dim]\n")

    while True:
        try:
            user_input = console.input("[bold cyan]You → [/bold cyan]").strip()

            if not user_input:
                continue

            # EXIT
            if user_input.lower() in ['exit', 'quit', 'bye']:
                farewell = "AARVAN OS shutting down da. See you soon!"
                console.print(f"[yellow]{farewell}[/yellow]")
                nova_speak(farewell)
                break

            # VOICE MODE
            if user_input.lower() in ['v', 'voice']:
                console.print("[yellow]🎙️  Speak now da — 7 seconds![/yellow]")
                spoken = nova_listen()

                if not spoken:
                    console.print("[red]Didn't catch that da. Try again.[/red]")
                    continue

                # Show what was heard
                console.print(Panel(
                    f"[italic]{spoken}[/italic]",
                    title="🎙️  You said",
                    border_style="yellow"
                ))

                # Process + speak back
                process_input(spoken, speak_response=True)

            # TEXT MODE — still speaks back!
            else:
                process_input(user_input, speak_response=True)

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit da[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()