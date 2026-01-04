# Contributing to PyVarChart

Thank you for your interest in contributing to PyVarChart! We welcome contributions of all kinds: bug reports, documentation improvements, feature requests, and code contributions.

## Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/Guy-Steiff/pyvarchart.git
cd pyvarchart
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install in development mode:**
```bash
pip install -e ".[dev]"
```

This installs PyVarChart in editable mode with development dependencies (pytest, black, flake8, mypy).

## Code Style

- **Follow PEP 8** for Python code style
- **Use type hints** for all functions and methods
- **Write docstrings** in Google style for all public functions
- **Keep Hungarian notation** for existing code consistency (e.g., `str_`, `int_`, `lst_`, `pd_`)
- **Format code** with black (optional but recommended): `black pyvarchart.py`

## Testing

### Run all tests:
```bash
pytest tests/
```

### Run with coverage:
```bash
pytest --cov=pyvarchart --cov-report=html
```

### Run specific test:
```bash
pytest tests/test_pyvarchart.py::TestBasicFunctionality::test_basic_chart_creation
```

**All tests must pass before submitting a pull request.**

## Making Changes

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the code style guidelines
4. **Add tests** for new functionality
5. **Update documentation** (README.md, docstrings, examples)
6. **Run tests** to ensure everything works:
   ```bash
   pytest tests/
   ```
7. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```
8. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
9. **Submit a pull request** on GitHub

## Pull Request Guidelines

- **Describe your changes** clearly in the PR description
- **Reference any related issues** (e.g., "Fixes #123")
- **Ensure all tests pass** before requesting review
- **Update CHANGELOG.md** if adding significant features
- **Keep PRs focused** - one feature/fix per PR when possible
- **Respond to review feedback** promptly

## Reporting Bugs

When reporting bugs, please include:
- PyVarChart version (`import pyvarchart; print(pyvarchart.__version__)`)
- Python version
- Operating system
- Minimal code example that reproduces the issue
- Expected vs actual behavior
- Full error traceback if applicable

## Suggesting Features

Feature requests are welcome! Please:
- Check if the feature already exists or is planned
- Describe the use case clearly
- Provide example usage if possible
- Be open to discussion about implementation

## Code of Conduct

- Be respectful and considerate
- Welcome newcomers and help them contribute
- Focus on constructive feedback
- Keep discussions professional

## Questions?

- **Issues:** https://github.com/Guy-Steiff/pyvarchart/issues
- **Email:** guy.steiff-pvc@bytz.me

Thank you for contributing to PyVarChart! 🎉


