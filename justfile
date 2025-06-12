# Justfile for pymadden project

# Run all tests
test:
    pytest tests/

# Run only fast unit tests
test-unit:
    pytest tests/ -m "not integration and not performance" -v

# Run integration tests (requires internet)
test-integration:
    pytest tests/ -m integration -v

# Run performance tests 
test-performance:
    pytest tests/ -m performance -v

# Run tests with coverage
test-cov:
    pytest --cov=pymadden --cov-report=term-missing tests/

# Run linting with Ruff
lint:
    ruff check .

# Run code formatting with Black and sort imports with isort
format:
    ruff format .

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