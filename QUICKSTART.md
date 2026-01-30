# Argus Quickstart

Get started with Argus in 5 minutes.

## Installation

```bash
pip install argus
```

Or install from source:

```bash
git clone https://github.com/yourusername/argus.git
cd argus
pip install -e .
```

## Basic Usage

### 1. Wrap Your Agent Function

```python
from argus import watch

@watch.agent(name="my-agent")
def my_ai_function(prompt: str):
    # Your AI logic here
    return "response"

# Call it normally
result = my_ai_function("Hello!")
```

That's it! Argus is now tracking all calls.

### 2. View Dashboard

```bash
# Start dashboard
argus dashboard

# Or in Python
from argus import watch
watch.dashboard(port=3000)
```

Open http://localhost:3000 to see:
- Total calls, costs, errors
- Per-agent statistics
- Real-time call logs

### 3. Check Stats

```bash
# CLI
argus stats
argus stats --agent my-agent

# Python
from argus import watch
stats = watch.stats()
print(stats)
```

## Real Example with OpenAI

```python
from argus import watch
from openai import OpenAI

client = OpenAI()

@watch.agent(name="gpt-assistant", tags=["production"])
def ask_gpt(prompt: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Use it
answer = ask_gpt("What is the capital of France?")
print(answer)

# Check costs
stats = watch.stats(agent_name="gpt-assistant")
print(f"Total cost: ${stats['total_cost']:.4f}")
```

## Manual Tracking

For more control:

```python
from argus import watch

# Start tracking
call_id = watch.start(
    agent_name="custom-agent",
    input_data={"prompt": "Hello"}
)

# Your logic
result = do_something()

# End tracking
watch.end(
    call_id=call_id,
    output_data={"result": result},
    cost=0.002
)
```

## Export Data

```bash
# Export to CSV
argus export data.csv

# Export to JSON
argus export data.json --format json
```

## CLI Commands

```bash
argus dashboard          # Start dashboard
argus stats              # Show statistics
argus list               # List all agents
argus export <file>      # Export data
```

## Next Steps

- Check out [examples/](examples/) for more use cases
- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Star the repo on GitHub!

## Common Issues

### Port already in use

```bash
argus dashboard --port 3001
```

### Database location

```bash
argus dashboard --db /path/to/custom.db
```

## Need Help?

- Open an issue on GitHub
- Check existing issues
- Join our Discord (coming soon)

Happy monitoring! 🚀
