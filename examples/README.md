# Argus Examples

This directory contains example code showing how to use Argus.

## Examples

### 1. Basic Example (`basic_example.py`)

Simple demonstration with multiple agents:
- Email sender agent
- Data processor agent
- Slack notifier agent

Shows error handling, statistics, and dashboard usage.

```bash
python examples/basic_example.py
```

### 2. OpenAI Example (`openai_example.py`)

Integration with OpenAI GPT models:
- Cost tracking
- Token counting
- Multiple prompts

Requires OpenAI API key:

```bash
export OPENAI_API_KEY="your-key-here"
pip install openai
python examples/openai_example.py
```

## Running Examples

All examples can be run directly:

```bash
# From argus directory
python examples/basic_example.py
python examples/openai_example.py
```

Each example will:
1. Execute some agent calls
2. Show statistics
3. Start the dashboard on http://localhost:3000

## Creating Your Own

Use these examples as templates:

```python
from argus import watch

@watch.agent(name="your-agent", tags=["production"])
def your_function(input_data):
    # Your logic here
    return result

# Use it
result = your_function("test")

# View stats
stats = watch.stats()
print(stats)

# Start dashboard
watch.dashboard()
```

## Need More Examples?

Check out:
- [QUICKSTART.md](../QUICKSTART.md) for basic usage
- [README.md](../README.md) for full documentation
- Open an issue to request specific examples
