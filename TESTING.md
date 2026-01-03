# Testing Guide

This document provides information about the test suite for the LLM-Powered Chatbot application.

## Test Overview

The test suite is located in `test_main.py` and provides comprehensive coverage of all functions in `main.py`.

### Test Statistics

- **Total Tests**: 25
- **Code Coverage**: 61%
- **All Tests Passing**: ✅

## Test Categories

### 1. TestInitializeSessionState (3 tests)
Tests for the `initialize_session_state()` function:
- Empty session state initialization
- Existing messages preservation
- Existing LLM instance preservation

### 2. TestSetupSidebar (4 tests)
Tests for the `setup_sidebar()` function:
- Model and temperature selection
- Clear chat history button
- Model options validation
- Temperature slider range validation

### 3. TestInitializeLLM (5 tests)
Tests for the `initialize_llm()` function:
- Successful LLM initialization
- Connection error handling
- Different temperature values
- Different model names
- Base URL configuration

### 4. TestDisplayChatMessages (8 tests)
Tests for the `display_chat_messages()` function:
- Empty message list
- Human message display
- AI message display
- Multiple messages
- Special characters handling
- System messages (ignored)
- HTML structure validation
- Empty and very long messages

### 5. TestIntegrationScenarios (2 tests)
Integration tests for common workflows:
- New chat session flow
- Model switching flow

### 6. TestEdgeCases (4 tests)
Edge case testing:
- Empty model name
- Boundary temperature values (0.0 and 1.0)
- Empty message content
- Very long messages (10,000 characters)

## Running Tests

### Using Make (Recommended)

```bash
# Run all tests
make test

# Run tests with verbose output
make test-verbose

# Run tests with coverage report
make test-coverage

# Run specific test
make test-specific TEST=test_initialize_llm_success
```

### Using pytest directly

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=main --cov-report=html

# Run specific test file
uv run pytest test_main.py

# Run specific test class
uv run pytest test_main.py::TestInitializeLLM

# Run specific test method
uv run pytest test_main.py::TestInitializeLLM::test_initialize_llm_success
```

## Test Dependencies

The following packages are required for testing:
- `pytest` - Testing framework
- `pytest-mock` - Mocking support
- `pytest-cov` - Coverage reporting
- `ruff` - Linter and formatter (replaces black + flake8)
- `langchain-core` - Message types (HumanMessage, AIMessage, etc.)

## Coverage Report

To generate an HTML coverage report:

```bash
make test-coverage
```

The report will be generated in `htmlcov/index.html`. Open it in your browser to see detailed coverage information.

## Writing New Tests

When adding new functions to `main.py`, follow these guidelines:

1. **Create a test class** for the function:
   ```python
   class TestYourFunction:
       """Test cases for your_function"""
   ```

2. **Mock Streamlit components** to avoid UI dependencies:
   ```python
   @patch('streamlit.some_component')
   def test_something(self, mock_component):
       # Your test here
   ```

3. **Mock session state** when needed:
   ```python
   mock_session = MagicMock()
   with patch('main.st.session_state', mock_session):
       # Your test here
   ```

4. **Test edge cases** including:
   - Empty inputs
   - Invalid inputs
   - Boundary values
   - Error conditions

5. **Use descriptive test names** that explain what is being tested:
   ```python
   def test_initialize_llm_with_invalid_model_name(self):
       """Test that invalid model names are handled gracefully"""
   ```

## Continuous Integration

To run all quality checks before committing:

```bash
make check
```

This runs:
1. Code linting with auto-fix (ruff)
2. Code formatting check (ruff)
3. All tests

### Individual Quality Checks

```bash
# Lint code
make lint

# Lint and auto-fix issues
make lint-fix

# Format code
make format

# Check formatting without changing files
make check-format

# Run all quality checks
make quality
```

## Troubleshooting

### Import Errors

If you encounter import errors:
```bash
# Make sure all dependencies are installed
uv sync
```

### Session State Errors

When testing Streamlit functions, always mock `st.session_state` properly:
```python
mock_session = MagicMock()
with patch('main.st.session_state', mock_session):
    # Your test code
```

### Coverage Not Updating

Clear pytest cache and rerun:
```bash
make clean
make test-coverage
```

## Best Practices

1. **Run tests frequently** during development
2. **Aim for >80% coverage** for new code
3. **Mock external dependencies** (Ollama, Streamlit UI)
4. **Test both success and failure paths**
5. **Keep tests fast** (all tests should run in < 1 second)
6. **Use descriptive assertions** with helpful error messages

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-mock documentation](https://pytest-mock.readthedocs.io/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
