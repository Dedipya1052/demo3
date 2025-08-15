.PHONY: help install install-dev test test-coverage lint format clean run demo

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-coverage- Run tests with coverage report"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black"
	@echo "  clean        - Clean up generated files"
	@echo "  run          - Run the application"
	@echo "  demo         - Run the demo"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install pytest-cov

# Run tests
test:
	python -m pytest tests/ -v

# Run tests with coverage
test-coverage:
	python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# Run linting
lint:
	flake8 src/ tests/ main.py
	mypy src/ main.py

# Format code
format:
	black src/ tests/ main.py

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf build/
	rm -rf dist/

# Run the application
run:
	python main.py --help

# Run the demo
demo:
	python main.py demo

# Development setup
setup: install-dev
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file from .env.example"; fi
	@echo "Development environment setup complete!"

# Quick check
check: lint test
	@echo "All checks passed!"

# Build package
build: clean
	python setup.py sdist bdist_wheel

# Install in development mode
dev-install:
	pip install -e .