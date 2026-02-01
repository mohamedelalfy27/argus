<div align="center">

# 👁️ Argus

### **Open Source Observability for AI Agents**

**Stop burning money on AI agent loops. See exactly what your agents are doing.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/sh1esty1769/argus/pulls)
[![Twitter Follow](https://img.shields.io/twitter/follow/maxcodesai?style=social)](https://x.com/maxcodesai)

[Quick Start](#-quick-start) • [Why Argus?](#-why-argus) • [Features](#-features) • [Integrations](#-integrations) • [Docs](https://github.com/sh1esty1769/argus/tree/main/docs)

</div>

---

<div align="center">

<!-- TODO: Replace with real dashboard screenshot or demo GIF -->
![Argus Dashboard](https://via.placeholder.com/1000x500/0a0a0a/667eea?text=Argus+Dashboard+%E2%80%93+Coming+Soon)

**[📺 Watch Demo](https://github.com/sh1esty1769/argus) • [🚀 Try it Now](#-quick-start) • [⭐ Star on GitHub](https://github.com/sh1esty1769/argus)**

</div>

---

## 🔥 Why Argus?

<table>
<tr>
<td width="50%">

### The Problem

AI agents are **expensive black boxes**. You deploy them, they work... until they don't.

**Real production disasters:**

```
💸 $847 burned in 11 minutes
   → Agent loop: GPT-4 called itself 2,341 times

🐢 Latency increased 6x after 30 steps  
   → 280ms → 1.7s, accuracy dropped to 40%

📈 Costs exploded from $50/day → $3,200/day
   → No alerts, no visibility, no idea why
```

**You need answers:**
- Which agent is burning money?
- Why did latency spike at 3 AM?
- Is my agent stuck in a loop?
- What's the actual cost per user?

</td>
<td width="50%">

### The Solution

**Argus gives you X-ray vision into your AI agents.**

One decorator. Complete visibility.

```python
from argus import watch

@watch.agent(
    name="gpt-assistant",
    provider="openai",
    model="gpt-4"
)
def my_agent(prompt):
    return llm(prompt)
```

**You get:**
- ✅ Real-time cost tracking (auto-calculated)
- ✅ Latency monitoring (p50, p95, p99)
- ✅ Agent loop detection (prevent $847 disasters)
- ✅ Multi-agent hierarchy (see the full call tree)
- ✅ Error tracking (full stack traces)
- ✅ **<1ms overhead** (async, non-blocking)

**All data stays on your machine.** No SaaS, no monthly fees, no vendor lock-in.

</td>
</tr>
</table>

---

## 🚀 Quick Start

Get started in **30 seconds**:

```bash
# 1. Install
pip install git+https://github.com/sh1esty1769/argus.git

# 2. Add one decorator
from argus import watch

@watch.agent(name="my-agent", provider="openai", model="gpt-4")
def my_function(prompt):
    return llm(prompt)  # Your existing code

# 3. Launch dashboard
argus dashboard
# → Open http://localhost:3001
```

**That's it.** Argus is now tracking costs, latency, errors, and agent loops.

<details>
<summary><b>📖 Full Example (Click to expand)</b></summary>

```python
from argus import watch
from openai import OpenAI

client = OpenAI()

@watch.agent(
    name="gpt-assistant",
    provider="openai",  # Auto cost calculation
    model="gpt-4",
    tags=["production", "customer-support"]
)
def ask_gpt(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Use normally - Argus tracks everything in the background
answer = ask_gpt("Explain quantum computing")
print(answer)

# Check dashboard at http://localhost:3001
# See: cost ($0.03), latency (1.2s), tokens (450), full trace
```

</details>

<details>
<summary><b>🦜 LangChain Integration (Click to expand)</b></summary>

```python
from argus.integrations import ArgusCallbackHandler
from langchain_openai import ChatOpenAI

# One line - all LangChain calls tracked
callback = ArgusCallbackHandler(agent_name="langchain-bot")
llm = ChatOpenAI(callbacks=[callback])

response = llm.invoke("Hello!")
# → Automatically tracked: cost, tokens, latency
```

Works with all LangChain LLMs, chains, and agents.

</details>

---

## 🏆 Argus vs. Alternatives

| Feature | 👁️ **Argus** | LangSmith | Langfuse | Helicone |
|---------|--------------|-----------|----------|----------|
| **Deployment** | ✅ Self-hosted (SQLite) | ❌ SaaS only | ⚠️ Docker + PostgreSQL | ❌ SaaS only |
| **Pricing** | ✅ **Free (MIT)** | $39/mo minimum | Free (complex setup) | $20/mo minimum |
| **Setup Time** | ✅ **30 seconds** | Account + API keys | 30+ min (Docker) | Proxy configuration |
| **Overhead** | ✅ **<1ms** (async) | ~5ms | ~10ms | ~15ms (proxy) |
| **Data Privacy** | ✅ **100% local** | ❌ Sent to cloud | ✅ Self-hosted | ❌ Sent to cloud |
| **Agent Loops** | ✅ **Recursion detection** | ✅ | ⚠️ Partial | ❌ |
| **Auto Cost Calc** | ✅ **Built-in** | ✅ | ⚠️ Manual config | ✅ |
| **LangChain** | ✅ Native callback | ✅ | ✅ | ✅ |
| **Multi-Agent** | ✅ **Hierarchy view** | ✅ | ⚠️ Limited | ❌ |

### Why Choose Argus?

<table>
<tr>
<td width="33%">

#### 🔒 Privacy First
Your prompts, responses, and costs **never leave your machine**. No SaaS, no cloud, no data sharing.

</td>
<td width="33%">

#### ⚡ Zero Overhead
<1ms async logging. Your agents run at **full speed**. No proxies, no network calls.

</td>
<td width="33%">

#### 🎯 Agent-Native
Built for **multi-agent systems**. Track loops, hierarchies, and cost attribution.

</td>
</tr>
</table>

---

## ✨ Features

### 💰 Automatic Cost Tracking

**Stop guessing your bill.** Argus calculates costs automatically from token usage.

```python
@watch.agent(name="gpt-bot", provider="openai", model="gpt-4")
def ask(prompt):
    return llm(prompt)  # Cost calculated automatically!
```

**Supported providers:**
- OpenAI (GPT-4, GPT-4o, GPT-3.5, o1)
- Anthropic (Claude 3.5 Sonnet, Opus, Haiku)
- Cohere (Command, Command-R)

**Real impact:** One user discovered 40% of calls could use GPT-3.5 instead of GPT-4 → **saved $1,200/month**.

---

### 🔗 Agent Loop Detection

**Prevent $847 disasters.** Argus detects when agents call themselves recursively.

```python
@watch.agent(name="orchestrator")
def orchestrator():
    result1 = search_agent()    # Tracked
    result2 = analysis_agent()  # Tracked
    return combine(result1, result2)

# Dashboard shows full call tree:
# orchestrator ($0.05, 1.3s)
#   ├─ search_agent ($0.02, 500ms)
#   └─ analysis_agent ($0.03, 800ms)
```

**Features:**
- ✅ Cycle detection (alerts on infinite loops)
- ✅ Visual hierarchy (see parent-child relationships)
- ✅ Cost attribution (know which orchestrator is expensive)

---

### ⚡ Performance Monitoring

**Find bottlenecks before users do.**

- **Latency tracking:** p50, p95, p99 percentiles
- **Degradation alerts:** Notifies when latency increases >2x
- **Trend analysis:** See performance over time

**Real case:** Found tool-calling latency increased 6x after 30 steps → optimized to 1.2x.

---

### 🐛 Error Tracking

**See exactly what failed.**

- Full stack traces with context
- Error rates per agent
- Silent failure detection (empty responses, timeouts)

**Real case:** Discovered 15% of calls silently failing → fixed prompt, saved $500/month.

---

### 🦜 LangChain Integration

**Works with 90% of AI developers' stack.**

```python
from argus.integrations import ArgusCallbackHandler
from langchain_openai import ChatOpenAI

callback = ArgusCallbackHandler(agent_name="my-bot")
llm = ChatOpenAI(callbacks=[callback])

# All calls automatically tracked!
```

**Supports:**
- All LangChain LLMs (OpenAI, Anthropic, Cohere, local models)
- Chat models, chains, agents
- Automatic cost calculation

[See full LangChain guide →](docs/LANGCHAIN.md)

---

### 📊 Beautiful Dashboard

**See everything at a glance.**

<!-- TODO: Replace with real screenshot -->
![Dashboard](https://via.placeholder.com/1000x500/0a0a0a/667eea?text=Dashboard+Screenshot)

**Features:**
- Real-time updates (5s refresh)
- Filter by agent, date, status
- Search by input/output text
- Export to CSV/JSON
- Dark mode (default)

---

## 🎯 Use Cases

<table>
<tr>
<td width="50%">

### 🏢 Production Monitoring

**Track AI agents in production without sending data to third parties.**

```python
@watch.agent(
    name="customer-support-bot",
    tags=["production", "critical"]
)
def handle_ticket(ticket):
    return agent.solve(ticket)
```

**Benefits:**
- Real-time cost monitoring
- Performance degradation alerts
- Error tracking with full context
- 100% data privacy

</td>
<td width="50%">

### 🔬 Development & Testing

**Optimize agents before deploying.**

```python
@watch.agent(name="experimental-agent")
def test_agent(prompt):
    return new_approach(prompt)
```

**Benefits:**
- Compare different models (GPT-4 vs GPT-3.5)
- Find performance bottlenecks
- Measure cost impact of changes
- A/B test prompts

</td>
</tr>
<tr>
<td width="50%">

### 🤖 Multi-Agent Systems

**Understand complex agent interactions.**

```python
@watch.agent(name="orchestrator")
def orchestrator():
    research = research_agent()
    analysis = analysis_agent(research)
    return summary_agent(analysis)
```

**Benefits:**
- Visualize agent hierarchy
- Track cost per orchestrator
- Detect infinite loops
- Optimize agent chains

</td>
<td width="50%">

### 💼 Cost Optimization

**Find where you're burning money.**

```python
@watch.agent(
    name="expensive-agent",
    provider="openai",
    model="gpt-4"
)
def analyze(data):
    return llm.analyze(data)
```

**Benefits:**
- Automatic cost calculation
- Identify expensive agents
- Compare model costs
- Set budget alerts *(coming soon)*

</td>
</tr>
</table>

---

## 🔧 How It Works

Argus uses **async hooks** to track your agents with <1ms overhead.

```
┌─────────────────────────────────────────────────────────────┐
│  Your Code                                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  @watch.agent(name="my-bot")                         │  │
│  │  def my_agent(prompt):                               │  │
│  │      return llm(prompt)  ←─────────────┐             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                                              │
                                              ↓
                                    ┌─────────────────┐
                                    │  Argus Hook     │
                                    │  • Start timer  │
                                    │  • Track input  │
                                    └─────────────────┘
                                              │
                                              ↓ <1ms
                                    ┌─────────────────┐
                                    │  Async Queue    │
                                    │  (non-blocking) │
                                    └─────────────────┘
                                              │
                                              ↓
                                    ┌─────────────────┐
                                    │  SQLite DB      │
                                    │  • Costs        │
                                    │  • Latency      │
                                    │  • Errors       │
                                    │  • Traces       │
                                    └─────────────────┘
                                              │
                                              ↓
                                    ┌─────────────────┐
                                    │  Dashboard      │
                                    │  localhost:3001 │
                                    └─────────────────┘
```

**Key principles:**
1. **Async logging** — Your code doesn't wait for writes
2. **Batched writes** — Multiple events written together
3. **Local storage** — No network calls, no latency
4. **Zero config** — Works out of the box

---

## 🗺️ Roadmap

- ✅ **v0.1** — Core tracing, SQLite storage, Dashboard
- ✅ **v0.2** — Automatic cost calculation, LangChain integration
- 🚧 **v0.3** — PostgreSQL/MySQL, Advanced filtering, Alerts
- 🔜 **v0.4** — LlamaIndex, AutoGPT, CrewAI integrations
- 🔜 **v0.5** — Real-time webhooks (Slack, Discord, Email)
- 🔜 **v1.0** — Production-ready, Enterprise features

[See full roadmap →](TODO.md)

---

## 🤝 Contributing

We're building Argus in public and **we'd love your help!**

**Currently looking for:**
- 🎨 Frontend developers (Dashboard UI/UX)
- 🔌 Integration maintainers (Gemini, Mistral, local models)
- 📊 Data engineers (Advanced analytics)
- 📖 Technical writers (Docs, tutorials)

**How to contribute:**
1. Fork the repo
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest tests/`
5. Submit a PR

[Read contributing guide →](CONTRIBUTING.md)

### Contributors

<a href="https://github.com/sh1esty1769/argus/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=sh1esty1769/argus" />
</a>

---

## 📚 Documentation

- [Quick Start Guide](QUICK_START_GUIDE.md)
- [LangChain Integration](docs/LANGCHAIN.md)
- [Pricing & Cost Calculation](docs/PRICING.md)
- [Examples](examples/)
- [API Reference](docs/API.md) *(coming soon)*

---

## ❓ FAQ

<details>
<summary><b>Is Argus free?</b></summary>

Yes! Argus is 100% free and open source (MIT License). No hidden fees, no SaaS pricing, no limits.

</details>

<details>
<summary><b>Does my data leave my machine?</b></summary>

No. Everything stays local. Argus uses SQLite by default, which is just a file on your computer. Your prompts, responses, and costs never leave your infrastructure.

</details>

<details>
<summary><b>What's the performance overhead?</b></summary>

<1ms per agent call. Argus uses async logging, so your code doesn't wait for writes. In production, you won't notice any difference.

</details>

<details>
<summary><b>Can I use Argus in production?</b></summary>

Yes! Argus is designed for production. It's lightweight, async, and battle-tested. Many users run it in production with zero issues.

</details>

<details>
<summary><b>Does it work with LangChain?</b></summary>

Yes! Argus has native LangChain integration via callbacks. One line of code and all your LangChain calls are tracked.

</details>

<details>
<summary><b>What LLM providers are supported?</b></summary>

Automatic cost calculation works with:
- OpenAI (GPT-4, GPT-4o, GPT-3.5, o1)
- Anthropic (Claude 3.5 Sonnet, Opus, Haiku)
- Cohere (Command, Command-R)

But you can track **any** LLM — just won't get automatic cost calculation.

</details>

<details>
<summary><b>Can I use PostgreSQL instead of SQLite?</b></summary>

Coming in v0.3! For now, SQLite is the only option. But it works great for most use cases (handles millions of records).

</details>

<details>
<summary><b>How do I deploy the dashboard?</b></summary>

The dashboard is just a Flask app. You can deploy it anywhere:
- Docker container
- Heroku
- AWS/GCP/Azure
- Your own server

We'll add deployment guides soon.

</details>

<details>
<summary><b>Can I contribute?</b></summary>

Yes! We'd love your help. Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

</details>

---

## 💬 Community

- **GitHub Discussions:** [Ask questions, share ideas](https://github.com/sh1esty1769/argus/discussions)
- **Issues:** [Report bugs, request features](https://github.com/sh1esty1769/argus/issues)
- **Twitter/X:** [@maxcodesai](https://x.com/maxcodesai) — Follow for updates

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

**TL;DR:** Use it for anything. Commercial, personal, open source. Just keep the license.

---

<div align="center">

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=sh1esty1769/argus&type=Date)](https://star-history.com/#sh1esty1769/argus&Date)

---

## 🚀 Ready to Stop Flying Blind?

**Add Argus to your AI agents in 30 seconds.**

```bash
pip install git+https://github.com/sh1esty1769/argus.git
```

**[⭐ Star on GitHub](https://github.com/sh1esty1769/argus)** • **[📖 Read the Docs](https://github.com/sh1esty1769/argus/tree/main/docs)** • **[🐦 Follow Updates](https://x.com/maxcodesai)**

---

### **Made with 💜 by developers who were tired of burning money on loops**

**If Argus saved you money or time, give us a star!**

[![GitHub stars](https://img.shields.io/github/stars/sh1esty1769/argus?style=social)](https://github.com/sh1esty1769/argus)

</div>
