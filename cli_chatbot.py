#!/usr/bin/env python3
"""Terminal-based CLI chatbot with streaming responses."""

import sys
import time
from typing import Generator, Optional

from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from ollama import Client
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel


class CliChatbot:
    """Terminal-based chatbot with streaming responses similar to Claude Code."""

    def __init__(self, model_name: str = "gemma3:270m", temperature: float = 0.7):
        self.console = Console()
        self.model_name = model_name
        self.temperature = temperature
        self.llm: Optional[ChatOllama] = None
        self.messages: list = []
        self.session = PromptSession(
            history=FileHistory(".chat_history"),
            style=Style.from_dict({"prompt": "#4a9eff bold"}),
        )

    def check_ollama_connection(self) -> bool:
        """Check if Ollama server is running."""
        try:
            client = Client(host="http://localhost:11434")
            client.list()
            return True
        except Exception as e:
            self.console.print(
                Panel(
                    f"[red]Failed to connect to Ollama:[/red]\n{e}\n\n"
                    "[yellow]Make sure Ollama is running:[/yellow]\n"
                    "[cyan]ollama serve[/cyan]",
                    title="Connection Error",
                    border_style="red",
                )
            )
            return False

    def get_available_models(self) -> list[str]:
        """Fetch available models from Ollama."""
        try:
            client = Client(host="http://localhost:11434")
            response = client.list()
            return [model.model for model in response.models]
        except Exception:
            return []

    def initialize_llm(self) -> bool:
        """Initialize the LLM instance."""
        try:
            self.llm = ChatOllama(
                model=self.model_name,
                temperature=self.temperature,
                base_url="http://localhost:11434",
            )
            return True
        except Exception as e:
            self.console.print(
                Panel(
                    f"[red]Failed to initialize model:[/red]\n{e}",
                    title="Initialization Error",
                    border_style="red",
                )
            )
            return False

    def stream_response(self, user_input: str) -> Generator[str, None, None]:
        """Stream the LLM response chunk by chunk."""
        if self.llm is None:
            yield "Error: LLM not initialized"
            return

        try:
            for chunk in self.llm.stream([HumanMessage(content=user_input)]):
                if hasattr(chunk, "content") and chunk.content:
                    yield chunk.content
        except Exception as e:
            yield f"\n[Error: {e}]"

    def display_welcome(self):
        """Display welcome message and setup info."""
        welcome_text = f"""
# LLM Terminal Chatbot

[cyan]Model:[/cyan] {self.model_name}
[cyan]Temperature:[/cyan] {self.temperature}

Type your message and press [bold]Enter[/bold] to chat.
Type [bold]/help[/bold] for available commands.
Type [bold]/quit[/bold] or press [bold]Ctrl+C[/bold] to exit.
        """

        self.console.print(
            Panel(
                welcome_text,
                title="Welcome",
                border_style="green",
                padding=(1, 2),
            )
        )

    def display_help(self):
        """Display help information."""
        help_text = """
[bold]Available Commands:[/bold]

[cyan]/help[/cyan]     - Show this help message
[cyan]/clear[/cyan]    - Clear chat history
[cyan]/models[/cyan]   - List available models
[cyan]/switch[/cyan]   - Switch to a different model
[cyan]/temp[/cyan]     - Change temperature setting
[cyan]/quit[/cyan]     - Exit the chatbot

[bold]Shortcuts:[/bold]

[cyan]Ctrl+C[/cyan]    - Exit the chatbot
[cyan]Ctrl+D[/cyan]    - Exit the chatbot
        """
        self.console.print(Panel(help_text, title="Help", border_style="cyan"))

    def display_models(self):
        """Display available models."""
        models = self.get_available_models()
        if models:
            models_text = "\n".join(f"  • {model}" for model in models)
            self.console.print(
                Panel(
                    f"[bold]Available Models:[/bold]\n\n{models_text}\n\n"
                    f"[cyan]Current model:[/cyan] {self.model_name}",
                    title="Models",
                    border_style="cyan",
                )
            )
        else:
            self.console.print(
                Panel(
                    "[yellow]No models found.[/yellow]\n\n"
                    "Install a model using:\n"
                    "[cyan]ollama pull llama3.2:3b[/cyan]",
                    title="Models",
                    border_style="yellow",
                )
            )

    def switch_model(self):
        """Switch to a different model."""
        models = self.get_available_models()
        if not models:
            self.console.print("[yellow]No models available. Install a model first.[/yellow]")
            return

        self.console.print("\n[bold]Available models:[/bold]")
        for i, model in enumerate(models, 1):
            self.console.print(f"  {i}. {model}")

        try:
            choice = self.session.prompt("\nEnter model number or name: ")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    self.model_name = models[idx]
                else:
                    self.console.print("[red]Invalid model number.[/red]")
                    return
            else:
                if choice in models:
                    self.model_name = choice
                else:
                    self.console.print("[red]Model not found.[/red]")
                    return

            if self.initialize_llm():
                self.console.print(f"[green]Switched to model:[/green] {self.model_name}")
        except (KeyboardInterrupt, EOFError):
            self.console.print("\n[yellow]Model switch cancelled.[/yellow]")

    def change_temperature(self):
        """Change the temperature setting."""
        try:
            temp_input = self.session.prompt(
                f"\nCurrent temperature: {self.temperature}\nEnter new temperature (0.0-1.0): "
            )
            temp = float(temp_input)
            if 0.0 <= temp <= 1.0:
                self.temperature = temp
                if self.initialize_llm():
                    self.console.print(f"[green]Temperature set to:[/green] {self.temperature}")
            else:
                self.console.print("[red]Temperature must be between 0.0 and 1.0.[/red]")
        except ValueError:
            self.console.print("[red]Invalid temperature value.[/red]")
        except (KeyboardInterrupt, EOFError):
            self.console.print("\n[yellow]Temperature change cancelled.[/yellow]")

    def handle_command(self, command: str) -> bool:
        """Handle special commands like /help, /clear, etc."""
        command = command.lower().strip()

        if command in ["/quit", "/exit", "/q"]:
            return False
        elif command == "/help":
            self.display_help()
        elif command == "/clear":
            self.messages = []
            self.console.clear()
            self.console.print("[green]Chat history cleared.[/green]")
        elif command == "/models":
            self.display_models()
        elif command == "/switch":
            self.switch_model()
        elif command == "/temp":
            self.change_temperature()
        else:
            self.console.print(
                f"[red]Unknown command:[/red] {command}\n"
                "Type [cyan]/help[/cyan] for available commands."
            )

        return True

    def run(self):
        """Run the main chat loop."""
        if not self.check_ollama_connection():
            return

        if not self.initialize_llm():
            return

        self.display_welcome()

        try:
            while True:
                try:
                    user_input: str = self.session.prompt("\n> ")
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Use /quit to exit.[/yellow]")
                    continue
                except EOFError:
                    break

                if not user_input.strip():
                    continue

                if user_input.startswith("/"):
                    if not self.handle_command(user_input):
                        break
                    continue

                user_panel = Panel(
                    user_input,
                    title="[bold blue]You[/bold blue]",
                    border_style="blue",
                    padding=(0, 1),
                )
                self.console.print(user_panel)

                self.messages.append(HumanMessage(content=user_input))

                with self.console.status("[bold green]Thinking...", spinner="dots") as status:
                    time.sleep(0.3)

                self.console.print("\n[bold green]Assistant:[/bold green]\n")

                response_text = ""
                with Live(console=self.console, refresh_per_second=20, transient=False) as live:
                    for chunk in self.stream_response(user_input):
                        response_text += chunk
                        live.update(Markdown(response_text))

                self.messages.append(AIMessage(content=response_text))
                self.console.print()

        except KeyboardInterrupt:
            self.console.print("\n\n[yellow]Goodbye![/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]Error:[/red] {e}")
        finally:
            self.console.print("\n[cyan]Chat session ended.[/cyan]")


def main():
    """Entry point for the CLI chatbot."""
    import argparse

    parser = argparse.ArgumentParser(description="Terminal-based LLM chatbot")
    parser.add_argument(
        "--model",
        "-m",
        default="gemma3:270m",
        help="Ollama model to use (default: gemma3:270m)",
    )
    parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=0.7,
        help="Temperature setting 0.0-1.0 (default: 0.7)",
    )

    args = parser.parse_args()

    if not 0.0 <= args.temperature <= 1.0:
        print("Error: Temperature must be between 0.0 and 1.0")
        sys.exit(1)

    chatbot = CliChatbot(model_name=args.model, temperature=args.temperature)
    chatbot.run()


if __name__ == "__main__":
    main()
