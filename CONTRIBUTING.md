# Contributing to AI Safety Library

Thank you for your interest in contributing to the AI Safety Library! This document provides guidelines for contributing to the project.

## Getting Started

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/MUKILAN0608/ai_safety_lib.git
   cd ai_safety_lib
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev,all]"
   ```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=ai_safety_lib --cov-report=html

# Run specific test file
pytest tests/test_confidence.py -v
```

### Code Quality

```bash
# Format code with black
black ai_safety_lib tests examples

# Sort imports
isort ai_safety_lib tests examples

# Lint with flake8
flake8 ai_safety_lib tests

# Type check with mypy
mypy ai_safety_lib
```

### Security Checks

```bash
# Check for security vulnerabilities
bandit -r ai_safety_lib

# Check dependencies
safety check
```

## Pull Request Process

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a Pull Request on GitHub

### PR Guidelines

- Write clear, descriptive commit messages
- Include tests for new features
- Update documentation as needed
- Ensure all tests pass
- Follow the existing code style

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and concise

## Testing Guidelines

- Write unit tests for new functionality
- Aim for >80% code coverage
- Use descriptive test names
- Include edge cases and error conditions

## Documentation

- Update README.md for major changes
- Add docstrings to new functions/classes
- Include examples for new features
- Update type hints

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include Python version and OS information
- Provide minimal reproducible examples
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
