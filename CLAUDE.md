# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an LLM-powered chatbot application built with LangChain and Ollama. It provides both a terminal CLI interface and a Streamlit web interface for interacting with local LLM models.

## Development Environment

**Package Manager**: This project uses `uv` for dependency management (not pip or poetry).

**Python Version**: Requires Python >=3.12

## Common Commands

### Setup
```bash
# Install dependencies
uv sync

# Activate virtual environment (if not using uv run)
source .venv/bin/activate
```

### Running the Application

**Using Makefile (recommended):**
```bash
# Run the CLI chatbot (terminal-based with streaming)
make run-cli

# Run the Streamlit web chatbot
make run-web

# Start Ollama server (in separate terminal)
make ollama-serve

# See all available commands
make help
```

**Using main.py directly (unified entry point):**
```bash
# Run in CLI mode (default)
uv run python main.py
uv run python main.py --mode cli

# Run CLI with specific model and temperature
uv run python main.py --mode cli --model llama3.2:3b --temperature 0.7

# Run in Web UI mode
uv run python main.py --mode web
uv run python main.py --mode ui

# Note: Ollama must be running separately
# In another terminal: ollama serve
```

**Alternatively, use the individual scripts:**
```bash
# Run CLI chatbot directly
uv run python cli_chatbot.py --model llama3.2:3b --temperature 0.7

# Run Streamlit chatbot directly
uv run streamlit run streamlit_chatbot.py
```

### CLI Chatbot Commands
The CLI chatbot supports these interactive commands:
- `/help` - Show available commands
- `/clear` - Clear chat history
- `/models` - List available Ollama models
- `/switch` - Switch to a different model
- `/temp` - Change temperature setting
- `/quit` - Exit the chatbot
- `Ctrl+C` or `Ctrl+D` - Exit the chatbot

### Dependency Management
```bash
# Add a new dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>

# Update dependencies
uv sync
```

## Project Structure

- `main.py`: Unified entry point - dispatches to CLI or Web UI mode based on arguments (default: CLI)
- `cli_chatbot.py`: Terminal-based CLI chatbot with streaming responses (Claude Code-like interface)
- `streamlit_chatbot.py`: Streamlit web-based chatbot application with UI and LLM integration
- `Makefile`: Task automation with helpful commands
- `pyproject.toml`: Project configuration and dependencies
- `README.md`: User documentation and setup instructions
- `.venv/`: Virtual environment (managed by uv)
- `.chat_history`: CLI chatbot history file (auto-generated)

## Key Dependencies

- **rich**: Terminal UI framework with markdown rendering and live updates
- **prompt-toolkit**: Advanced terminal input with history and auto-completion
- **streamlit**: Web UI framework for the chatbot interface
- **langchain-ollama**: Ollama integration for LangChain
- **langchain-community**: Additional LangChain utilities
- **ollama**: Python client for Ollama

## Application Features

### Main Entry Point (main.py)
- Unified entry point for both CLI and Web UI modes
- Default mode: CLI (terminal-based)
- Mode selection via `--mode` argument (cli/ui/web)
- Supports all CLI chatbot arguments in CLI mode (model, temperature)
- Launches Streamlit web interface in UI/Web mode

### CLI Chatbot (cli_chatbot.py) - Recommended
- Terminal-based interface similar to Claude Code
- Real-time streaming responses with live markdown rendering
- Loading indicators and status updates
- Interactive commands (/help, /switch, /models, etc.)
- Persistent chat history across sessions
- Model switching and temperature adjustment on-the-fly
- Colored panels and rich formatting
- Local inference for privacy
- Command-line arguments for model and temperature

### Web Chatbot (streamlit_chatbot.py)
- Multiple lightweight model support (llama3.2, phi3, gemma2, qwen2.5)
- Adjustable temperature settings
- Chat history management
- Clean, modern dark theme UI
- Streamlit-based web interface

## Makefile Commands

The project includes a comprehensive Makefile for easy task automation:

**Quick Start:**
- `make help` - Display all available commands
- `make install` - Install all dependencies
- `make run-cli` - Run CLI chatbot
- `make run-web` - Run web chatbot
- `make test` - Run all tests
- `make lint` - Check code quality

**Ollama Management:**
- `make ollama-serve` - Start Ollama server
- `make ollama-pull-llama` - Pull llama3.2:3b model
- `make ollama-pull-all` - Pull all supported models
- `make ollama-list` - List downloaded models

**Development:**
- `make dev` - Complete dev setup (install + pull model)
- `make check` - Run all checks before committing
- `make clean` - Remove cache files

For the complete list of commands, run `make help`