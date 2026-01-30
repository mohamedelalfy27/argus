<div align="center">

# 👁️ Argus

### Open Source Observability for AI Agents

**Stop flying blind. See what your AI agents are doing.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Twitter Follow](https://img.shields.io/twitter/follow/maxcodesai?style=social)](https://x.com/maxcodesai)

[Quick Start](#-quick-start) • [Features](#-features) • [Examples](#-examples) • [Dashboard](#-dashboard)

<img src="https://via.placeholder.com/800x400/667eea/ffffff?text=Argus+Dashboard+Preview" alt="Argus Dashboard" width="800"/>

</div>

---

## 🎯 The Problem

You're building AI agents with GPT-4, Claude, or local models. They work... but you have **no idea** what's happening:

- 💸 **"Why is my API bill $5,000?"** - No cost tracking
- 🐌 **"Why is this so slow?"** - No performance metrics  
- 💥 **"Why did it fail?"** - No error monitoring
- 📊 **"Which agent is expensive?"** - No analytics

**You're flying blind.**

---

## ✨ The Solution

**Argus** - One decorator. Complete visibility.

Named after the all-seeing giant from Greek mythology with 100 eyes, Argus watches over your AI agents.

```python
from argus import watch

@watch.agent(name="my-agent")
def my_ai_function(prompt: str):
    response = openai.ChatCompletion.create(...)
    return response

# That's it! Now you see everything:
# ✅ Every call logged
# ✅ Cost tracked in real-time
# ✅ Performance monitored
# ✅ Errors caught
# ✅ Beautiful dashboard
```

---

## 🚀 Quick Start

### Installation

```bash
pip install argus
```

### Basic Usage

```python
from argus import watch

@watch.agent(name="email-bot", tags=["production"])
def send_email(to: str, subject: str):
    # Your AI logic here
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Write email to {to} about {subject}"}]
    )
    return response.choices[0].message.content

# Use it normally
result = send_email("user@example.com", "Meeting Tomorrow")

# Every call is now tracked!
```

### View Dashboard

```bash
argus dashboard
```

Open **http://localhost:3000** and see:

- 📊 Total calls, costs, errors
- ⚡ Performance metrics per agent
- 📈 Real-time activity feed
- 🎯 Cost breakdown by agent

---

## 🎨 Features

### 🔍 **Complete Visibility**
Track every agent call with input, output, duration, cost, and status.

### 💰 **Cost Tracking**
See exactly how much each agent costs. No more surprise bills.

### ⚡ **Performance Monitoring**
Identify slow agents. Optimize what matters.

### 🐛 **Error Tracking**
Catch failures instantly. See error rates per agent.

### 📊 **Beautiful Dashboard**
Real-time web UI with charts, stats, and activity feed.

### 🗄️ **Local Storage**
Everything stored in SQLite. No cloud required. Your data stays yours.

### 🏷️ **Tags & Filtering**
Organize agents by environment, team, or purpose.

### 📤 **Export Data**
Export to CSV/JSON for analysis in Excel, Python, or BI tools.

### 🚀 **Zero Config**
Works out of the box. No setup, no API keys, no hassle.

### 🪶 **Lightweight**
< 1ms overhead per call. Won't slow down your agents.

---

## 💡 Examples

### OpenAI Integration

```python
from argus import watch
from openai import OpenAI

client = OpenAI()

@watch.agent(name="gpt-assistant", tags=["openai", "production"])
def ask_gpt(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Calculate cost
    tokens = response.usage.total_tokens
    cost = (tokens / 1000) * 0.03  # GPT-4 pricing
    
    return {
        "answer": response.choices[0].message.content,
        "tokens": tokens,
        "cost": cost
    }

# Use it
result = ask_gpt("Explain quantum computing")
print(f"Answer: {result['answer']}")
print(f"Cost: ${result['cost']:.4f}")

# Check total costs
stats = watch.stats(agent_name="gpt-assistant")
print(f"Total spent: ${stats['total_cost']:.2f}")
```

### Multiple Agents

```python
from argus import watch

@watch.agent(name="email-bot", tags=["production"])
def send_email(to: str, subject: str):
    # Email logic
    return {"status": "sent"}

@watch.agent(name="slack-bot", tags=["production"])
def send_slack(channel: str, message: str):
    # Slack logic
    return {"status": "sent"}

@watch.agent(name="data-processor", tags=["etl"])
def process_data(data: list):
    # Processing logic
    return {"processed": len(data)}

# Use them
send_email("user@example.com", "Hello")
send_slack("#general", "Deployment complete")
process_data([1, 2, 3, 4, 5])

# See stats for all agents
stats = watch.stats()
print(f"Total agents: {stats['total_agents']}")
print(f"Total calls: {stats['total_calls']}")
print(f"Total cost: ${stats['total_cost']:.2f}")
```

### Error Tracking

```python
from argus import watch

@watch.agent(name="risky-agent", tags=["experimental"])
def risky_operation(data: dict):
    if not data.get("valid"):
        raise ValueError("Invalid data")
    return {"result": "success"}

# Errors are automatically tracked
try:
    risky_operation({"valid": False})
except ValueError:
    pass

# Check error rate
stats = watch.stats(agent_name="risky-agent")
print(f"Error rate: {stats['error_rate']*100:.1f}%")
```

### Manual Tracking

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
    cost=0.002,
    error=None  # or error message if failed
)
```

---

## 🎛️ Dashboard

### Start Dashboard

```bash
# Default port (3000)
argus dashboard

# Custom port
argus dashboard --port 8080

# Custom database
argus dashboard --db /path/to/custom.db
```

### Features

- **📊 Overview Stats** - Total calls, costs, errors at a glance
- **🤖 Agent Cards** - Per-agent metrics with drill-down
- **📞 Activity Feed** - Real-time call log with filtering
- **🔄 Auto-refresh** - Updates every 5 seconds
- **🎨 Beautiful UI** - Clean, modern design

---

## 🔧 CLI Commands

```bash
# View statistics
argus stats

# Filter by agent
argus stats --agent my-agent

# List all agents
argus list

# Export data
argus export data.csv
argus export data.json --format json

# Start dashboard
argus dashboard --port 3000
```

---

## 🏆 Why Argus?

### vs. Manual Logging
- ❌ Manual: Write logging code everywhere
- ✅ Argus: One decorator

### vs. Cloud Services
- ❌ Cloud: Send data to third parties, pay monthly
- ✅ Argus: Local storage, free forever

### vs. Building Your Own
- ❌ DIY: Weeks of development, maintenance burden
- ✅ Argus: Install in 30 seconds, works out of the box

### vs. Nothing
- ❌ Nothing: Flying blind, surprise bills, no debugging
- ✅ Argus: Complete visibility, cost control, easy debugging

---

## 🚦 Getting Started

### 1. Install

```bash
pip install argus
```

### 2. Add Decorator

```python
from argus import watch

@watch.agent(name="my-agent")
def my_function():
    return "result"
```

### 3. View Dashboard

```bash
argus dashboard
```

### 4. Open Browser

http://localhost:3000

**That's it!** 🎉

---

## 🤝 Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas We Need Help

- 🔌 More LLM integrations (Anthropic, Cohere, etc.)
- 💰 Better cost calculation algorithms
- 🎨 Dashboard improvements
- 📊 Advanced analytics features
- 📖 Documentation improvements
- 🌍 Internationalization

---

## 🗺️ Roadmap

### v0.2.0 - Cost Calculation
- [ ] Automatic cost calculation for OpenAI
- [ ] Anthropic Claude cost tracking
- [ ] Cohere cost tracking
- [ ] Custom cost functions

### v0.3.0 - Integrations
- [ ] LangChain integration
- [ ] LlamaIndex integration
- [ ] AutoGPT integration
- [ ] CrewAI integration

### v0.4.0 - Dashboard++
- [ ] Advanced filtering
- [ ] Charts and graphs
- [ ] Export from dashboard
- [ ] Real-time alerts

### v0.5.0 - Alerts
- [ ] Cost threshold alerts
- [ ] Error rate alerts
- [ ] Webhook notifications
- [ ] Email notifications

### v1.0.0 - Production Ready
- [ ] Multi-database support (PostgreSQL, MySQL)
- [ ] Team collaboration features
- [ ] API for external tools
- [ ] Enterprise features

See [TODO.md](TODO.md) for full roadmap.

---

## 📊 Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/sh1esty1769/argus?style=social)
![GitHub forks](https://img.shields.io/github/forks/sh1esty1769/argus?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/sh1esty1769/argus?style=social)

![GitHub issues](https://img.shields.io/github/issues/sh1esty1769/argus)
![GitHub pull requests](https://img.shields.io/github/issues-pr/sh1esty1769/argus)
![GitHub last commit](https://img.shields.io/github/last-commit/sh1esty1769/argus)

</div>

---

## 💬 Community

- **GitHub Discussions:** [Ask questions, share ideas](https://github.com/sh1esty1769/argus/discussions)
- **Issues:** [Report bugs, request features](https://github.com/sh1esty1769/argus/issues)
- **Twitter/X:** [@maxcodesai](https://x.com/maxcodesai)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with ❤️ by developers who were tired of flying blind.

Inspired by:
- [Sentry](https://sentry.io/) - Error tracking done right
- [Datadog](https://www.datadoghq.com/) - Observability platform
- [LangSmith](https://www.langchain.com/langsmith) - LLM observability

---

## 🔗 Links

- **GitHub:** https://github.com/sh1esty1769/argus
- **Issues:** https://github.com/sh1esty1769/argus/issues
- **Discussions:** https://github.com/sh1esty1769/argus/discussions
- **Twitter/X:** [@maxcodesai](https://x.com/maxcodesai)

---

## ⭐ Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=sh1esty1769/argus&type=Date)](https://star-history.com/#sh1esty1769/argus&Date)

</div>

---

<div align="center">

### **Stop flying blind. Let Argus watch your agents.** 👁️

**[Get Started Now](#-quick-start)** • **[View Examples](#-examples)** • **[Read Docs](#-documentation)**

<br/>

**If Argus helps you, give us a ⭐ on GitHub!**

[![GitHub stars](https://img.shields.io/github/stars/sh1esty1769/argus.svg?style=social&label=Star)](https://github.com/sh1esty1769/argus)

<br/>

Made with 💜 by [@maxcodesai](https://x.com/maxcodesai)

</div>
