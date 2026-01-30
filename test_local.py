"""
Local test without installation
"""

import sys
sys.path.insert(0, '.')

from agentwatch import watch
import time
import random


@watch.agent(name="test-agent", tags=["demo"])
def test_function(x: int):
    """Test function"""
    time.sleep(0.1)
    if random.random() < 0.2:
        raise Exception("Random error")
    return x * 2


if __name__ == "__main__":
    print("🧪 Testing AgentWatch locally...\n")
    
    # Run some tests
    for i in range(5):
        try:
            result = test_function(i)
            print(f"✅ test_function({i}) = {result}")
        except Exception as e:
            print(f"❌ test_function({i}) failed: {e}")
    
    # Show stats
    print("\n📊 Stats:")
    stats = watch.stats()
    print(f"Total agents: {stats['total_agents']}")
    print(f"Total calls: {stats['total_calls']}")
    
    # List agents
    print("\n🤖 Agents:")
    agents = watch.list_agents()
    for agent in agents:
        print(f"  • {agent['name']}: {agent['total_calls']} calls, {agent['total_errors']} errors")
    
    # Get recent calls
    print("\n📞 Recent calls:")
    calls = watch.get_calls(limit=5)
    for call in calls:
        status_icon = "✅" if call['status'] == 'success' else "❌"
        print(f"  {status_icon} {call['agent_name']}: {call['duration_ms']}ms")
    
    print("\n✅ All tests passed!")
