# LLM-Powered Chatbot

A modern chatbot application built with Streamlit and Ollama, featuring a clean UI and local LLM inference.

## Features

- **Local LLM Inference**: Uses Ollama for privacy-focused, local AI processing
- **Multiple Models**: Support for various lightweight models (llama3.2, phi3, gemma2, qwen2.5)
- **Clean UI**: Modern dark theme with intuitive chat interface
- **Customizable**: Adjustable temperature and model selection
- **Chat History**: Maintains conversation context throughout the session
- **Fast & Private**: All processing happens locally on your machine

## Prerequisites

1. **Python 3.12+**: Required for this project
2. **uv**: Package manager (install from [astral.sh/uv](https://astral.sh/uv))
3. **Ollama**: Local LLM runtime (install from [ollama.ai](https://ollama.ai))

## Installation

### 1. Install Ollama

```bash
# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# macOS
brew install ollama

# Windows
# Download from https://ollama.ai/download
```

### 2. Pull a Lightweight Model

```bash
# Choose one or more models:
ollama pull llama3.2:3b      # 3B parameter model (recommended)
ollama pull phi3:mini         # Microsoft's compact model
ollama pull gemma2:2b         # Google's lightweight model
ollama pull qwen2.5:3b        # Alibaba's efficient model
ollama pull llama3.2:1b       # Smallest option
```

### 3. Start Ollama Server

```bash
ollama serve
```

Keep this running in a separate terminal.

### 4. Install Project Dependencies

```bash
# Clone the repository (if not already done)
cd llm-powererd-chatbot

# Install dependencies using uv
uv sync
```

## Usage

### Run the Chatbot

```bash
uv run streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`.

### Using the Interface

1. **Select a Model**: Use the sidebar dropdown to choose your preferred model
2. **Adjust Temperature**: Control response creativity (0.0 = focused, 1.0 = creative)
3. **Start Chatting**: Type your message in the chat input at the bottom
4. **Clear History**: Click the "Clear Chat History" button to start fresh

## Project Structure

```
llm-powererd-chatbot/
├── main.py              # Streamlit application
├── pyproject.toml       # Project configuration
├── uv.lock              # Dependency lock file
├── README.md            # This file
├── CLAUDE.md            # Development guidelines
└── .venv/               # Virtual environment (created by uv)
```

## Configuration

The chatbot connects to Ollama at `http://localhost:11434` by default. If you're running Ollama on a different port, modify the `base_url` in `main.py:124`.

## Troubleshooting

### "Failed to connect to Ollama"
- Ensure Ollama is running: `ollama serve`
- Check if the service is accessible: `curl http://localhost:11434`

### "Model not found"
- Pull the model first: `ollama pull <model-name>`
- Verify installed models: `ollama list`

### Slow responses
- Try a smaller model (llama3.2:1b or gemma2:2b)
- Ensure your system meets the model's requirements

## Development

### Add Dependencies

```bash
# Add a new package
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>
```

### Code Structure

The application is organized into modular functions:
- `setup_page()`: Configures Streamlit page and styling
- `setup_sidebar()`: Creates the settings sidebar
- `initialize_llm()`: Sets up the Ollama connection
- `display_chat_messages()`: Renders chat history
- `main()`: Orchestrates the application flow

## Technologies Used

- **Streamlit**: Web interface framework
- **LangChain**: LLM application framework
- **Ollama**: Local LLM runtime
- **uv**: Fast Python package manager

## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to submit issues and enhancement requests!
