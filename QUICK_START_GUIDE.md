# 🚀 Quick Start Guide for Contributors

## For Users (Try Argus)

```bash
# 1. Install
pip install git+https://github.com/sh1esty1769/argus.git

# 2. Add to your code
from argus import watch

@watch.agent(name="my-bot", provider="openai", model="gpt-4")
def my_function():
    # Your AI agent code here
    pass

# 3. View dashboard
argus dashboard
# Open http://localhost:3001
```

## For Contributors (Develop Argus)

### Setup

```bash
# 1. Clone
git clone https://github.com/sh1esty1769/argus.git
cd argus

# 2. Install in development mode
pip install -e .

# 3. Load demo data
python scripts/load_demo_data.py

# 4. Start dashboard
argus dashboard
```

### Project Structure

```
argus/
├── argus/                  # Main package
│   ├── __init__.py        # Package exports
│   ├── watch.py           # Core @watch.agent decorator
│   ├── storage.py         # SQLite database
│   ├── dashboard.py       # Flask dashboard
│   ├── cli.py             # CLI commands
│   ├── pricing.py         # Cost calculation
│   └── integrations/      # LangChain, etc.
├── examples/              # Usage examples
├── tests/                 # Unit tests
├── scripts/               # Helper scripts
└── docs/                  # Documentation
```

### Common Tasks

**Run tests:**
```bash
pytest tests/
```

**Run example:**
```bash
python examples/basic_example.py
```

**View database:**
```bash
sqlite3 argus.db
.tables
SELECT * FROM agent_runs LIMIT 5;
```

**Clear database:**
```bash
rm argus.db
python scripts/load_demo_data.py
```

## For Maintainers (Release)

### Pre-release Checklist

- [ ] All tests pass: `pytest tests/`
- [ ] Version bumped in `setup.py`
- [ ] CHANGELOG.md updated
- [ ] README.md up to date
- [ ] Examples work
- [ ] Dashboard loads

### Release Process

```bash
# 1. Update version in setup.py
# version="0.2.0"

# 2. Update CHANGELOG.md
# Add new version section

# 3. Commit
git add setup.py CHANGELOG.md
git commit -m "chore: bump version to 0.2.0"

# 4. Tag
git tag v0.2.0
git push origin main --tags

# 5. Build
python -m build

# 6. Upload to PyPI
python -m twine upload dist/*
```

## Troubleshooting

### Dashboard won't start

```bash
# Check if port 3001 is in use
lsof -i :3001

# Kill process if needed
kill -9 <PID>

# Or use different port
argus dashboard --port 3002
```

### No data in dashboard

```bash
# Load demo data
python scripts/load_demo_data.py

# Or run an example
python examples/basic_example.py
```

### Import errors

```bash
# Reinstall in development mode
pip uninstall argus
pip install -e .
```

### Database locked

```bash
# Close all connections
pkill -f "argus dashboard"

# Remove lock
rm argus.db-journal

# Restart
argus dashboard
```

## Getting Help

- **Issues:** https://github.com/sh1esty1769/argus/issues
- **Discussions:** https://github.com/sh1esty1769/argus/discussions
- **Twitter:** [@maxcodesai](https://x.com/maxcodesai)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Quick tips:
- Fork the repo
- Create a feature branch: `git checkout -b feature/my-feature`
- Make changes
- Run tests: `pytest tests/`
- Commit: `git commit -m "feat: add my feature"`
- Push: `git push origin feature/my-feature`
- Open PR on GitHub
