# Integrating Argus with Kiro IDE

Argus can monitor Kiro AI assistant to track token usage, costs, and performance.

## Why Monitor Kiro?

- 📊 **Track costs** - See how much each Kiro session costs
- ⚡ **Monitor performance** - Identify slow operations
- 🐛 **Debug issues** - Track when Kiro fails
- 📈 **Usage analytics** - Understand how you use Kiro

## Quick Start

### 1. Install Argus

```bash
pip install argus
```

### 2. Wrap Kiro Operations

```python
from argus import watch

@watch.agent(name="kiro-assistant")
def ask_kiro(prompt: str):
    # Your Kiro API call here
    response = kiro.process(prompt)
    return response

# Now every Kiro call is tracked!
result = ask_kiro("How do I use decorators?")
```

### 3. View Dashboard

```bash
argus dashboard
```

Open http://localhost:3000 to see:
- Total Kiro calls
- Cost per session
- Average response time
- Error rate

## Use Cases

### 1. Track Token Usage

```python
from argus import watch

@watch.agent(name="kiro-chat", tags=["production"])
def kiro_chat(message: str):
    response = kiro.chat(message)
    
    # Argus automatically logs:
    # - Input message
    # - Response
    # - Duration
    # - Timestamp
    
    return response
```

### 2. Monitor Code Generation

```python
@watch.agent(name="kiro-codegen", tags=["code"])
def generate_code(prompt: str, language: str):
    code = kiro.generate_code(prompt, language)
    
    # Track:
    # - How often you generate code
    # - Which languages you use most
    # - Average generation time
    
    return code
```

### 3. Track Debugging Sessions

```python
@watch.agent(name="kiro-debug", tags=["debug"])
def debug_with_kiro(code: str, error: str):
    fix = kiro.debug(code, error)
    
    # Monitor:
    # - Debug success rate
    # - Common errors
    # - Time to fix
    
    return fix
```

### 4. Monitor File Operations

```python
@watch.agent(name="kiro-files", tags=["filesystem"])
def kiro_file_op(operation: str, path: str):
    result = kiro.file_operation(operation, path)
    
    # Track:
    # - Read/write frequency
    # - File access patterns
    # - Operation duration
    
    return result
```

## Advanced: Cost Tracking

```python
from argus import watch

class KiroMonitor:
    @watch.agent(name="kiro-with-cost")
    def process(self, prompt: str):
        response = kiro.process(prompt)
        
        # Calculate cost
        tokens = response.get('tokens', 0)
        cost = self._calculate_cost(tokens)
        
        return {
            "response": response,
            "tokens": tokens,
            "cost": cost
        }
    
    def _calculate_cost(self, tokens: int) -> float:
        # Claude Sonnet pricing
        return (tokens / 1000) * 0.003
```

## Dashboard Features

When monitoring Kiro, you'll see:

### Overall Stats
- Total Kiro operations
- Total cost (if tracked)
- Average response time
- Error rate

### Per-Operation Stats
- Code generation: X calls, $Y cost
- Chat: X calls, $Y cost
- Debugging: X calls, $Y cost
- File ops: X calls, $Y cost

### Recent Activity
- Last 20 Kiro operations
- Success/failure status
- Duration for each
- Timestamp

## Export Data

```python
from argus import watch

# Export to CSV
watch.export("kiro_usage.csv", format="csv")

# Export to JSON
watch.export("kiro_usage.json", format="json")
```

Analyze in Excel, Python, or any data tool!

## CLI Commands

```bash
# View stats
argus stats

# Filter by Kiro operations
argus stats --agent kiro-assistant

# List all Kiro agents
argus list

# Export data
argus export kiro_logs.csv
```

## Best Practices

### 1. Tag Operations
```python
@watch.agent(name="kiro-op", tags=["production", "critical"])
```

### 2. Track Costs
Always calculate and log costs for budgeting.

### 3. Monitor Errors
Use error tracking to identify problematic prompts.

### 4. Regular Exports
Export logs weekly for analysis.

### 5. Set Alerts (Coming Soon)
Get notified when costs exceed threshold.

## Example: Full Integration

```python
from argus import watch

class KiroAssistant:
    def __init__(self):
        self.watch = watch
    
    @watch.agent(name="kiro-main", tags=["production"])
    def process_request(self, user_input: str):
        # Main Kiro processing
        response = self._call_kiro_api(user_input)
        return response
    
    @watch.agent(name="kiro-code", tags=["code"])
    def generate_code(self, prompt: str):
        # Code generation
        code = self._call_kiro_codegen(prompt)
        return code
    
    def get_usage_report(self):
        # Get comprehensive report
        return self.watch.stats()
    
    def start_dashboard(self):
        # Launch dashboard
        self.watch.dashboard(port=3000)

# Usage
kiro = KiroAssistant()
kiro.process_request("Help me with Python")
kiro.generate_code("Create a REST API")

# View stats
print(kiro.get_usage_report())

# Launch dashboard
kiro.start_dashboard()
```

## Troubleshooting

### Dashboard not showing data?
Make sure you're calling decorated functions.

### Costs not tracked?
You need to manually calculate and log costs.

### Performance impact?
Argus adds <1ms overhead per call.

## Examples

See `examples/kiro_integration.py` for complete examples.

## Questions?

Open an issue on GitHub or check the main README.

---

**Happy monitoring! 🚀**
