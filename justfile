# Justfile for pymadden project

# Run tests
test:
    pytest tests/

# Run tests with coverage
test-cov:
    pytest --cov=pymadden --cov-report=term-missing tests/

# Run linting with Ruff
lint:
    ruff .

# Run code formatting with Black and sort imports with isort
format:
	poetry run black .
	poetry run isort .

# Install project dependencies
install:
    poetry install

# Run the pre-commit hooks
pre-commit:
    pre-commit run --all-files

# Run all checks (tests, linting, formatting, and import sorting)
check: test lint format

# Build the project
build:
    poetry build

# Publish the project to PyPI
publish:
    poetry publish