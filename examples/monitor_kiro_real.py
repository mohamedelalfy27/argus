"""
Real-world example: Monitor Kiro AI assistant in production

This shows how to wrap Kiro's operations to track:
- Token usage
- API costs
- Response times
- Error rates
"""

from argus import watch
from typing import Dict, Any
import os


class KiroMonitor:
    """
    Wrapper class to monitor Kiro AI assistant
    """
    
    def __init__(self):
        self.watch = watch
    
    @watch.agent(name="kiro-assistant", tags=["production", "ai"])
    def process_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main entry point for Kiro requests
        Track every interaction with the AI
        """
        # In real usage, this would call Kiro's actual API
        # For now, we simulate it
        
        response = {
            "answer": "Processed by Kiro",
            "tokens_used": 250,
            "model": "claude-sonnet-4.5",
            "cost": self._calculate_cost(250)
        }
        
        return response
    
    @watch.agent(name="kiro-code-review", tags=["code", "review"])
    def review_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Track code review operations
        """
        return {
            "issues_found": 2,
            "suggestions": ["Add type hints", "Improve error handling"],
            "severity": "medium"
        }
    
    @watch.agent(name="kiro-refactor", tags=["code", "refactor"])
    def refactor_code(self, code: str, instructions: str) -> Dict[str, Any]:
        """
        Track code refactoring
        """
        return {
            "refactored": True,
            "changes": 15,
            "improved_readability": True
        }
    
    def _calculate_cost(self, tokens: int) -> float:
        """
        Calculate cost based on token usage
        Claude Sonnet pricing (example)
        """
        cost_per_1k_tokens = 0.003
        return (tokens / 1000) * cost_per_1k_tokens
    
    def get_usage_report(self) -> Dict[str, Any]:
        """
        Get comprehensive usage report
        """
        return self.watch.stats()
    
    def export_logs(self, filename: str = "kiro_usage.csv"):
        """
        Export usage logs for analysis
        """
        self.watch.export(filename, format="csv")
        print(f"✅ Exported logs to {filename}")


# Usage example
if __name__ == "__main__":
    print("🤖 Kiro AI Assistant Monitor\n")
    
    # Initialize monitor
    kiro = KiroMonitor()
    
    # Simulate Kiro usage
    print("1. Processing user request...")
    result = kiro.process_request("How do I use async/await in Python?")
    print(f"   Tokens: {result['tokens_used']}, Cost: ${result['cost']:.4f}\n")
    
    print("2. Reviewing code...")
    result = kiro.review_code("def hello(): print('hi')", "python")
    print(f"   Issues found: {result['issues_found']}\n")
    
    print("3. Refactoring code...")
    result = kiro.refactor_code("old_code", "make it cleaner")
    print(f"   Changes: {result['changes']}\n")
    
    # Get usage report
    print("=" * 50)
    print("📊 Usage Report:")
    print("=" * 50)
    
    report = kiro.get_usage_report()
    print(f"\nTotal operations: {report['total_calls']}")
    print(f"Total cost: ${report['total_cost']:.4f}")
    
    # Export logs
    print("\n📁 Exporting logs...")
    kiro.export_logs("kiro_usage.csv")
    
    print("\n🎯 View dashboard:")
    print("   argus dashboard")
    print("   Open: http://localhost:3000")
