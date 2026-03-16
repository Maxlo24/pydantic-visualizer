# Setup Guide for pydantic-visualizer

This guide will help you set up the pydantic-visualizer package for development and publishing.

## 📋 Prerequisites

Before you begin, ensure you have:

- Python 3.11 or higher installed
- [uv](https://github.com/astral-sh/uv) package manager installed
- Git installed
- A GitHub account (for CI/CD)
- A PyPI account (for publishing)

## 🚀 Initial Setup

### 1. Install uv (if not already installed)

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Install Dependencies

```bash
# Navigate to the project directory
cd pydantic-visualizer

# Install the package in editable mode with development dependencies
uv pip install -e ".[dev]"
```

### 3. Verify Installation

```bash
# Run tests
pytest

# Check code style
ruff check .

# Run type checking
mypy pydantic_visualizer
```

## 🧪 Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pydantic_visualizer --cov-report=html

# Run specific test file
pytest tests/test_generator.py

# Run specific test
pytest tests/test_generator.py::TestPydanticToMermaidGenerator::test_simple_model
```

### Code Quality Checks

```bash
# Format code
ruff format .

# Check for issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Type checking
mypy pydantic_visualizer
```

### Running Examples

```bash
# Run the basic usage examples
python examples/basic_usage.py
```

## 📦 Building the Package

### Local Build

```bash
# Install build tools
uv pip install build

# Build the package
python -m build

# This creates:
# - dist/pydantic_visualizer-0.1.0.tar.gz (source distribution)
# - dist/pydantic_visualizer-0.1.0-py3-none-any.whl (wheel)
```

### Test Installation

```bash
# Install from local build
uv pip install dist/pydantic_visualizer-0.1.0-py3-none-any.whl

# Or install in editable mode for development
uv pip install -e .
```

## 🔐 Setting Up GitHub Secrets

For automated publishing to PyPI, you need to set up GitHub secrets:

### 1. Get PyPI API Token

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Scroll to "API tokens"
3. Click "Add API token"
4. Name it (e.g., "pydantic-visualizer-github-actions")
5. Set scope to "Entire account" or specific to this project
6. Copy the token (starts with `pypi-`)

### 2. Add Secret to GitHub

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click "Add secret"

## 📤 Publishing to PyPI

### Option 1: Automated Publishing (Recommended)

1. Create a new release on GitHub:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. Go to GitHub → Releases → "Create a new release"
3. Choose the tag you just created
4. Fill in release notes
5. Click "Publish release"

The GitHub Action will automatically build and publish to PyPI.

### Using UV:

```bash
uv build --no-sources
```

```bash
uv publish 
```
### Option 2: Manual Publishing

```bash
# Install twine
uv pip install twine

# Build the package
python -m build

# Check the package
twine check dist/*

# Upload to TestPyPI (for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

## 🧹 Cleaning Up

```bash
# Remove build artifacts
rm -rf build/ dist/ *.egg-info/

# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove test coverage files
rm -rf .coverage htmlcov/ .pytest_cache/
```

## 🔄 Updating the Package

### Version Bumping

1. Update version in `pyproject.toml`
2. Update version in `pydantic_visualizer/__init__.py`
3. Update `CHANGELOG.md` with changes
4. Commit changes:
   ```bash
   git add .
   git commit -m "chore: bump version to 0.2.0"
   ```
5. Create and push tag:
   ```bash
   git tag v0.2.0
   git push origin main
   git push origin v0.2.0
   ```

## 🐛 Troubleshooting

### Import Errors

If you get import errors:
```bash
# Reinstall in editable mode
uv pip install -e ".[dev]"
```

### Test Failures

If tests fail:
```bash
# Clear pytest cache
rm -rf .pytest_cache/

# Reinstall dependencies
uv pip install -e ".[dev]"

# Run tests with verbose output
pytest -v
```

### Build Issues

If build fails:
```bash
# Clean build artifacts
rm -rf build/ dist/ *.egg-info/

# Rebuild
python -m build
```

## 📚 Additional Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [PyPI Help](https://pypi.org/help/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

## 🎯 Next Steps

After setup:

1. ✅ Run all tests to ensure everything works
2. ✅ Try the examples in `examples/basic_usage.py`
3. ✅ Read `CONTRIBUTING.md` for contribution guidelines
4. ✅ Check GitHub Actions are running successfully
5. ✅ Consider adding more examples or documentation
6. ✅ Plan your first release!

## 💡 Tips

- Always run tests before committing
- Use conventional commit messages
- Keep CHANGELOG.md updated
- Test on TestPyPI before publishing to PyPI
- Use semantic versioning for releases
- Document breaking changes clearly

---

**Happy Developing! 🎉**