#!/usr/bin/env python3
"""Main entry point for the LLM-powered chatbot application.

This script provides a unified entry point that can launch either:
- CLI mode (default): Terminal-based chatbot with streaming responses
- UI/Web mode: Streamlit-based web interface
"""

import sys
import argparse


def run_cli_mode(model: str, temperature: float):
    """Run the CLI chatbot."""
    from cli_chatbot import CliChatbot

    chatbot = CliChatbot(model_name=model, temperature=temperature)
    chatbot.run()


def run_ui_mode():
    """Run the Streamlit web UI chatbot."""
    import subprocess

    # Launch Streamlit with the streamlit_chatbot.py file
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_chatbot.py"])


def main():
    """Main entry point with mode selection."""
    parser = argparse.ArgumentParser(
        description="LLM-powered chatbot with CLI and Web UI modes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run in CLI mode (default)
  python main.py
  python main.py --mode cli

  # Run with specific model and temperature in CLI mode
  python main.py --mode cli --model llama3.2:3b --temperature 0.8

  # Run in Web UI mode
  python main.py --mode ui
  python main.py --mode web

Notes:
  - Make sure Ollama is running: ollama serve
  - CLI mode provides a terminal-based interface with streaming responses
  - UI/Web mode launches a Streamlit web interface in your browser
        """,
    )

    parser.add_argument(
        "--mode",
        "-m",
        choices=["cli", "ui", "web"],
        default="cli",
        help="Interface mode: cli (terminal) or ui/web (Streamlit web interface). Default: cli",
    )

    parser.add_argument(
        "--model",
        default="gemma3:270m",
        help="Ollama model to use (CLI mode only). Default: gemma3:270m",
    )

    parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=0.7,
        help="Temperature setting 0.0-1.0 (CLI mode only). Default: 0.7",
    )

    args = parser.parse_args()

    # Validate temperature
    if not 0.0 <= args.temperature <= 1.0:
        print("Error: Temperature must be between 0.0 and 1.0")
        sys.exit(1)

    # Launch appropriate mode
    if args.mode == "cli":
        run_cli_mode(model=args.model, temperature=args.temperature)
    elif args.mode in ["ui", "web"]:
        if args.model != "gemma3:270m" or args.temperature != 0.7:
            print(
                "Note: --model and --temperature options are ignored in UI/Web mode. "
                "Use the UI controls to configure these settings."
            )
        run_ui_mode()


if __name__ == "__main__":
    main()
