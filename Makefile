.PHONY: help install sync run test test-verbose test-coverage clean lint format check-format dev-install update ollama-serve ollama-pull-all

# Default target - show help
.DEFAULT_GOAL := help

# Colors for terminal output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)  LLM-Powered Chatbot - Makefile Commands$(NC)"
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"

##@ Setup & Installation

install: ## Install all dependencies (first time setup)
	@echo "$(GREEN)Installing dependencies with uv...$(NC)"
	uv sync
	@echo "$(GREEN)✓ Installation complete!$(NC)"

sync: ## Sync dependencies with pyproject.toml
	@echo "$(GREEN)Syncing dependencies...$(NC)"
	uv sync
	@echo "$(GREEN)✓ Dependencies synced!$(NC)"

dev-install: ## Install development dependencies
	@echo "$(GREEN)Installing dev dependencies...$(NC)"
	uv add --dev pytest pytest-mock pytest-cov ruff
	@echo "$(GREEN)✓ Dev dependencies installed!$(NC)"

update: ## Update all dependencies to latest versions
	@echo "$(GREEN)Updating dependencies...$(NC)"
	uv sync --upgrade
	@echo "$(GREEN)✓ Dependencies updated!$(NC)"

##@ Running the Application

run-cli: ## Run the terminal CLI chatbot (recommended)
	@echo "$(GREEN)Starting CLI chatbot...$(NC)"
	@echo "$(YELLOW)Make sure Ollama is running in another terminal!$(NC)"
	uv run python main.py --mode cli

run-web: ## Run the Streamlit web chatbot
	@echo "$(GREEN)Starting Streamlit chatbot...$(NC)"
	@echo "$(YELLOW)Make sure Ollama is running in another terminal!$(NC)"
	uv run python main.py --mode web

run: ## Run the chatbot (default: CLI mode)
	@echo "$(GREEN)Starting chatbot in CLI mode...$(NC)"
	@echo "$(YELLOW)Make sure Ollama is running in another terminal!$(NC)"
	uv run python main.py

##@ Ollama Management

ollama-serve: ## Start Ollama server
	@echo "$(GREEN)Starting Ollama server...$(NC)"
	ollama serve

ollama-pull-all: ## Pull all supported models
	@echo "$(GREEN)Pulling all supported models...$(NC)"
	@echo "$(YELLOW)This may take a while...$(NC)"
	ollama pull llama3.2:3b
	ollama pull phi3:mini
	ollama pull qwen2.5:3b
	ollama pull gemma2:2b
	ollama pull llama3.2:1b
	@echo "$(GREEN)✓ All models downloaded!$(NC)"

ollama-pull-llama: ## Pull llama3.2:3b model
	@echo "$(GREEN)Pulling llama3.2:3b...$(NC)"
	ollama pull llama3.2:3b

ollama-pull-phi: ## Pull phi3:mini model
	@echo "$(GREEN)Pulling phi3:mini...$(NC)"
	ollama pull phi3:mini

ollama-pull-qwen: ## Pull qwen2.5:3b model
	@echo "$(GREEN)Pulling qwen2.5:3b...$(NC)"
	ollama pull qwen2.5:3b

ollama-pull-gemma: ## Pull gemma2:2b model
	@echo "$(GREEN)Pulling gemma2:2b...$(NC)"
	ollama pull gemma2:2b

ollama-list: ## List all downloaded Ollama models
	@echo "$(GREEN)Downloaded models:$(NC)"
	ollama list

##@ Testing

test: ## Run all tests
	@echo "$(GREEN)Running tests...$(NC)"
	uv run pytest

test-verbose: ## Run tests with verbose output
	@echo "$(GREEN)Running tests (verbose)...$(NC)"
	uv run pytest -v

test-coverage: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	uv run pytest --cov=main --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/index.html$(NC)"

test-watch: ## Run tests in watch mode (requires pytest-watch)
	@echo "$(GREEN)Running tests in watch mode...$(NC)"
	uv run ptw

test-specific: ## Run specific test (usage: make test-specific TEST=test_name)
	@echo "$(GREEN)Running specific test: $(TEST)$(NC)"
	uv run pytest -v -k "$(TEST)"

##@ Code Quality

lint: ## Run ruff linter
	@echo "$(GREEN)Linting code with ruff...$(NC)"
	uv run ruff check .

lint-fix: ## Run ruff linter and fix auto-fixable issues
	@echo "$(GREEN)Linting and fixing code...$(NC)"
	uv run ruff check --fix .

format: ## Format code with ruff formatter
	@echo "$(GREEN)Formatting code with ruff...$(NC)"
	uv run ruff format .

check-format: ## Check code formatting without making changes
	@echo "$(GREEN)Checking code format...$(NC)"
	uv run ruff format --check .

quality: lint-fix format test ## Run all quality checks (lint, format, test)
	@echo "$(GREEN)✓ All quality checks passed!$(NC)"

##@ Cleanup

clean: ## Remove cache files and build artifacts
	@echo "$(RED)Cleaning up cache files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

clean-all: clean ## Remove cache files, build artifacts, and virtual environment
	@echo "$(RED)Removing virtual environment...$(NC)"
	rm -rf .venv
	@echo "$(GREEN)✓ Full cleanup complete!$(NC)"

##@ Development Workflow

dev: install ollama-pull-llama ## Complete development setup (install + pull default model)
	@echo "$(GREEN)✓ Development environment ready!$(NC)"
	@echo "$(YELLOW)Run 'make ollama-serve' in one terminal$(NC)"
	@echo "$(YELLOW)Run 'make run' in another terminal$(NC)"

check: lint check-format test ## Run all checks before committing
	@echo "$(GREEN)✓ All checks passed! Ready to commit.$(NC)"

##@ Docker (if using Docker in future)

docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t llm-chatbot .

docker-run: ## Run Docker container
	@echo "$(GREEN)Running Docker container...$(NC)"
	docker run -p 8501:8501 llm-chatbot

##@ Information

info: ## Show project information
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)  Project Information$(NC)"
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo ""
	@echo "$(YELLOW)Python Version:$(NC)"
	@python3 --version || echo "Python not found"
	@echo ""
	@echo "$(YELLOW)UV Version:$(NC)"
	@uv --version || echo "UV not installed"
	@echo ""
	@echo "$(YELLOW)Ollama Version:$(NC)"
	@ollama --version || echo "Ollama not installed"
	@echo ""
	@echo "$(YELLOW)Project Dependencies:$(NC)"
	@uv pip list 2>/dev/null || echo "No dependencies installed yet"
	@echo ""
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"

status: ## Show git and project status
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)  Project Status$(NC)"
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo ""
	@echo "$(YELLOW)Git Status:$(NC)"
	@git status --short || echo "Not a git repository"
	@echo ""
	@echo "$(YELLOW)Git Branch:$(NC)"
	@git branch --show-current || echo "Not a git repository"
	@echo ""
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"

##@ Quick Start

quickstart: ## Quick start guide
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)  Quick Start Guide$(NC)"
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo ""
	@echo "$(YELLOW)1. First Time Setup:$(NC)"
	@echo "   make dev"
	@echo ""
	@echo "$(YELLOW)2. Terminal 1 - Start Ollama:$(NC)"
	@echo "   make ollama-serve"
	@echo ""
	@echo "$(YELLOW)3. Terminal 2 - Run CLI Chatbot:$(NC)"
	@echo "   make run-cli"
	@echo ""
	@echo "$(YELLOW)   Or run Web Chatbot:$(NC)"
	@echo "   make run-web"
	@echo ""
	@echo "$(YELLOW)4. Run Tests:$(NC)"
	@echo "   make test"
	@echo ""
	@echo "$(YELLOW)5. Before Committing:$(NC)"
	@echo "   make check"
	@echo ""
	@echo "$(GREEN)For more commands, run: make help$(NC)"
	@echo ""
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
