#!/usr/bin/env python3
"""
Quick demo of Argus - run this to see it in action!
"""

import sys
sys.path.insert(0, '.')

from argus import watch
import time
import random


print("🎬 Argus Quick Demo")
print("=" * 50)
print()

# Define some demo agents
@watch.agent(name="email-bot", tags=["production"])
def send_email(to: str):
    """Simulated email sending"""
    time.sleep(random.uniform(0.05, 0.15))
    if random.random() < 0.1:
        raise Exception("SMTP timeout")
    return f"Email sent to {to}"


@watch.agent(name="data-processor", tags=["etl"])
def process_data(items: int):
    """Simulated data processing"""
    time.sleep(random.uniform(0.1, 0.3))
    return f"Processed {items} items"


@watch.agent(name="ai-assistant", tags=["openai", "production"])
def ask_ai(question: str):
    """Simulated AI call"""
    time.sleep(random.uniform(0.2, 0.5))
    return f"AI response to: {question}"


# Run demo
print("📧 Running email bot...")
for i in range(3):
    try:
        result = send_email(f"user{i}@example.com")
        print(f"  ✅ {result}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print()
print("⚙️ Running data processor...")
for i in range(3):
    result = process_data(random.randint(10, 100))
    print(f"  ✅ {result}")

print()
print("🤖 Running AI assistant...")
questions = [
    "What is Python?",
    "How do I use decorators?",
    "Explain async/await"
]
for q in questions:
    result = ask_ai(q)
    print(f"  ✅ {result}")

print()
print("=" * 50)
print("📊 Statistics:")
print("=" * 50)

# Show overall stats
stats = watch.stats()
print(f"\n🎯 Overall:")
print(f"  Total agents: {stats['total_agents']}")
print(f"  Total calls: {stats['total_calls']}")
print(f"  Total cost: ${stats['total_cost']:.4f}")

# Show per-agent stats
print(f"\n🤖 Per Agent:")
for agent in watch.list_agents():
    print(f"\n  📋 {agent['name']}")
    print(f"     Tags: {', '.join(agent['tags'])}")
    print(f"     Calls: {agent['total_calls']}")
    print(f"     Errors: {agent['total_errors']}")
    print(f"     Avg duration: {agent['avg_duration_ms']:.0f}ms")

print()
print("=" * 50)
print("🎯 Dashboard:")
print("=" * 50)
print()
print("To view the dashboard, run:")
print("  argus dashboard")
print()
print("Or in Python:")
print("  from argus import watch")
print("  watch.dashboard()")
print()
print("Then open: http://localhost:3000")
print()
print("✅ Demo complete!")
