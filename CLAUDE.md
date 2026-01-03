# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an LLM-powered chatbot application built with Streamlit, LangChain, and Ollama. It provides a modern chat interface for interacting with local LLM models.

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
```bash
# Run the Streamlit chatbot
uv run streamlit run main.py

# Note: Ollama must be running separately
# In another terminal: ollama serve
```

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

- `main.py`: Streamlit chatbot application with UI and LLM integration
- `pyproject.toml`: Project configuration and dependencies
- `README.md`: User documentation and setup instructions
- `.venv/`: Virtual environment (managed by uv)

## Key Dependencies

- **streamlit**: Web UI framework for the chatbot interface
- **langchain-ollama**: Ollama integration for LangChain
- **langchain-community**: Additional LangChain utilities
- **ollama**: Python client for Ollama

## Application Features

- Multiple lightweight model support (llama3.2, phi3, gemma2, qwen2.5)
- Adjustable temperature settings
- Chat history management
- Clean, modern dark theme UI
- Local inference for privacy