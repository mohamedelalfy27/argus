# Contributing to AgentWatch

Thank you for your interest in contributing to AgentWatch! 🎉

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-for-observability.git
   cd AI-for-observability/agentwatch
   ```
3. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

## Running Tests

```bash
pytest tests/ -v
```

## Code Style

We use Black for formatting and follow PEP 8:

```bash
# Format code
black agentwatch/

# Check linting
flake8 agentwatch/

# Type checking
mypy agentwatch/
```

## Pull Request Process

1. Update README.md if you're adding features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

## Feature Requests

Open an issue with:
- Clear description of the feature
- Use case / motivation
- Example code (if applicable)

## Bug Reports

Include:
- Python version
- AgentWatch version
- Minimal reproduction code
- Expected vs actual behavior

## Areas We Need Help

- [ ] Support for more LLM providers (Anthropic, Cohere, etc.)
- [ ] Better cost calculation algorithms
- [ ] Dashboard improvements
- [ ] Performance optimizations
- [ ] Documentation improvements
- [ ] Example integrations (LangChain, LlamaIndex, etc.)

## Questions?

Open a GitHub Discussion or reach out on Twitter.

Thanks for contributing! 🚀
