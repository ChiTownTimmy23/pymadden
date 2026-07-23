# Justfile for pymadden project

# Run tests
test:
    uv run pytest tests/

# Run tests with coverage
test-cov:
    uv run pytest --cov=pymadden --cov-report=term-missing tests/

# Run linting with Ruff
lint:
    uv run ruff check .

# Run code formatting with Ruff
format:
    uv run ruff format .

# Install project dependencies
install:
    uv sync

# Run the pre-commit hooks
pre-commit:
    pre-commit run --all-files

# Run all checks (tests, linting, formatting)
check: test lint format

# Fetch live data as a smoke test
smoke:
    uv run python test_script.py

# Build the project
build:
    uv build

# Publish the project to PyPI
publish:
    uv publish
