"""
AgentWatch - Open Source Observability for AI Agents
"""

from .watch import Watch

# Global instance
watch = Watch()

__version__ = "0.1.0"
__all__ = ["watch", "Watch"]
