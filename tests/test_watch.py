"""
Tests for Watch class
"""

import pytest
import tempfile
import os
from agentwatch import Watch


@pytest.fixture
def watch():
    """Create a Watch instance with temporary database"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as f:
        db_path = f.name
    
    w = Watch(db_path=db_path)
    yield w
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


def test_agent_decorator_success(watch):
    """Test successful agent call"""
    
    @watch.agent(name="test-agent")
    def test_func(x):
        return x * 2
    
    result = test_func(5)
    assert result == 10
    
    # Check stats
    stats = watch.stats()
    assert stats["total_agents"] == 1
    assert stats["total_calls"] == 1


def test_agent_decorator_error(watch):
    """Test agent call with error"""
    
    @watch.agent(name="error-agent")
    def error_func():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        error_func()
    
    # Check stats
    stats = watch.stats(agent_name="error-agent")
    assert stats["total_calls"] == 1
    assert stats["total_errors"] == 1


def test_manual_tracking(watch):
    """Test manual start/end tracking"""
    
    watch.storage.register_agent("manual-agent", [])
    
    call_id = watch.start(
        agent_name="manual-agent",
        input_data={"test": "data"}
    )
    
    assert call_id is not None
    
    watch.end(
        call_id=call_id,
        output_data={"result": "success"},
        cost=0.001
    )
    
    stats = watch.stats(agent_name="manual-agent")
    assert stats["total_calls"] == 1
    assert stats["total_cost"] == 0.001


def test_list_agents(watch):
    """Test listing agents"""
    
    @watch.agent(name="agent1", tags=["test"])
    def func1():
        return "a"
    
    @watch.agent(name="agent2", tags=["prod"])
    def func2():
        return "b"
    
    func1()
    func2()
    
    agents = watch.list_agents()
    assert len(agents) == 2
    assert any(a["name"] == "agent1" for a in agents)
    assert any(a["name"] == "agent2" for a in agents)


def test_get_calls(watch):
    """Test getting call history"""
    
    @watch.agent(name="call-test")
    def test_func(x):
        return x
    
    test_func(1)
    test_func(2)
    test_func(3)
    
    calls = watch.get_calls(agent_name="call-test", limit=10)
    assert len(calls) == 3
    assert all(c["agent_name"] == "call-test" for c in calls)


def test_tags(watch):
    """Test agent tags"""
    
    @watch.agent(name="tagged-agent", tags=["production", "critical"])
    def tagged_func():
        return "ok"
    
    tagged_func()
    
    agents = watch.list_agents()
    agent = next(a for a in agents if a["name"] == "tagged-agent")
    assert "production" in agent["tags"]
    assert "critical" in agent["tags"]


def test_multiple_calls_stats(watch):
    """Test statistics with multiple calls"""
    
    @watch.agent(name="multi-agent")
    def multi_func(x):
        if x == 5:
            raise ValueError("Five!")
        return x
    
    # Make multiple calls
    for i in range(10):
        try:
            multi_func(i)
        except ValueError:
            pass
    
    stats = watch.stats(agent_name="multi-agent")
    assert stats["total_calls"] == 10
    assert stats["total_errors"] == 1
    assert stats["error_rate"] == 0.1
