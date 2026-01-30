#!/usr/bin/env python3
"""
Load realistic demo data for Argus dashboard
"""

import sys
sys.path.insert(0, '.')

from argus import watch
import random
import time
from datetime import datetime, timedelta


# Realistic AI agent scenarios
AGENTS = [
    {
        "name": "gpt-4-assistant",
        "tags": ["openai", "production"],
        "calls": 1247,
        "avg_duration": (2000, 4000),  # ms
        "cost_per_call": (0.02, 0.08),  # $
        "error_rate": 0.02
    },
    {
        "name": "claude-code-reviewer",
        "tags": ["anthropic", "code"],
        "calls": 856,
        "avg_duration": (1500, 3000),
        "cost_per_call": (0.015, 0.045),
        "error_rate": 0.01
    },
    {
        "name": "gpt-3.5-summarizer",
        "tags": ["openai", "fast"],
        "calls": 3421,
        "avg_duration": (500, 1200),
        "cost_per_call": (0.001, 0.004),
        "error_rate": 0.03
    },
    {
        "name": "image-generator",
        "tags": ["dalle", "creative"],
        "calls": 234,
        "avg_duration": (8000, 15000),
        "cost_per_call": (0.04, 0.08),
        "error_rate": 0.05
    },
    {
        "name": "email-writer",
        "tags": ["production", "automation"],
        "calls": 1893,
        "avg_duration": (1800, 3500),
        "cost_per_call": (0.01, 0.03),
        "error_rate": 0.015
    },
    {
        "name": "data-analyzer",
        "tags": ["analytics", "batch"],
        "calls": 567,
        "avg_duration": (3000, 6000),
        "cost_per_call": (0.025, 0.06),
        "error_rate": 0.04
    }
]


def create_agent_function(agent_config):
    """Create a tracked agent function"""
    name = agent_config["name"]
    tags = agent_config["tags"]
    
    @watch.agent(name=name, tags=tags)
    def agent_function(iteration):
        # Simulate realistic duration
        duration = random.uniform(*agent_config["avg_duration"]) / 1000
        time.sleep(min(duration, 0.1))  # Cap at 0.1s for speed
        
        # Calculate cost
        cost = random.uniform(*agent_config["cost_per_call"])
        
        # Simulate errors
        if random.random() < agent_config["error_rate"]:
            raise Exception(f"API timeout for {name}")
        
        return {
            "status": "success",
            "iteration": iteration,
            "cost": cost
        }
    
    return agent_function


def load_demo_data():
    """Load realistic demo data"""
    print("🚀 Loading demo data for Argus...\n")
    
    total_calls = 0
    total_cost = 0
    
    for agent_config in AGENTS:
        print(f"📊 Loading {agent_config['name']}...")
        
        agent_func = create_agent_function(agent_config)
        calls = agent_config["calls"]
        
        # Simulate calls over time
        for i in range(min(calls, 50)):  # Limit to 50 for speed
            try:
                result = agent_func(i)
                total_cost += result.get("cost", 0)
                total_calls += 1
                
                if (i + 1) % 10 == 0:
                    print(f"  ✅ {i + 1}/{min(calls, 50)} calls")
                    
            except Exception as e:
                total_calls += 1
                if (i + 1) % 10 == 0:
                    print(f"  ❌ {i + 1}/{min(calls, 50)} calls (with errors)")
        
        print(f"  ✅ Completed {agent_config['name']}\n")
    
    print("=" * 60)
    print("📊 Demo Data Summary:")
    print("=" * 60)
    print(f"Total agents: {len(AGENTS)}")
    print(f"Total calls: {total_calls}")
    print(f"Total cost: ${total_cost:.2f}")
    print()
    print("🎯 Dashboard ready at: http://localhost:3001")
    print("=" * 60)


if __name__ == "__main__":
    load_demo_data()
